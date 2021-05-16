import smtplib
from email.message import EmailMessage

def emailalert(pincode, output):
    email_id = "sample@example.com"
    email_pwd = "sample_password"

    message = EmailMessage()
    message['Subject'] = "Vaccine Available for 18+"
    message['From'] = email_id
    message['To'] = "destination_email@gmail.com"
    message.set_content(f"Hey! vaccine for 18+ available at {pincode}\n\n{output}")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pwd)
        smtp.send_message(message)
        print("Success")