document.addEventListener('DOMContentLoaded', function() {
    const toastElements = {
        success: document.getElementById('successToast'),
        error: document.getElementById('errorToast'),
        info: document.getElementById('infoToast'),
        warning: document.getElementById('warningToast')
    };

    Object.keys(toastElements).forEach(type => {
        const toastEl = toastElements[type];
        if (toastEl) {
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
        }
    });
});