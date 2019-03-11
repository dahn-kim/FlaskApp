import secrets
import os
from flask import url_for, current_app
from PIL import Image #image as a class
from flask_mail import Message
from app import mail

def save_picture(pic_form):
    """
    saving the picture from account form and modify the size and the name of the image file
    """

    random_hex = secrets.token_hex(8) #creating random characters for the filename


    # 1. splitting the name of the file and the format of the file
    # 2. file_name -> _ , because we are not going to use file_name but returning file_ext only.
    _ , file_ext = os.path.splitext(pic_form.filename)

    #now joining two strings
    picture_filename = random_hex + file_ext

    #our root starts from 'run.py' then running at 'app' folder as we are calling it from run.py, everyone has different root path so we use "current_app.root_path"
    picture_path = os.path.join(current_app.root_path, "static/img/profile_pics", picture_filename)

    output_size = (200,200)
    img = Image.open(pic_form) # img as an object of the image class)
    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_filename

def send_reset_email(user):
    token = user.get_reset_token()

    msg = Message('Password Reset Request',
                    sender='noreply@python0to1.com',
                    recipients = [user.email]
                    )

    msg.body = f""" To reset password, click the link below:

    {url_for('auth.reset_password', token=token, _external=True)}

    The link is valid only in 30 minutes.
    If it was not you, please ignore this email.
    """

    mail.send(msg)
