document.addEventListener('DOMContentLoaded', function () {
    // Decrement Quantity
    document.querySelectorAll('.decrement-qty').forEach(button => {
        button.addEventListener('click', function () {
            let input = document.getElementById('id_qty_' + this.dataset.item_id);
            let currentValue = parseInt(input.value);
            if (currentValue > 1) {
                input.value = currentValue - 1;
            }
        });
    });

    // Increment Quantity
    document.querySelectorAll('.increment-qty').forEach(button => {
        button.addEventListener('click', function () {
            let input = document.getElementById('id_qty_' + this.dataset.item_id);
            let currentValue = parseInt(input.value);
            if (currentValue < 99) {
                input.value = currentValue + 1;
            }
        });
    });
});