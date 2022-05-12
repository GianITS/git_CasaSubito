const btnInsert = document.getElementById("btninsert")
const dpList = document.getElementById("dplist")
const spanIns1 = document.querySelector(".spanIns1")
const spanIns2 = document.querySelector(".spanIns2")

btnInsert.addEventListener('click', function(){
    dpList.classList.toggle("hidden");
    spanIns1.classList.toggle("animate");
    spanIns2.classList.toggle("animate");
    btnInsert.classList.toggle("active");
})