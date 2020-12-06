var submitBtn = document.querySelector('#submit_btn')


var input_login = document.querySelector('#login')
var input_email = document.querySelector('#email')
var input_pwd = document.querySelector('#pwd')
var input_pwd_rep = document.querySelector('#pwd_rep')


submitBtn.addEventListener('click', function (e) {
    if (!validateLogin(input_login.value)) {
        input_login.classList.add('error');
    }
    else{
        input_login.classList.remove('error');
    }

    if (!validateEmail(input_email.value)) {
        input_email.classList.add('error')
    }
    else{
        input_email.classList.remove('error')
    }

    if (!validatePassword(input_pwd.value)) {
        input_pwd.classList.add('error')
    }
    else{
        input_pwd.classList.remove('error')
    }

    if (!validatePasswordRep(input_pwd.value, input_pwd_rep.value)) {
        input_pwd_rep.classList.add('error')
    }
    else{
        input_pwd_rep.classList.remove('error')
    }
});


function validatePassword(pw) {
    pattern = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}$");
    return pattern.test(pw);
}


function validateLogin(login) {
    pattern = new RegExp("^[a-zA-Z0-9_]*$");
    return pattern.test(login);
}


function validateEmail(email){
    pattern = new RegExp("^[a-zA-Z0-9\-.]+@([a-zA-Z0-9\-]+\\.)+[a-z]{2,4}$")
    return pattern.test(email);
}


function validatePasswordRep(pwr, pwd_rep){
    return pwr === pwd_rep
}