import main
import os
import sendgrid
from sendgrid.helpers.mail import *


def test_send(
        to_email='dafydd.james+test@gmail.com',
        from_email='ciaff.tickets@gmail.com',
        subject='Testing',
        mime_type='text/plain',
        body='Hello, Email!'):

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content(mime_type, body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == '__main__':
    test_send()
