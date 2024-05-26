import smtplib
from email.mime.text import MIMEText 
from flask import render_template


def send_mail(customer, Dealer, rating, comments):
    port = 2525 
    smtp_server= "sandbox.smtp.mailtrap.io"
    username = "ce7b802e105869"
    password = "256ac85b36bdf8"
    message =  render_template("message.html", message_data={"customer": customer, "Dealer": Dealer, "rating": rating,"comments":comments })
    
    sender_email = "sender_email@example.com"
    receiver_email = "receiver_email@example.com"
    
    msg =  MIMEText(message, 'html')
    msg['Subject'] = "Lexus Feedback"
    msg["From"] = sender_email
    msg["To"] = receiver_email    
    
    #send email 
    with smtplib.SMTP(smtp_server,port) as server:
        server.login(username, password)
        server.sendmail(sender_email,receiver_email, msg.as_string())