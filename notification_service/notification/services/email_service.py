from django.core.mail import send_mail


class SendEmailService:
    def __init__(
        self,
        email,
    ) -> None:
        self.email = email

    def send(self, message):
        subject = "New post"
        send_mail(
            subject,
            message,
            "Twiga <{}>".format("mavenwewchuli@gmail.com"),
            [self.email],
        )
