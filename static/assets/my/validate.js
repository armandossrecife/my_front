function validateEmail() {
    const email = document.getElementById('email').value;
    const confirmEmail = document.getElementById('confirmaemail').value;
  
    if (email !== confirmEmail) {
      alert('Emails do not match. Please try again.');
      return false;
    }
  
    return true;
  }
  
  function validatePassword() {
    const password = document.getElementById('pwd').value;
    const confirmPassword = document.getElementById('confirmapwd').value;
  
    if (password !== confirmPassword) {
      alert('Passwords do not match. Please try again.');
      return false;
    }
  
    return true;
  }
  
  // Add an event listener to the form's submit button
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').addEventListener('submit', (event) => {
      if (!validateEmail() || !validatePassword()) {
        event.preventDefault(); // Prevent form submission
      }
    });
  });