from __future__ import print_function

from dotenv import load_dotenv
import os, requests

load_dotenv()


class EmailClient:
    def __init__(
        self,
        sender_email,
        sender_name,
        to_email,
        to_name,
        cc_email,
        cc_name,
        bcc_email,
        bcc_name,
        reply_to_email,
        reply_to_name,
        html_content,
        subject,
    ):
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.to_email = to_email
        self.to_name = to_name
        self.cc_email = cc_email
        self.cc_name = cc_name
        self.bcc_email = bcc_email
        self.bcc_name = bcc_name
        self.reply_to_email = reply_to_email
        self.reply_to_name = reply_to_name
        self.html_content = html_content
        self.subject = subject

    def send_email(self):
        # Call the email service using the requests library
        # Define the endpoint
        endpoint = (
            f"{os.getenv('EMAIL_SVC_URL')}:{os.getenv('EMAIL_SVC_PORT')}/send_email"
        )
        # Define the payload
        payload = {
            "sender_email": self.sender_email,
            "sender_name": self.sender_name,
            "to_email": self.to_email,
            "to_name": self.to_name,
            "cc_email": self.cc_email,
            "cc_name": self.cc_name,
            "bcc_email": self.bcc_email,
            "bcc_name": self.bcc_name,
            "reply_to_email": self.reply_to_email,
            "reply_to_name": self.reply_to_name,
            "html_content": self.html_content,
            "subject": self.subject,
        }
        # Make the request in a try catch
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            # Now check the response status code
            if response.status_code == 200:
                print("Email sent successfully!")
        except requests.exceptions.HTTPError as err:
            print(f"Error sending email: {err}")
            raise err


def create_email_from_post(post, origin):
    title = post["title"]
    url = post["url"]
    text = post["text"]
    title_entities = post["title_entities"] if post["title_entities"] else []
    text_entities = post["text_entities"] if post["text_entities"] else []

    html_content = f"""
        <h2><a href="{url}">{title}</a></h2>
        <p>Tags: {", ".join(title_entities)}</p>
        <p style="margin-left: 40px; font-style: italic;">{text}</p>
    """
    return html_content


def inform_user_of_latest_posts(posts, origin):
    html_contents = []
    for post in posts:
        html_content = create_email_from_post(post, origin)
        html_contents.append(html_content)

    html_content = "\n".join(html_contents)
    title = f"<h1>Your Latest Posts from {origin}</h1>"

    html_content = f"<html><b ody>{title}\n{html_content}</body></html>"
    subject = f"Your Latest Posts from {origin}"

    # Check if the required environment variables are set - if not raise an error
    if (
        not os.getenv("SENDER_EMAIL")
        or not os.getenv("SENDER_NAME")
        or not os.getenv("TO_EMAIL")
        or not os.getenv("TO_NAME")
        or not os.getenv("REPLY_TO_EMAIL")
        or not os.getenv("REPLY_TO_NAME")
    ):
        raise ValueError("Required environment variables are not set!")

    # TODO: Send email using email svc
    email_client = EmailClient(
        sender_email=os.getenv("SENDER_EMAIL"),
        sender_name=os.getenv("SENDER_NAME"),
        to_email=os.getenv("TO_EMAIL"),
        to_name=os.getenv("TO_NAME"),
        cc_email=os.getenv("CC_EMAIL") if os.getenv("CC_EMAIL") else None,
        cc_name=os.getenv("CC_NAME") if os.getenv("CC_NAME") else None,
        bcc_email=os.getenv("BCC_EMAIL") if os.getenv("BCC_EMAIL") else None,
        bcc_name=os.getenv("BCC_NAME") if os.getenv("BCC_NAME") else None,
        reply_to_email=os.getenv("REPLY_TO_EMAIL"),
        reply_to_name=os.getenv("REPLY_TO_NAME"),
        html_content=html_content,
        subject=subject,
    )
    try:
        email_client.send_email()
    except Exception as e:
        print(f"Error sending email: {str(e)}")
