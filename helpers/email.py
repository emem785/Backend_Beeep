from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

html_verification_message = "verification.html"
html_verification_sub = ""

html_alert_message = ""
html_alert_sub = ""

def send_verification_mail(code, to_mail):

    subject = 'Account Verification'
    html_message = render_to_string(html_verification_message, {'code': code})
    plain_message = strip_tags(html_message)
    from_email = 'BEEEP VERIFICATION  <alerts@beeep.xyz>' 
    to = to_mail

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=True)