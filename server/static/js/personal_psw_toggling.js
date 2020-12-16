var togglePasswordLast = document.querySelector('#toggle_pwd_last');
var password_last = document.querySelector('#pwd_last');


if (password_last !== null && password_last !== undefined) { 
    togglePasswordLast.addEventListener('click', function (e) {
        // toggle the type attribute
        const type = password_last.getAttribute('type') === 'password' ? 'text' : 'password';
        password_last.setAttribute('type', type);
        // toggle the eye slash icon
        this.classList.toggle('fa-eye-slash');
    });
}

var togglePassword = document.querySelector('#toggle_pwd');
var password = document.querySelector('#pwd');


if (password !== null && password !== undefined) { 
    togglePassword.addEventListener('click', function (e) {
        // toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        // toggle the eye slash icon
        this.classList.toggle('fa-eye-slash');
    });
}

var togglePasswordRep = document.querySelector('#toggle_pwd_rep');
var password_rep = document.querySelector('#pwd_rep');

if (password_rep !== null && password_rep !== undefined){    
    togglePasswordRep.addEventListener('click', function (e) {
        // toggle the type attribute
        const type = password_rep.getAttribute('type') === 'password' ? 'text' : 'password';
        password_rep.setAttribute('type', type);
        // toggle the eye slash icon
        this.classList.toggle('fa-eye-slash');
    });
}