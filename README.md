# DevOps Automation Project – Assignment 2

**Author:** Michael McKibbin  
**Student ID:** 20092733  
**LinkedIn:** [michaelkevinmckibbin](https://www.linkedin.com/in/michaelkevinmckibbin)

## 📘 Overview

This project automates the provisioning and monitoring of a scalable web application infrastructure on AWS using Python and Bash. It was submitted as part of the DevOps module (26670, 2023–2024) for my BSc in Computer Science at SETU Waterford.

## 🚀 Features

- Launches EC2 instances using Boto3 (up to 3 in a single call)
- Installs Apache and hosts a dynamic `index.html` page with instance metadata
- Uploads and runs monitoring scripts (`monitor.sh` and `memv2.sh`) via SCP and SSH
- Deploys and starts a custom Node.js app (`app.js`)
- Sets up AWS CloudWatch alarms for auto-scaling based on CPU utilization
- Describes and outputs active alarms from CloudWatch

## 📁 File Descriptions

| File | Description |
|------|-------------|
| `devops_2.py` | Main Python script to automate EC2 provisioning, app deployment, and CloudWatch alarm setup. |
| `monitor.sh` | Bash script to extract and display EC2 instance status, Apache metrics, and system info. |
| `memv2.sh` | Bash script to push custom metrics (memory, connections, I/O wait) to AWS CloudWatch. |
| `Devops-Assignment-2-Report-mmckibbin-20092733.pdf` | Detailed PDF report documenting architecture, implementation, and testing. |
| `DevOps Assignment 2 Grading.xlsx` | Checklist used to ensure assignment met all required criteria. |

## 🛠️ Tools & Technologies

- **AWS EC2, CloudWatch, Auto Scaling**
- **Python 3**, **Boto3**
- **Bash scripting**
- **Apache HTTP Server**
- **Node.js**
- **AMI creation**
- **Custom monitoring metrics**

## 🖼️ Architecture

- **VPC with 3 Availability Zones**
- Public and private subnets
- Load Balancer and Auto Scaling Group
- Custom AMI for efficient scaling
- CloudWatch alarms: 
  - Scale out above 50% CPU
  - Scale in below 30% CPU

See the full diagram and deployment flow in the PDF report.

## 🧪 Testing

- Auto-scaling behavior tested using synthetic traffic (e.g. `curl` loops)
- Confirmed load balancer routing, CloudWatch triggering, and instance termination
- Verified monitoring output from `monitor.sh` and `memv2.sh`

## 📷 Screenshots

The report includes:
- Full VPC setup
- Load balancer and scaling screenshots
- Monitoring output and metrics visualizations

## 📜 License

This project was developed for academic purposes. Code and scripts may be reused for personal learning or non-commercial educational use with attribution.

---

**Michael McKibbin**  
BSc Computer Science (Computer Forensics & Security)  
AWS Cloud Practitioner | CompTIA Security+ | Oracle Java SE 7  
[GitHub](https://github.com/MichaelMcKibbin) | [LinkedIn](https://linkedin.com/in/michaelkevinmckibbin)
