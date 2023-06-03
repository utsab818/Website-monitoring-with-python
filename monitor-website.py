import requests
import smtplib
import os
import dotenv

dotenv.load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def sendMail(msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

try:
    response = requests.get('http://ec2-43-205-128-29.ap-south-1.compute.amazonaws.com:8080/')

    # print(response)
    # print(response.text)
    # print(response.status_code)

    # if False: // check the else part 
    if response.status_code == 200:
        print("Application is running successfully!")
    else:
        print('Application Down. Fix it!')
        # send email when application down
        msg =  f"Subject: SITE DOWN\nApplication returned {response.status_code}. Fix the issue! Restart the application."
        sendMail(msg)
        
except Exception as ex:
    print('Connection error!!!')
    print(ex)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        msg = "Subject: SITE DOWN\nApplication not accessible..."
        sendMail(msg)