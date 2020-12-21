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
