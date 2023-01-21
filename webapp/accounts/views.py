from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SetPasswordForm, PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from tournaments.models import Club
from webapp.settings import DEBUG, EMAIL_HOST_USER
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')

    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')


def activate_email(request, user, to_email):
    mail_subject = "Activate your account"
    message = render_to_string(template_name='accounts/email_template_activate_account.html', context={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': "https" if request.is_secure() else "http"
    })
    email = EmailMessage(mail_subject, message, to={to_email})

    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on received activation link to confirm and complete registration.')

    else:
        messages.error(request, f'Problem sending email to {to_email}.')


@user_not_authenticated
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if DEBUG:
                user = form.save()
                login(request, user)
                messages.success(request, f"Nový užívateľ úspešne vytvorený!")
                return redirect('home')

            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                activate_email(request, user, form.cleaned_data.get('email'))
                return redirect('home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="accounts/signup.html",
        context={"form": form}
    )


@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "Užívateľ úspešne odhlásený!")
    return redirect('login')


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                messages.success(request, f"Užívateľ {user.first_name} {user.last_name} prihlásený!")
                return redirect('home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = AuthenticationForm()

    context = {"form": form}
    return render(
        request=request,
        template_name="registration/login.html",
        context=context
    )


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaše heslo bolo zmenené.")
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    context = {'form': form}
    return render(request=request,
                  template_name='accounts/password_reset_confirm.html',
                  context=context
                  )


@user_not_authenticated
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                mail_subject = "Žiadosť o obnovenie hesla"
                message = render_to_string(template_name='accounts/email_template_password_reset.html', context={
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': "https" if request.is_secure() else "http"
                })

                email = EmailMessage(mail_subject, message, to={associated_user.email})
                if email.send():
                    messages.success(request, f"""E-mail na obnovenie hesla bol odoslaný. Ak ste e-mail nedostali, 
                    skontrolujte, či ste zadali správnu e-mailovú adresu a zložku so spamom.""")

                else:
                    messages.error(request, f'Problém pri odosielaní resetovacieho e-mailu.')

            else:
                return redirect('home')

    form = PasswordResetForm()
    context = {'form': form}
    return render(request=request,
                  template_name='accounts/password_reset.html',
                  context=context
                  )


@user_not_authenticated
def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Heslo bolo úspešne resetované. Môžete sa prihlásiť.")
                return redirect('login')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        context = {'form': form}
        return render(request=request,
                      template_name='accounts/password_reset_confirm.html',
                      context=context
                      )

    else:
        messages.error(request, "Platnosť odkazu na obnovenie vypršala!")

    messages.error(request, "Vyskytol sa problém, presmerovanie späť na domovskú stránku.")
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    profile = request.user.profile
    group = list(Group.objects.filter(user=user))
    context = {'user': user, 'profile': profile, 'group': group}
    return render(
        request=request,
        template_name='accounts/profile.html',
        context=context
    )


@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Zmeny profilu uložené!")
            return redirect('profile')

        else:
            for error in list(user_form.errors.values()):
                messages.error(request, error)

            for error in list(profile_form.errors.values()):
                messages.error(request, error)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request=request,
                  template_name='accounts/profile_update.html',
                  context=context
                  )


def permission_request_email(request, user, profile, group, club):
    mail_subject = "Žiadosť o udelenie práv"
    message_admin = render_to_string(
        template_name='accounts/email_template_permission_request.html',
        context={
            'user': user,
            'profile': profile,
            'group': group,
            'club': club
        })

    message_user = render_to_string(
        template_name='accounts/email_template_permission_request_user_copy.html',
        context={
            'user': user,
            'profile': profile,
            'group': group,
            'club': club
        })

    email_admin = EmailMessage(mail_subject, message_admin, to={EMAIL_HOST_USER})
    email_user = EmailMessage(mail_subject, message_user, to={user.email})
    if email_admin.send() and email_user.send():
        messages.success(request, f"""Vaše žádost byla úspěšně odeslána.""")


@login_required
def permission_request(request):
    user = request.user
    profile = request.user.profile
    group = None
    club = None
    if request.method == "GET":
        group = request.GET.get('group')

    if request.method == "POST":
        group = request.GET.get('group')
        if group == "Organizátor":
            permission_request_email(request, user, profile, group, club)
            return redirect('profile')

        elif group == "Zástupca klubu":
            club = request.POST.get('clubname')
            permission_request_email(request, user, profile, group, club)
            return redirect('profile')

        else:
            messages.error(request, f'Problém pri odosielaní žiadosti.')
            return redirect('profile')

    permission_groups = ["Organizátor", "Zástupca klubu"]
    clubs = Club.objects.all()
    context = {'user': user, 'clubs': clubs, 'profile': profile, "groups": permission_groups, "group": group}
    return render(request=request,
                  template_name='accounts/permission_request.html',
                  context=context
                  )
