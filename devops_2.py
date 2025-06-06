# DevOps Assignment 2
# Michael McKibbin 20092733
#
# Requires:
# python3 & boto3
#
# AWS CLI credentials are stored in a separate file, (~/.aws/credentials)
#
# AMI:
# Amazon Linux2 AMI image: ami-0ced9049444b57252
# Instance type: nano
# Keypair: key6.pem (~/key6.pem)
# Security group ID: sg-08506a9bf41ce7f35 (MyDevOpsSecurityGroup02)
#
# ====================
#

import boto3
import time
import webbrowser
import random
import string
import urllib
import os
from cgitb import html
from ipaddress import ip_address
from os import system
from urllib import response
from botocore.exceptions import ClientError
import json

# Part A Core Functionality

# 1. Launch New EC2 Instance
# 2. Configure instance settings
# 3. Set up EC2 website
# Download and install Apache web server
# Create index.html and add content
# Get meta data
# Get image
# copy index.html to local drive
ec2 = boto3.resource("ec2")
try:
    print("\nCreating new EC2 instance\n")

    new_ec2_instance = ec2.create_instances(
        # Amazon Linux2 AMI (check current available AMIs before assignment submission)
        ImageId="ami-0ced9049444b57252",
        # How many instances to launch. Min and Max
        MinCount=1,
        MaxCount=3,
        # Instance type (t2.nano)
        InstanceType="t2.nano",
        # Tag the instance
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "devops2Autoscale"},
                    {"Key": "Owner", "Value": "mmckibbin"},
                ],
            },
        ],
        # MyDevOpsSecurityGroup01 Security group ID
        SecurityGroupIds=["sg-08506a9bf41ce7f35"],
        KeyName="key6",
        UserData="""#!/bin/bash
            yum install httpd -y
            systemctl enable httpd
            systemctl start httpd

            echo "Content-type: text/html"
            echo '<html>' > index.html
            echo '<head>' >> index.html
            echo '<title>DevOps Assignment 1</title>' >> index.html
            echo '</head>' >> index.html
            echo '<body>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:200%;">Assignment 2: DevOps_2</p>' >> index.html   
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">AMI: ' >> index.html
            echo $(curl http://169.254.169.254/latest/meta-data/ami-id) >> index.html
            echo '</p>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">Instance ID: ' >> index.html
            echo $(curl http://169.254.169.254/latest/meta-data/instance-id) >> index.html
            echo '</p>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">Instance Type: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/instance-type) >> index.html
            echo '</p>' >> index.html
            
            echo '<p style="font-family:Helvetica, sans-serif; font-size:150%;">Instance IP: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/public-ipv4) >> index.html
            echo '</p>' >> index.html

            echo '<p style="font-family:Helvetica, sans-serif;">Security Group: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/security-groups) >> index.html
            echo '</p>' >> index.html

            echo '<p style="font-family:Helvetica, sans-serif;">Availability Zone: ' >> index.html 
            echo $(curl http://169.254.169.254/latest/meta-data/placement/availability-zone-id ) >> index.html
            echo '</p>' >> index.html

            echo '<img src="http://devops.witdemo.net/logo.jpg"> logo.jpg ' >> index.html
            echo '</body>' >> index.html
            echo '</html>' >> index.html

            cp index.html /var/www/html/index.html
        """,
    )

except Exception as e:
    print("Error! \nThe EC2 creation process has encountered an error.\n")
    print(e)
    errorfile = open("error.log", "w")
    errorfile.write(str(e))
    errorfile.close()
    print("See error.log for details.")

else:
    # Print instance ID, type, & state
    print(
        "\nNew EC2 instance created successfully!"
        + "\n[ID: "
        + new_ec2_instance[0].id
        + "]"
        + "\n[Type: "
        + new_ec2_instance[0].instance_type
        + "]"
        +
        #'\n[Region: ' + new_ec2_instance[0].region['Name'] + ']' +
        "\n[Current state: "
        + new_ec2_instance[0].state["Name"]
        + "]"
    )

    # Check instance state every 5 seconds.
    print("\nWaiting for instance to run...")
    while new_ec2_instance[0].state["Name"] != "running":
        time.sleep(5)
        new_ec2_instance[0].reload()

    # Print instance state & public ip address
    print(
        "\n\n[Current state: "
        + new_ec2_instance[0].state["Name"]
        + "]\n"
        + "[Public IP: "
        + new_ec2_instance[0].public_ip_address
        + "]\n"
    )

    # Wait x seconds for webserver to initialise
    print("\n\nAllowing time for web server to initialise...")
    time.sleep(60)
    print("\nOpening webpage at: " + new_ec2_instance[0].public_ip_address)
    print("\n\n")
    ip_address = new_ec2_instance[
        0
    ].public_ip_address  # Set variable to instance public IP
    webbrowser.open(
        "http://" + new_ec2_instance[0].public_ip_address
    )  # Open web browser to instance public IP

    # 6. Monitoring
    # Out of sequence numerically as connection timed out when running later on, after s3 setup (Sections 4 & 5)
try:
    time.sleep(30)  # wait a bit...
    # set keypair permissions for ssh access
    print("\nSet keypair permission")
    system("chmod 400 key6.pem")
    print("\nDone.")
    print("\n")

    # copy monitoring scripts to instance, run them.
    print("\nCopying monitor.sh to ec2 instance")
    system(
        f"scp -o StrictHostKeyChecking=no -i key6.pem monitor.sh ec2-user@{ip_address}:."
    )
    print("\nDone.")
    print("\n")
    print("\nSet permissions on monitor.sh")
    system(f"ssh -i key6.pem ec2-user@{ip_address} 'chmod 700 monitor.sh'")
    print("\nDone.")
    print("\n")
    print("\nRun monitor.sh (on ec2 instance)")
    system(f"ssh -i key6.pem ec2-user@{ip_address} './monitor.sh'")
    print("\nend of monitoring script")
    print("\n")

    print("\nCopying memv2.sh to ec2 instance")
    system(
        f"scp -o StrictHostKeyChecking=no -i key6.pem memv2.sh ec2-user@{ip_address}:."
    )
    print("\nDone.")
    print("\n")
    print("\nSet permissions on memv2.sh")
    system(f"ssh -i key6.pem ec2-user@{ip_address} 'chmod 700 memv2.sh'")
    print("\nDone.")
    print("\n")
    print("\nRun memv2.sh (on ec2 instance)")
    system(f"ssh -i key6.pem ec2-user@{ip_address} './memv2.sh'")
    print("\nend of memv2 script")
    print("\n")



    # list files in instance
    print("\nList files in instance" + new_ec2_instance[0].id + "...")
    system(f"ssh -i key6.pem ec2-user@{ip_address} 'ls -l'")
    print("\nDone.")
    print("\n")

    # # copy install-node.sh and run it
    # print("\nCopying install-node.sh to ec2 instance")
    # system(
    #     f"scp -o StrictHostKeyChecking=no -i key6.pem install-node.sh ec2-user@{ip_address}:."
    # )
    # print("\nSet permissions on install-node.sh")
    # system(f"ssh -i key6.pem ec2-user@{ip_address} 'chmod 700 install-node.sh'")
    # print("\nRun install-node.sh")
    # system(f"ssh -i key6.pem ec2-user@{ip_address} './install-node.sh'")
    # print("\nend of install-node.sh script")
    # print("\n")

#     # install Node.js
#     print("\nInstalling Node.js...")
#     system("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash")
#     system("source ~/.nvm/nvm.sh")
#     system("nvm install 16")
#     system("node -v")
#     print("\nDone.")

except Exception as e:
    print(e)


# Upload the app.js file to ec2 instance
file_path = "app.js"
print("\nUploading " + file_path + " to ec2 instance...")
system(
    f"scp -o StrictHostKeyChecking=no -i key6.pem {file_path} ec2-user@{ip_address}:."
)
print("\nDone.")
print("now connect via SSH and install node, then run app")
time.sleep(10)

# # run app.js
# print("\nRunning app.js...")
# system("node app.js")
# print("\nDone.")

# # open browser window to ec2 instance
# print("\nOpening browser window to ec2 instance...")

# print("\nOpening webpage at: " + new_ec2_instance[0].public_ip_address)
# print("\n\n")
# ip_address = new_ec2_instance[
#     0
# ].public_ip_address  # Set variable to instance public IP
# webbrowser.open(
#     "http://" + new_ec2_instance[0].public_ip_address +":3000"
# )  # Open web browser to instance public IP



# # install Node.js
# print("\nInstalling Node.js...")
# system("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash -")
# system("source ~/.nvm/nvm.sh")
# system("nvm install 16")
# #export nvm dir to bashrc
# system("export NVM_DIR=$HOME/.nvm")
# system("[ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\"")
# system("[ -s \"$NVM_DIR/bash_completion\" ] && \. \"$NVM_DIR/bash_completion\"")
# system("nvm use 16")
# print("\ninstalling npm")
# system("npm install -g npm@latest")
# # get node version number
# print("\nNode version:")
# system("node -v")
# print("\nDone.")

# # Upload the app.js file
# file_path = "app.js"
# if os.path.exists(file_path):
#     try:
#         s3_client.upload_file(
#             file_path, bucket_name, "app.js", ExtraArgs={"ContentType": "text/javascript"}
#         )
#         print(f"File {file_path} uploaded as app.js.")
#     except ClientError as e:
#         print(f"Error uploading {file_path}: {e}")
#         exit(1)
# else:
#     print(f"File {file_path} does not exist.")
#     exit(1)

# # run app.js
# print("\nRunning app.js...")
# system("node app.js")




#CloudWatch alarms setup

print("Setting up CloudWatch alarms...")
cloudwatch = boto3.client("cloudwatch")

# CPU utilization greater than 50%
try:
    cloudwatch.put_metric_alarm(
        AlarmName="HighCPUUtilization",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=1,
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Period=60,
        Statistic="Average",
        Threshold=50.0,
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:automate:us-east-1:ec2:reboot",
        ],
        AlarmDescription="Alarm if server CPU utilization exceeds 50%",
        Dimensions=[
            {"Name": "InstanceId", "Value": new_ec2_instance[0].id},
        ],
        Unit="Percent",
    )
    print("High CPU utilization alarm created.")
except ClientError as e:
    print(f"Error creating high CPU utilization alarm: {e}")

# CPU utilization less than 30%
try:
    cloudwatch.put_metric_alarm(
        AlarmName="LowCPUUtilization",
        ComparisonOperator="LessThanThreshold",
        EvaluationPeriods=1,
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Period=60,
        Statistic="Average",
        Threshold=30.0,
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:automate:us-east-1:ec2:terminate",
        ],
        AlarmDescription="Alarm if server CPU utilization below 30%",
        Dimensions=[
            {"Name": "InstanceId", "Value": new_ec2_instance[0].id},
        ],
        Unit="Percent",
    )
    print("Low CPU utilization alarm created.")
except ClientError as e:
    print(f"Error creating low CPU utilization alarm: {e}")

try:
    # Describe alarms
    print("\nDescribing alarms...")
    response = cloudwatch.describe_alarms()
    for alarm in response["MetricAlarms"]:
        print(f"Alarm Name: {alarm['AlarmName']}")
        print(f"Alarm Description: {alarm['AlarmDescription']}")
        print(f"Alarm State: {alarm['StateValue']}")
        print(f"Alarm Actions: {alarm['AlarmActions']}")
        print(f"Alarm Comparison: {alarm['ComparisonOperator']}")
        print(f"Evaluation Periods: {alarm['EvaluationPeriods']}")
        print(f"Metric Name: {alarm['MetricName']}")
        print(f"Namespace: {alarm['Namespace']}")
        print(f"Period: {alarm['Period']}")
        print(f"Statistic: {alarm['Statistic']}")
        print(f"Threshold: {alarm['Threshold']}")
        print(f"Unit: {alarm['Unit']}")
        print("\n")
except ClientError as e:
    print(f"Error describing alarms: {e}")

# print("\n\nexiting...")
# time.sleep(1)
exit()
