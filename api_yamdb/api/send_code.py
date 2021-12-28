from django.core.mail import send_mail

LETTER_SUBJECT = 'Код подтверждения Yamb'
LETTER_TEXT = 'Ваш код для получения токена "confirmation_code":"{code}"'


def send_code(email, code):
    send_mail(
        LETTER_SUBJECT,
        LETTER_TEXT.format(code=code),
        None,  # Use DEFAULT_FROM_EMAIL
        [email],
        fail_silently=False,
    )
