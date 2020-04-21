(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

symbol = document.querySelector("form[name='buy-form'] input[name='symbol']");
shares = document.querySelector("form[name='buy-form'] input[name='shares']");
submit = document.querySelector("form[name='buy-form'] input[name='buy']");
function checkFields() {
    if (symbol.value === '') {
        submit.disabled = true;
    } else {
        submit.disabled = false;
    }
}