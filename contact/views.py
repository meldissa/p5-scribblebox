from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages

from .forms import ContactForm

# Create your views here.


def contact(request):
    """
    Display contact form and allow users to submit messages.
    Admin receives an email to notify that user has submitted
    a query.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            email_message = render_to_string(
                'contact/contact_emails/contact_email_message.txt',
                {
                    'email': email,
                    'message': message
                }
            )
            email_subject = render_to_string(
                'contact/contact_emails/contact_email_subject.txt',
                {'subject': subject}
            )
            send_mail(email_subject, email_message,
                      email,
                      [settings.DEFAULT_FROM_EMAIL])
            messages.success(request, 'Thank you for your query! Your contact information \
            and message was successfully submitted.')
            return render(request, 'contact/contact_success.html')

    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact/contact.html', context)
