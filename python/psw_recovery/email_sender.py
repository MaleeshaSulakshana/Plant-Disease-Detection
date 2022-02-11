from email.message import EmailMessage
import smtplib


def send_recovery_code(receiver_email, code):
    # construct email
    email = EmailMessage()
    email['Subject'] = 'Plant Diseases Detection Admin Password Recovery'
    email['From'] = 'plantdiseasesdetection@gmail.com'
    email['To'] = str(receiver_email)
    email.set_content(
        """Password recovery code : <b>{}</b>""".format(str(code)), subtype='html')

    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('plantdiseasesdetection@gmail.com', 'plantdiseases')
    server.send_message(email)
    server.quit()
