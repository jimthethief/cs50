username = document.querySelector("form[name='register'] input[name='username']");
password = document.querySelector("form[name='register'] input[name='password']");
confirmation = document.querySelector("form[name='register'] input[name='confirmation']");
submit = document.querySelector("form[name='register'] input[name='submit']");
function checkFields() {
    var emptyField = (username.value === "" ||
                      password.value === "" ||
                      confirmation.value === "");
    if (emptyField) {
        submit.disabled = true;
    } else {
        submit.disabled = false;
    }
}