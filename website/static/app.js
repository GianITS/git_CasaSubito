const btnInsert = document.getElementById("btninsert")
const dpList = document.getElementById("dpList")
const menu = document.getElementById("menu")
const spanIns1 = document.querySelector(".spanIns1")
const spanIns2 = document.querySelector(".spanIns2")

btnInsert.addEventListener('click', function(){
    spanIns1.classList.toggle("animate");
    spanIns2.classList.toggle("animate");
    btnInsert.classList.toggle("active");
    menu.classList.toggle("extend");
    dpList.classList.toggle("show");
})
const search = document.querySelector(".icon")

search.addEventListener('click', function(){
    console.log("cerco")
})
const btnUser = document.querySelector(".user")
const userMenu = document.querySelector(".userMenu")

btnUser.addEventListener('click', function(){
    userMenu.classList.toggle("visible");
})