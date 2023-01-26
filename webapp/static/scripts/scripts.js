// SIDE-BAR-BTN function
function displaySideBar() {
    let sideBar = document.querySelector("nav.side-bar")
    sideBar.style.display = 'block'
    let sideBarButton = document.querySelector(".side-bar-btn")
    sideBarButton.style.display = "none"
}


//SIDE-BAR-CANCEL function
function hideSideBar() {
    let sideBar = document.querySelector("nav.side-bar")
    sideBar.style.display = "none"
    let sideBarButton = document.querySelector(".side-bar-btn")
    sideBarButton.style.display = "inline"
}

function resizeControl() {
    innerSize = window.innerWidth;
    if (innerSize > 768) {
        let sideBar = document.querySelector("nav.side-bar")
        sideBar.style.display = "none"
        let sideBarButton = document.querySelector(".side-bar-btn")
        if (sideBarButton.style.display == "none") {
            sideBarButton.style.display = "block"
        }
    }
}

let sideBarButton = document.querySelector(".side-bar-btn")
let sideBarCross = document.querySelector("nav.side-bar .side-bar-cancel")
sideBarButton.addEventListener("click", displaySideBar);
sideBarCross.addEventListener("click", hideSideBar);


//SIDE-BAR-MENU DROPDOWN function
function dropdownToggle(dropMenu) {
    let dropdown = document.querySelector(`.side-menu ul li ${dropMenu}`)
    dropdown.classList.toggle("hidden")
    let allDrops = document.querySelectorAll(".side-menu ul li .dropdown")
    for (drop of allDrops) {
        if (drop == dropdown) {
            continue
        } else if (!drop.classList.contains("hidden")) {
            drop.classList.add("hidden")
        }
    }
}


//MESSAGE CANCEL CROSS

function closeMessage() {
    let message = document.querySelector(".alert")
    message.style.display = "none"
}