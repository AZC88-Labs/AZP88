window.onload = () => {
    const currentYearFooter = document.querySelector(".bottom-footer");
    const currentYear = (new Date().getFullYear()).toString();
    if(!currentYearFooter.textContent.includes(currentYear)){
        currentYearFooter.innerHTML = "<p>©" + new Date().getFullYear() + " AZP88</p>";
    }
}
