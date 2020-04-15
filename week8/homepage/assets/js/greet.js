// get the form
var form = document.getElementById("hiForm");

function greet()
{
	let name = document.querySelector('#name').value;
	if (name === '')
	{
		name = 'stranger';
	}
	document.querySelector('#hello').innerHTML = 'Hello, ' + name + '!';
}

function closeForm() {
    form.style.display = "none";
    document.querySelector('#hello').classList.toggle('fade');
}

// when user clicks anywhere outside of form, close it
window.onclick = function(event) {
  if (event.target == form)
  {
    closeForm();
  }
}