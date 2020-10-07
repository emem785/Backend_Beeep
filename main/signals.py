from django.dispatch import receiver
from django.core import signals
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from helpers.verification import Verifier
from helpers.email import send_verification_mail
from main.models import Beeep

@receiver(post_save, sender=User)
def send_verification_message(sender, **kwargs):

    if kwargs.get('created', False):
        user = kwargs.get("instance")
        verifier = Verifier(user)
        verifier.gen_code()
        code = verifier.get_code()
        print(code)
        print("------------------------------sending code..!!!---------------------------------")
        # send_verification_mail(code.get('code', False), user.email)
        print("------------------------------Code sent..!!!---------------------------------")

post_save.connect(send_verification_message, sender = User)

@receiver(post_save, sender=Beeep)
def send_beeep_message(sender, **kwargs):

    if kwargs.get('created', False):
        user = kwargs.get("instance")
        
        print("------------------------------sending code..!!!---------------------------------")
        print("------------------------------Code sent..!!!---------------------------------")

post_save.connect(send_beeep_message, sender = Beeep)