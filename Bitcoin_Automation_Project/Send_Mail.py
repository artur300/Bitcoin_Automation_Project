import smtplib
import os
import logging
from email.message import EmailMessage


# Retrieves the email application's password from an environment variable for secure access.
EMAIL_APP_PASSWORD = os.environ.get('MAIL_APP_PASS')

# Creates an email message with the maximum Bitcoin price and the time it occurred.
# The message includes a subject, sender, recipient, and a formatted text body.
# Returns the complete EmailMessage object ready to be sent.
def create_email_message(max_price, max_time):
    logging.info('Creating email message with max price and timestamp...')

    msg = EmailMessage()
    msg['Subject'] = 'Bitcoin Info'
    msg['From'] = 'arturaniki@gmail.com'
    msg['To'] = 'arturaniki@gmail.com'

    formatted_time = max_time.strftime('%Y-%m-%d %H:%M:%S')
    msg.set_content(
        f'The maximum Bitcoin price in the last hour was: ${max_price:,.2f}\n'
        f'Time it occurred (Israel time): {formatted_time}\n\n'
        f'See the graph attached.'
    )

    logging.info('Email message created successfully.')
    return msg


# Attaches a PNG graph image file to the provided EmailMessage object.
# If the file is not found, logs an error and raises the exception.
def attach_graph_to_email(msg, filename='btc_price_graph.png'):
    logging.info(f'Attaching graph image to email: {filename}')
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            msg.add_attachment(
                file_data,
                maintype='image',
                subtype='png',
                filename=filename
            )
            logging.info('Graph image attached to email successfully.')
    except FileNotFoundError:
        logging.error('Graph image file not found.')
        raise




# Sends an email containing the maximum Bitcoin price and a graph attachment.
# Handles authentication errors, missing attachment files, and general exceptions with logging.
def send_email(max_price, max_time):
    logging.info('Preparing to send email with Bitcoin report...')
    try:
        msg = create_email_message(max_price, max_time)
        attach_graph_to_email(msg)

        logging.info('Connecting to Gmail SMTP server...')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('arturaniki@gmail.com', EMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        logging.info('Email sent successfully.')

    except smtplib.SMTPAuthenticationError:
        logging.error('Authentication failed. Please check your email or app password.')
    except FileNotFoundError:
        logging.error('Attachment file missing, email not sent.')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

