function openNav() {
    document.getElementById("searchSideBar").style.width = "170px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("searchSideBar").style.left = "10px"
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("searchSideBar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}