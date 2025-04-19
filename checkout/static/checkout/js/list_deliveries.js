// Delete Confirmation Modal
document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    const deliveryNameElement = document.getElementById('deliveryName');

    deleteModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const deliveryId = button.getAttribute('data-delivery-id');
        const deliveryName = button.getAttribute('data-delivery-name');

        deliveryNameElement.textContent = deliveryName;

        deleteForm.action = `/checkout/delivery/${deliveryId}/delete/`;
    });
});