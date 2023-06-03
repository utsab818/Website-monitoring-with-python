import requests
import smtplib
import os
import dotenv
import paramiko
import boto3
import time
import schedule

dotenv.load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def sendMail(msg):
    print('Sending email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()

    # For prompt to confirm automatically
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(hostname='65.2.188.183', username='admin', key_filename='C:\\Users\\utsab\\Downloads\\useit.pem')
    stdin, stdout, stderr = ssh.exec_command('sudo docker start 76e09301c908')
    print(stdin)
    print(stdout.readlines())
    ssh.close()
    print('Application restarted')

def restart_server_and_container():
    # restart aws server
    ec2 = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    INSTANCE_ID = ['i-0a80477bf5b7c0e59']
    ec2.reboot_instances(InstanceIds=INSTANCE_ID)
    print('Server restarted')

    # wait for server to get started
    while True:
        response = ec2.describe_instance_status(InstanceIds=['i-0a80477bf5b7c0e59'])
        if response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
             # restart the container
             time.sleep(20)
             restart_container()
             break

def monitor_application():
    try:
        response = requests.get('http://ec2-65-2-188-183.ap-south-1.compute.amazonaws.com:8080/')

        # print(response)
        # print(response.text)
        # print(response.status_code)

        # if False: // check the else part 
        if False:
            print("Application is running successfully!")
        else:
            print('Application Down. Fix it!')
            # send email when application down
            msg =  f"Subject: SITE DOWN\nApplication returned {response.status_code}. Fix the issue! Restart the application."
            sendMail(msg)

            # restart the application
            restart_container()
            
    except Exception as ex:
        print('Connection error!!!')
        print(ex)
        msg = "Subject: SITE DOWN\nApplication not accessible..."
        sendMail(msg)

        # restart server and container
        restart_server_and_container()

# use scheduler
schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()

