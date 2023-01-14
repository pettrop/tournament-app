# Generated by Django 4.1.5 on 2023-01-14 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discipline_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('lastname', models.CharField(max_length=32)),
                ('year_of_birth', models.PositiveSmallIntegerField()),
                ('license_validity', models.DateField()),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tournaments.club')),
            ],
            options={
                'ordering': ['lastname'],
            },
        ),
        migrations.CreateModel(
            name='Propositions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.TextField(null=True)),
                ('tournament_system', models.TextField(null=True)),
                ('notes', models.TextField(null=True)),
                ('event_location', models.CharField(max_length=128, null=True)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('category', models.ManyToManyField(to='tournaments.category')),
                ('discipline', models.ManyToManyField(to='tournaments.discipline')),
                ('league', models.ManyToManyField(to='tournaments.league')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True)),
                ('task', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_name', models.CharField(max_length=9, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('tournament_order', models.PositiveSmallIntegerField(null=True)),
                ('players', models.ManyToManyField(to='tournaments.player')),
                ('propositions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.propositions')),
                ('season', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.season')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField()),
                ('ranking', models.PositiveSmallIntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.player')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.tournament')),
            ],
        ),
        migrations.AddField(
            model_name='propositions',
            name='schedule',
            field=models.ManyToManyField(null=True, to='tournaments.schedule'),
        ),
        migrations.AddField(
            model_name='propositions',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.season'),
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizer_name', models.CharField(max_length=32)),
                ('organizer_lastname', models.CharField(max_length=32)),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.function')),
            ],
        ),
    ]
