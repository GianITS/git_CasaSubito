const btnInsert = document.getElementById("btninsert")
const dpList = document.getElementById("dplist")

btnInsert.addEventListener('click', function(){
    dpList.classList.toggle("hidden");
    console.log("premuto")
})