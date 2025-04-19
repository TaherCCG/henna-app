// Stripe payment setup
document.addEventListener('DOMContentLoaded', function () {
    /*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

    var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    var clientSecret = $('#id_client_secret').text().slice(1, -1);
    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();
    var style = {
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
    var card = elements.create('card', {style: style});
    card.mount('#card-element');
    
    // Handle realtime validation errors on the card element
    card.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
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
    
    // Handle form submit
    var form = document.getElementById('payment-form');
    
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        card.update({ 'disabled': true});
        $('#submit-button').attr('disabled', true);
        $('#payment-form').fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);
    
        var saveInfo = Boolean($('#id-save-info').attr('checked'));
        // From using {% csrf_token %} in the form
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
        };
        var url = '/checkout/cache_checkout_data/';
    
        $.post(url, postData).done(function () {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email.value),
                        address:{
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            state: $.trim(form.county.value),
                        }
                    }
                },
                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        postal_code: $.trim(form.postcode.value),
                        state: $.trim(form.county.value),
                    }
                },
            }).then(function(result) {
                if (result.error) {
                    var errorDiv = document.getElementById('card-errors');
                    var html = `
                        <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);
                    $('#payment-form').fadeToggle(100);
                    $('#loading-overlay').fadeToggle(100);
                    card.update({ 'disabled': false});
                    $('#submit-button').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        }).fail(function () {
            // just reload the page, the error will be in django messages
            location.reload();
        })
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

        // Fetch updated delivery details from the server
        fetch(`/checkout/update-delivery/${deliveryMethodId}/`)
            .then(response => response.json()) 
            .then(data => {
                // Update the page with the data received from the server
                companyNameField.textContent = `Company: ${data.company_name} (${data.delivery_name})`;
                estimatedDeliveryTimeField.textContent = `Estimated Delivery Time: ${data.estimated_delivery_time}`;
                deliveryCostField.textContent = `£${data.delivery_cost.toFixed(2)}`;
                orderSummaryDeliveryCost.textContent = `£${data.delivery_cost.toFixed(2)}`; 
                grandTotalField.textContent = `£${data.grand_total_with_vat.toFixed(2)}`;
                grandTotalToPayField.textContent = `£${data.grand_total_with_vat.toFixed(2)}`; 
            })
            .catch(error => console.error('Error:', error)); 
    });
});
