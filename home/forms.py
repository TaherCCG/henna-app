from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Your Name'
    )
    email = forms.EmailField(
        required=True,
        label='Your Email'
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        label='Your Phone Number'
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        label='Subject'
    )
    message = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label='Your Message'
    )

    contact_method_choices = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    contact_method = forms.ChoiceField(
        choices=contact_method_choices,
        required=False,
        label='Preferred Contact Method'
    )

    reason_choices = [
        ('support', 'Support'),
        ('feedback', 'Feedback'),
        ('inquiry', 'General Inquiry'),
    ]
    reason = forms.ChoiceField(
        choices=reason_choices,
        required=False,
        label='Reason for Contact'
    )

    consent = forms.BooleanField(
        required=True,
        label='I consent to my data being processed.'
    )
