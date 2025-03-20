window.onload = () => { //onload function - cahnge to actuall year
    const currentYearFooter = document.querySelector(".bottom-footer"); //get the footer
    const currentYear = (new Date().getFullYear()).toString(); //get the current year
    if(!currentYearFooter.textContent.includes(currentYear)){ //check if the year is the same
        currentYearFooter.innerHTML = "<p>©" + new Date().getFullYear() + " AZP88</p>"; //cahnge the year
    }
}

let pauza = 0; // follow the state of the player

document.querySelector('.pause')?.addEventListener('click', function(){ //listen and change classes of pause button
    const picon = document.querySelector('#play-icon'); //get ellement that has the icon
    if(picon.classList.contains('fa-pause')){   //check if the icon is pause or play
        picon.classList.remove('fa-pause'); //process of changing the icon
        picon.classList.add('fa-play');
        pauza = 1;  //change the state of the player
    }else{
        picon.classList.remove('fa-play');
        picon.classList.add('fa-pause');
        pauza = 0;
    }
});

const bulletsCont = document.querySelector('.bullets'); // get the container of bullets

if (bulletsCont) {
    const images = ["img1.png","img2.png", "img3.png"]; //array of images(poor database of images XD)

    images.forEach((image, index)=> {
        const bullet = document.createElement('div'); // create a bullet for each image
        bullet.classList.add('bullet'); // add class to the bullet
        if(index === 0){ // check if the bullet is the first one
            bullet.classList.add('active'); // add class to the first bullet
        }
        bulletsCont.appendChild(bullet); // add bullet to the container
    });
}
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