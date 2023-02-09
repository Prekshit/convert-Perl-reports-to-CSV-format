import csv
import email
import imaplib
import smtplib
import time
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

def convert_perl_to_csv(perl_report):
    # Convert Perl report to list of lists (rows and columns)
    report_lines = perl_report.strip().split("\n")
    report_data = [line.split() for line in report_lines]

    # Write report data to CSV file
    csv_file = "report.csv"
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(report_data)

    return csv_file

def send_email(sender_email, sender_password, recipient_email, csv_file):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Perl Report"
    message.attach(MIMEText("Attached is the converted Perl report in CSV format."))

    with open(csv_file, "rb") as file:
        payload = MIMEBase('application', "octet-stream")
        payload.set_payload((file.read()))
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', "attachment", filename=csv_file)
        message.attach(payload)

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email, recipient_email, message.as_string())
    smtp.quit()

if __name__ == "__main__":
    # Login credentials for sender email
    sender_email = "sender_email@gmail.com"
    sender_password = "sender_password"

    # Email address to send the converted report
    recipient_email = "recipient_email@gmail.com"

    # Connect to the IMAP server and select the inbox
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(sender_email, sender_password)
    mail.select("inbox")

    while True:
        # Search for email from specific sender
        status, email_ids = mail.search(None, '(FROM "specific_sender@example.com")')
        email_ids = email_ids[0].split()

        # Loop through each email
        for email_id in email_ids:
            # Fetch the email
            status, email_data = mail.fetch(email_id, "(RFC822)")
            email_body = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(email_body)

            # Loop through each
