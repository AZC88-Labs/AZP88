document.querySelectorAll('.colectsection').forEach((el)=>{
   el.addEventListener('click', (e)=>{
     const panel = el.querySelector('.panel');
     if(panel){
         if(panel.classList.contains('active')){
             panel.classList.remove('active');
         }else{
             panel.classList.add('active');
         }
     }
   });
});
