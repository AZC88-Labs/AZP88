// change current year
window.onload = () =>{
    const currentYear = new Date().getFullYear().toString();
    const footerYear = document.querySelector('.bottom-footer');
    if(!footerYear.textContent.includes(currentYear)){
        footerYear.innerHTML = "<p>>©${currentYear} AZP88</p>";
    }
}
// image slider
const controlPanel = document.querySelector('.control-panel');

if(controlPanel){
    const images = ['img1.jpg', 'img2.jpg', 'img3.webp'];
    const changeTime = 5000;
    let animationTimeout;
    let isPaused = false;

    document.querySelector('.pause')?.addEventListener('click', ()=>{
        const picon = document.querySelector('#play-icon');
        const actBullet = document.querySelector('.bullet-load');
        if(picon.classList.contains('fa-pause')){
            picon.classList.remove('fa-pause');
            picon.classList.add('fa-play');
            isPaused = true;
            clearInterval(slideInterval);
            clearTimeout(animationTimeout);
            const loadprogress = window.getComputedStyle(actBullet);
            const currwidth = loadprogress.getPropertyValue('width');
            actBullet.style.transition = 'none';
            actBullet.style.width = currwidth;
        }else{
            picon.classList.remove('fa-play');
            picon.classList.add('fa-pause');
            isPaused = false;
            actBullet.style.width = '0%';
            activeLoadAnim(actBullet);
            startInterval();
        }

    });

    images.forEach((image,index)=>{
        const bullet = document.createElement('div');
        bullet.classList.add('bullet');
        if(index === 0){
            bullet.classList.add('active');
            const bulletInside = document.createElement('div');
            bulletInside.classList.add('bullet-load');
            bullet.appendChild(bulletInside);
            activeLoadAnim(bulletInside);
        }
        controlPanel.appendChild(bullet);
    });

    const bullets = Array.from(controlPanel.children);
    let bIndex=1;
    function nextIndex(){
        if(!isPaused) curBulletAct(bullets[bIndex]);
    }

    const sliderImage = document.querySelector('.slider-image');
    function curBulletAct(target){
        const lActive = controlPanel.querySelector('.active');
        if(lActive) lActive.classList.remove('active');
        target.classList.add('active');
        bIndex = (bullets.indexOf(target)+1)%images.length;

        isPaused = false;

        const bulletInside = controlPanel.querySelector('.bullet-load');
        if (bulletInside) {
            bulletInside.remove();
            target.appendChild(bulletInside);
        }
        sliderImage.src=`img/slider/${images[bullets.indexOf(target)]}`;
        activeLoadAnim(bulletInside);
    }

    function activeLoadAnim(acBullet){
        acBullet.style.transition = 'none';
        acBullet.style.width = '0%';
        clearTimeout(animationTimeout);

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                if (!isPaused) {
                    acBullet.style.transition = `width ${changeTime / 1000}s linear`;
                    acBullet.style.width = '100%';
                }
            });
        });
    }
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearInterval(slideInterval);
            clearTimeout(animationTimeout);
        } else if (!isPaused) {
            const actBullet = document.querySelector('.bullet-load');
            if (actBullet) {
                activeLoadAnim(actBullet);
            }
            startInterval();
        }
    });

    let slideInterval;
    function startInterval(){
        slideInterval = setInterval(nextIndex, changeTime);
    }
    function resetInterval(){
        clearInterval(slideInterval);
        startInterval();
    }

    controlPanel.addEventListener('click', (e)=>{
        if(e.target.classList.contains('bullet')){
            curBulletAct(e.target);
            const pbtn = document.querySelector('#play-icon');
            if(pbtn.classList.contains('fa-play')){
                pbtn.classList.remove('fa-play');
                pbtn.classList.add('fa-pause');
            }
        }
        resetInterval()
    });
    startInterval();
}
// change login/register form
const ghostButtons = document.querySelectorAll('.ghost');
ghostButtons.forEach(button => {
    button.addEventListener('click', () => {
        const logforms = document.querySelectorAll('.logform');
        logforms.forEach(form => {
            form.classList.toggle('active');
        });
    });
});
//walidacja soon