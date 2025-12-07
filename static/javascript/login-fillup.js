// Autofill for Admin
document.getElementById("fillAdmin").addEventListener("click", function (e) {
  e.preventDefault();
  document.getElementById("inputUser").value = "admin_demo";
  document.getElementById("inputPassword").value = "admin123"; // example password
});

// Autofill for Viewer
document.getElementById("fillViewer").addEventListener("click", function (e) {
  e.preventDefault();
  document.getElementById("inputUser").value = "viewer_demo";
  document.getElementById("inputPassword").value = "viewer123"; // example password
});
