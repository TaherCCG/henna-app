const form = document.querySelector('form');

// Validates form fields to ensure required inputs are filled
function validateForm() {
    let valid = true;

    const requiredInputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    requiredInputs.forEach(input => {
        if (!input.value.trim()) {
            valid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return valid;
}

// Shows an alert with a message based on success or error
function showAlert(message, isError = false) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert ${isError ? 'alert-danger' : 'alert-success'} alert-dismissible fade show`;
    alertContainer.role = 'alert';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;

    form.parentElement.insertBefore(alertContainer, form);
}

// Event listener for form submission
form.addEventListener('submit', function (event) {
    event.preventDefault();

    if (validateForm()) {
        showAlert('Form submitted successfully!', false);
        console.log('Form data:', new FormData(form));
    } else {
        showAlert('Please fill out all required fields.', true);
    }
});
