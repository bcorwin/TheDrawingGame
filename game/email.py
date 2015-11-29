from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(to_emails, subject, text_content, html_content=None, from_email=settings.POSTMARK_SENDER):
    '''
    Low-level email send function
    '''
    if to_emails != None:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        if html_content is not None: msg.attach_alternative(html_content, "text/html")
        msg.send()
    return(None)  