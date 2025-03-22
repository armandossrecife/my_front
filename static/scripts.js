var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Toggle Main Sidebar
document.getElementById('toggleSidebar').addEventListener('click', function () {
    const mainSidebar = document.getElementById('mainSidebar');
    const bsCollapse = new bootstrap.Collapse(mainSidebar, { toggle: true });
});

// Function to handle button clicks
function handleButtonClick(button, urlAttribute) {
    if (button) {
        button.addEventListener('click', function () {
            const url = button.getAttribute(urlAttribute);

            if (url) {
                window.location.href = url; // Redirect to the specified URL
            } else {
                console.error(`${urlAttribute} is not defined for the button.`);
                // Optionally, show a user-friendly error message (e.g., using a toast notification)
            }
        });
    }
}

// Set up mini sidebar buttons
function setupMiniSideBarButtons() {
    // Set up the logout button
    const logoutButton = document.getElementById('logoutButton');
    handleButtonClick(logoutButton, 'data-logout-url');

    // Set up the home button
    const homeButton = document.getElementById('homeButton');
    handleButtonClick(homeButton, 'data-home-url');

    // Set up the profile button
    const profileButton = document.getElementById('profileButton');
    handleButtonClick(profileButton, 'data-profile-url');

    // Set up the setting button
    const settingButton = document.getElementById('settingButton');
    handleButtonClick(settingButton, 'data-setting-url')
}

// Call the function to set up the buttons when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    setupMiniSideBarButtons();
});