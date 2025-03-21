window.onload = () =>{ //onload check if the footer year is current year
    const currentYear = new Date().getFullYear().toString(); //get current year
    const footerYear = document.querySelector('.bottom-footer'); //get footer year
    if(!footerYear.textContent.includes(currentYear)){ //if footer year is not current year
        footerYear.innerHTML = "<p>>©${currentYear} AZP88</p>"; //set footer year to current year
    }
}

let pause = 0; //pause variable to check if the slide is paused or not
const picon = document.querySelector('#play-icon'); //get play icon

document.querySelector('.pause')?.addEventListener('click', ()=>{ //pause button event listener
    if(picon.classList.contains('fa-pause')){ //if play icon is pause
        picon.classList.remove('fa-pause');
        picon.classList.add('fa-play'); //change icon to play
        pause = 1; //set pause to 1
    }else{
        picon.classList.remove('fa-play'); //if play icon is play
        picon.classList.add('fa-pause'); //change icon to pause
        pause = 0; //set pause to 0
    }
})

const bulletsCont = document.querySelector('.bullets'); // get the container of bullets

if (bulletsCont) {
    const images = ["img01.svg","img02.svg", "img03.svg"]; //array of images(poor database of images XD)

    images.forEach((image, index)=> {
        const bullet = document.createElement('div'); // create a bullet for each image
        bullet.classList.add('bullet'); // add class to the bullet
        if(index === 0){ // check if the bullet is the first one
            bullet.classList.add('active'); // add class to the first bullet
        }
        bulletsCont.appendChild(bullet); // add bullet to the container
    });
}

bulletsCont.addEventListener('click', (event)=>{
    const bullet = event.target; // get the bullet clicked
    if(bullet.classList.contains('bullet')){
        document.querySelector('.bullet.active')?.classList.remove('active');
        bullet.classList.add('active');

        const index = Array.from(bulletsCont.children).indexOf(bullet);
        document.querySelector('.slideshow').src = `img/slider/img0${index+1}.svg`;
    }
});

// walidacja?? XD

document.getElementById("loginForm").addEventListener("submit", (event) => {
    event.preventDefault(); // pauza wysyłania formularza?
    const login = document.getElementById("email").value; // get login
    const password = document.getElementById("password").value; // get password
    const MSG = document.getElementById('loginErrorMSG');

    MSG.textContent = "";
    MSG.style.color = "red";

    const ValidEmail = (login) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(login);
    if(!ValidEmail(login)) return (MSG.textContent = "Invalid email format");

    const ValidPassword = (password) => password.length >= 8;
    if(!ValidPassword(password)) return (MSG.textContent = "Password must contain at least 8 characters");

    MSG.style.color = "green";
    MSG.textContent = "Login successful";

    //walidacja powyzej(do pozniejszych zmian)
    const loginData = {
        email: login,
        password: password
    };
    //fetch do serwera(do totalnych zmian pozniej XD)

    fetch('rzepkowyadres', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
        .then(response => response.json())
        .then(data => {
            if(data.status === "success"){
                window.location.href = "stronazalogowanapotemdozmianyrazemztymkodempewnie.html";
            }else{
                MSG.textContent = data.message;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            MSG.style.color = "red";
            MSG.textContent = "An error occurred. Please try again."; // Obsługa błędu
        });
});