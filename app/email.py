from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    print(current_app.config['MAIL_EMAIL'])
    token = user.get_reset_password_token()
    send_email(('[EcoHUB] Reset Your Password'),
               sender=current_app.config['MAIL_EMAIL'],
               recipients=[user.email_address],
               text_body=render_template('users/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('users/reset_password.html',
                                         user=user, token=token))