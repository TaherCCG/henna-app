// Increment Quantity
$('.increment-qty').click(function (e) {
    e.preventDefault();  // Prevent default button behaviour
    let inputField = $(this).closest('tr').find('.qty_input');
    let currentQty = parseInt(inputField.val());
    inputField.val(currentQty + 1);  // Increment the quantity
    $(this).closest('form').submit();  // Submit the form to update the quantity
});

// Decrement Quantity
$('.decrement-qty').click(function (e) {
    e.preventDefault();
    let inputField = $(this).closest('tr').find('.qty_input');
    let currentQty = parseInt(inputField.val());

    if (currentQty > 1) {  // Ensure quantity does not go below 1
        inputField.val(currentQty - 1);  // Decrement the quantity
        $(this).closest('form').submit();  // Submit the form to update the quantity
    }
});

// Remove item from cart and reload page
$('.remove-item').click(function (e) {
    e.preventDefault();
    let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    let itemId = $(this).attr('id').split('remove_')[1];
    let url = `/cart/remove_from_cart/${itemId}/`;
    let data = { 'csrfmiddlewaretoken': csrfToken };

    // Send a POST request to remove the item
    $.post(url, data)
        .done(function () {
            location.reload();
        })
        .fail(function () {
            alert('Failed to remove item. Please try again.');
        });
});
