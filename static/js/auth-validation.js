const passwordInput = document.getElementById('password');
const strengthMeter = document.getElementById('password-strength');

if (passwordInput) {
    passwordInput.addEventListener('input', () => {
        const val = passwordInput.value;
        let strength = 0;

        if (val.length > 5) strength += 25;
        if (val.match(/[A-Z]/)) strength += 25;
        if (val.match(/[0-9]/)) strength += 25;
        if (val.match(/[^A-Za-z0-9]/)) strength += 25;

        strengthMeter.style.width = strength + '%';

        // Color coding
        if (strength < 50) {
            strengthMeter.style.background = '#e74c3c'; // Red
        } else if (strength < 100) {
            strengthMeter.style.background = '#f1c40f'; // Yellow
        } else {
            strengthMeter.style.background = '#2ecc71'; // Green
        }
    });
}