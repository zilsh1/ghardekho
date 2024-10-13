//     Project title      : GharDekho
//      Enrollment number  : 22002171410064
//      Date               : 30, march, 2024
//      Subject            : Full stack development(Frontend)
const pwd=document.getElementById('pwd')
const form=document.getElementById('loginForm')
const error=document.getElementById('err')

form.addEventListener('submit',(e)=>{ //
   e.preventDefault()
   if(pwd.value.length<8){
        error.innerText="Please provide password with atleast 8 character"
   }else{
      error.innerText=""
   }
})