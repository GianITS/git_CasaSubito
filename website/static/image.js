
const inner1 = document.getElementById("inner1")
const inner2 = document.getElementById("inner2")
const inner3 = document.getElementById("inner3")
const inner4 = document.getElementById("inner4")
const inner5 = document.getElementById("inner5")
const inner6 = document.getElementById("inner6")
const s1 = document.querySelector(".slides.s1")

inner1.addEventListener('click', function(){
    s1.classList.add("move1");
    s1.classList.remove("move2");
    s1.classList.remove("move3");
    s1.classList.remove("move4");
    s1.classList.remove("move5");
    s1.classList.remove("move6");
})
inner2.addEventListener('click', function(){
    s1.classList.remove("move1");
    s1.classList.add("move2");
    s1.classList.remove("move3");
    s1.classList.remove("move4");
    s1.classList.remove("move5");
    s1.classList.remove("move6");
})
inner3.addEventListener('click', function(){
    s1.classList.remove("move1");
    s1.classList.remove("move2");
    s1.classList.add("move3");
    s1.classList.remove("move4");
    s1.classList.remove("move5");
    s1.classList.remove("move6");
})
inner4.addEventListener('click', function(){
    s1.classList.remove("move1");
    s1.classList.remove("move2");
    s1.classList.remove("move3");
    s1.classList.add("move4");
    s1.classList.remove("move5");
    s1.classList.remove("move6");
})
inner5.addEventListener('click', function(){
    s1.classList.remove("move1");
    s1.classList.remove("move2");
    s1.classList.remove("move3");
    s1.classList.remove("move4");
    s1.classList.add("move5");
    s1.classList.remove("move6");
})
inner6.addEventListener('click', function(){
    s1.classList.remove("move1");
    s1.classList.remove("move2");
    s1.classList.remove("move3");
    s1.classList.remove("move4");
    s1.classList.remove("move5");
    s1.classList.add("move6");
})