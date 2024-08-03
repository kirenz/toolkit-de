// ... your password prompt and validation logic ...

// Wrap the content in a function
function protectContent() {
    // Check if the user has already entered the correct password
    if (!localStorage.getItem('accessGranted')) {
        const password = prompt('Enter password to access this site:');
        if (password === 'your_password') {
            localStorage.setItem('accessGranted', true);
        } else {
            document.body.innerHTML = 'Incorrect password. Access denied.';
        }
    }
}

// Call the function when the DOM is loaded
document.addEventListener('DOMContentLoaded', protectContent);
