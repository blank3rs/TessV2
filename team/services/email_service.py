import os
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def read_emails(email_provider="gmail", folder="inbox", limit=5) -> str:
    """Read recent emails from the specified folder"""
    try:
        # Get email credentials based on provider
        if email_provider.lower() == "gmail":
            email_address = os.getenv("GMAIL_ADDRESS")
            email_password = os.getenv("GMAIL_PASSWORD")
            imap_server = "imap.gmail.com"
        elif email_provider.lower() == "outlook":
            email_address = os.getenv("OUTLOOK_ADDRESS")
            email_password = os.getenv("OUTLOOK_PASSWORD")
            imap_server = "outlook.office365.com"
        else:
            return f"Unsupported email provider: {email_provider}"
        
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        
        # Select the folder (mailbox)
        mail.select(folder)
        
        # Search for all emails and get the latest ones
        _, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        latest_emails = email_ids[-limit:] if len(email_ids) > limit else email_ids
        
        email_list = []
        for email_id in reversed(latest_emails):
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            message = email.message_from_bytes(email_body)
            
            subject = message["subject"]
            sender = message["from"]
            date = message["date"]
            
            email_list.append(f"From: {sender}\nSubject: {subject}\nDate: {date}\n")
        
        mail.close()
        mail.logout()
        
        return "\n".join(email_list) if email_list else "No emails found"
    except Exception as e:
        return f"Error reading emails: {str(e)}"

def send_email(to: str, subject: str, body: str, email_provider="gmail") -> str:
    """Send an email"""
    try:
        # Get email credentials based on provider
        if email_provider.lower() == "gmail":
            email_address = os.getenv("GMAIL_ADDRESS")
            email_password = os.getenv("GMAIL_PASSWORD")
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
        elif email_provider.lower() == "outlook":
            email_address = os.getenv("OUTLOOK_ADDRESS")
            email_password = os.getenv("OUTLOOK_PASSWORD")
            smtp_server = "smtp.office365.com"
            smtp_port = 587
        else:
            return f"Unsupported email provider: {email_provider}"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return f"Email sent successfully to {to} using {email_provider}"
    except Exception as e:
        return f"Error sending email: {str(e)}" 