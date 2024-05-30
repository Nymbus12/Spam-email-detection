import imaplib
import email
from email.header import decode_header

# Account credentials
username = "example@email.com"
password = "password"
imap_server = "imap.example.com"

def clean(text):
    # Clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def detect_spam(subject, sender):
    # basic spam logic
    spam_keywords = ["win", "free", "prize", "congratulation"] # will change later
    if any(keyword in subject.lower() for keyword in spam_keywords):
        return True
    
    spam_senders = ["noreply@", "info@", "newsletter@", "etcspamdomain.com"] # will more considered letter
    if any(sender_keyword in sender.lower() for sender_keyword in spam_senders):
        return True
    
    return False

# connect to the server and login
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, password)

# select mailbox that want to check
mail.select("inbox")

# search for all emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

for email_id in email_ids:
    # Fetch the email by ID
    res, msg = mail.fetch(email_id, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # Parse the email
            msg = email.message_from_bytes(response[1])
            subject, endcoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
                
            sender = msg.get("From")

            # Detect spam
            if detect_spam(subject, sender):
                print(f"Deleting spam email: Subject: {subject}, From: {sender}")
                mail.store(email_id, '+FLAGS', '\\Deleted')

            
        # Permanent remove emails masked for deletion
        mail.expunge()

        # Close the connection and logout
        mail.close()
        mail.logout()

