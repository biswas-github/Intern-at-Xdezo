var form = document.querySelector("form");
var passwordInput = document.getElementById("password");
var passwordError = document.getElementById("password-error");

form.onsubmit = function (event) {
  var value = passwordInput.value;
  value = value.trim();

  // very simple rule: required and at least 4 characters
  if (value === "") {
    passwordError.textContent = "Password is required.";
    event.preventDefault();
  } else if (value.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters.";
    event.preventDefault();
  } else {
    passwordError.textContent = "";
  }
};
