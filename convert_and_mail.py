import csv
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Set the recipient email address
recipient_email = "recipient@example.com"

# Set the sender email address and password
sender_email = "sender@example.com"
sender_password = "sender_email_password"

# Run the Perl script to generate the report
perl_script = "perl_script.pl"
subprocess.call([perl_script])

# Read the Perl report file and convert it to CSV format
perl_report_file = "perl_report.txt"
csv_file = "perl_report.csv"
with open(perl_report_file, 'r') as file:
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for line in file:
            csv_writer.writerow(line.strip().split("\t"))

# Set up the email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = "Perl Report Converted to CSV"

# Attach the CSV file to the email
with open(csv_file, "rb") as f:
    payload = MIMEBase('application', 'octet-stream', Name=csv_file)
    payload.set_payload((f.read()))
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=csv_file)
    message.attach(payload)

# Send the email
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, sender_password)
server.sendmail(sender_email, recipient_email, message.as_string())
server.quit()

print("Perl report converted to CSV and sent to the recipient email successfully!")
