document.addEventListener('DOMContentLoaded', function () {
    /*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
    */

    let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    let clientSecret = $("input[name='client_secret']").val();
    let stripe = Stripe(stripePublicKey);
    let elements = stripe.elements();
    let style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    let card = elements.create('card', { style: style });
    card.mount('#card-element');

    // Handle real-time validation errors on the card element
    card.addEventListener('change', function (event) {
        let errorDiv = document.getElementById('card-errors');
        if (event.error) {
            let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    // Handle form submission
    let form = document.getElementById('payment-form');

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();

        // Disable the card element and show spinner
        card.update({ 'disabled': true });
        $('#submit-button').attr('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Processing...');

        // Set up timeout (10 seconds)
        const paymentTimeout = setTimeout(() => {
            let errorDiv = document.getElementById('card-errors');
            let html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>Payment is taking longer than expected. Please refresh and try again.</span>
            `;
            $(errorDiv).html(html);
            card.update({ 'disabled': false });
            $('#submit-button').attr('disabled', false).html('Submit Payment');
        }, 10000);

        // Get the PaymentIntent ID from the client secret
        const paymentIntentId = clientSecret.split('_secret')[0];
        
        // Create PaymentMethod and confirm payment
        stripe.createPaymentMethod({
            type: 'card',
            card: card,
        }).then(function(pmResult) {
            if (pmResult.error) {
                clearTimeout(paymentTimeout);
                showStripeError(pmResult.error);
                return Promise.reject(pmResult.error);
            }

            console.log('Using existing PaymentIntent:', paymentIntentId);
            
            // Add PaymentIntent ID to form data
            $('<input>').attr({
                type: 'hidden',
                name: 'payment_intent_id',
                value: paymentIntentId
            }).appendTo(form);

            // Confirm payment with existing PaymentIntent
            return stripe.confirmCardPayment(clientSecret, {
                payment_method: pmResult.paymentMethod.id,
                receipt_email: $('#id_email').val(),
                shipping: {
                    name: $('#id_full_name').val(),
                    phone: $('#id_phone_number').val(),
                    address: {
                        line1: $('#id_street_address1').val(),
                        line2: $('#id_street_address2').val(),
                        city: $('#id_town_or_city').val(),
                        state: $('#id_county').val(),
                        postal_code: $('#id_postcode').val(),
                        country: $('#id_country').val()
                    }
                }
            });
        }).then(function(confirmResult) {
            clearTimeout(paymentTimeout);
            
            if (confirmResult.error) {
                showStripeError(confirmResult.error);
                return;
            }

            if (confirmResult.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }).catch(function(error) {
            clearTimeout(paymentTimeout);
            console.error('Payment flow error:', error);
            showStripeError(error.message ? error : {message: 'Payment processing failed'});
        });

        function showStripeError(error) {
            let errorDiv = document.getElementById('card-errors');
            let html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${error.message}</span>
            `;
            $(errorDiv).html(html);
            card.update({ 'disabled': false });
            $('#submit-button').attr('disabled', false).html('Submit Payment');
        }
    });

    // Delivery method update setup
    const deliverySelect = document.getElementById('id_delivery_method');
    const deliveryCostField = document.getElementById('delivery-cost');
    const orderSummaryDeliveryCost = document.getElementById('order-summary-delivery-cost');
    const grandTotalField = document.getElementById('grand-total');
    const grandTotalToPayField = document.getElementById('grand-total-to-pay');
    const estimatedDeliveryTimeField = document.getElementById('estimated-delivery-time');
    const companyNameField = document.getElementById('company-name');

    // Update delivery cost and details when delivery method changes
    deliverySelect.addEventListener('change', function () {
        const deliveryMethodId = this.value;
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val() || $('meta[name="csrf-token"]').attr('content');

        // Disable the submit button during update
        $('#submit-button').attr('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Updating...');

        // Fetch updated delivery details and update PaymentIntent
        $.ajax({
            url: `/checkout/update-delivery/${deliveryMethodId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                // Update UI
                companyNameField.textContent = `Company: ${data.company_name} (${data.delivery_name})`;
                estimatedDeliveryTimeField.textContent = `Estimated Delivery Time: ${data.estimated_delivery_time}`;
                deliveryCostField.textContent = `£${data.delivery_cost.toFixed(2)}`;
                orderSummaryDeliveryCost.textContent = `£${data.delivery_cost.toFixed(2)}`;
                grandTotalField.textContent = `£${data.grand_total_with_vat.toFixed(2)}`;
                grandTotalToPayField.textContent = `£${data.grand_total_with_vat.toFixed(2)}`;
    
                // Update Stripe elements with new client secret
                if (data.client_secret) {
                    clientSecret = data.client_secret;
                    $("input[name='client_secret']").val(data.client_secret);

                    // Refresh Stripe Elements
                    stripe = Stripe(stripePublicKey);
                    elements = stripe.elements();
                    card = elements.create('card', { style: style });
                    card.mount('#card-element');
                }
            
                // Re-enable submit button
                $('#submit-button').attr('disabled', false).html('Submit Payment');
            },
            error: function (xhr, status, error) {
                console.error('Error:', xhr.responseJSON || error);
                let errorMsg = 'Error updating delivery cost';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                deliveryCostField.textContent = errorMsg;
                $('#submit-button').attr('disabled', false).html('Submit Payment');
            }
        });
    });
});
