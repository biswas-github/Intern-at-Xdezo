// simple demo credentials
const adminCreds = { username: "admin_demo", password: "admin123" };
const viewerCreds = { username: "viewer_demo", password: "viewer123" };

const inputUser = document.getElementById("inputUser");
const inputPassword = document.getElementById("inputPassword");

const adminBtn = document.querySelector(".Admin-sign-in button");
const viewerBtn = document.querySelector(".viewer-sign-in button");

adminBtn.addEventListener("click", function () {
  inputUser.value = adminCreds.username;
  inputPassword.value = adminCreds.password;
});

viewerBtn.addEventListener("click", function () {
  inputUser.value = viewerCreds.username;
  inputPassword.value = viewerCreds.password;
});
