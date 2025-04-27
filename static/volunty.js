// Open the registration modal
function openModal() {
  document.getElementById("myModal").style.display = "flex";
}

// Close the registration modal
function closeModal() {
  document.getElementById("myModal").style.display = "none";
}

// Toggle dark/light mode
function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
}

// Handle volunteer form submission
function submitVolunteer() {
  const name = document.getElementById("volunteerName").value.trim();
  const email = document.getElementById("volunteerEmail").value.trim();
  const phone = document.getElementById("volunteerPhone").value.trim();
  const role = document.getElementById("volunteerRole").value;

  if (!name || !email || !phone || !role) {
    alert("Please fill in all fields.");
    return;
  }

  // Placeholder behavior (just shows an alert for now)
  alert("Thank you for registering, " + name + "!");
  closeModal();

  // Later we can add AJAX POST here to send data to backend server!
}
