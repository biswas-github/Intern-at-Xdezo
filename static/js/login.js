window.onload = function () {
  var form = document.querySelector("form");
  var usernameInput = document.getElementById("username");
  var passwordInput = document.getElementById("password");

  var adminBtn = document.querySelector("button[name='role'][value='ADMIN']");
  var viewerBtn = document.querySelector("button[name='role'][value='VIEWER']");

  // When admin button is clicked, fill admin data then submit
  adminBtn.addEventListener("click", function (event) {
    // if you only want to fill (not submit automatically), uncomment next line

    event.preventDefault();
    usernameInput.value = "admin_demo";
    passwordInput.value = "admin1234";
  });

  // When viewer button is clicked, fill viewer data then submit
  viewerBtn.addEventListener("click", function (event) {
    // if you only want to fill (not submit automatically), uncomment next line
    event.preventDefault();
    usernameInput.value = "viewer_demo";
    passwordInput.value = "viewer1234";
  });
};
