from typing import List
from .function import Parameter
from .function import Function
import sendgrid
import os
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Mail(Function):
    mail: sendgrid.SendGridAPIClient
    cloudinary: cloudinary.config

    def __init__(self) -> None:
        self.mail = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))
        self.cloudinary = cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )

    @property
    def name(self) -> str:
        return 'mail_sender'

    @property
    def description(self) -> str:
        return 'Takes subject, body of a mail, recipient mail, imagepath in json format as ```{"subject": "Test Subject", "body": "Test body of mail", "to": "example@gmail.com", "image": "figure_name.jpeg"}```, image path can be an empty string if image doesnt exist. Returns the response after sending.'

    @property
    def parameters(self) -> List[Parameter]:
        return [
            Parameter(
                name="subject",
                param_type="string",
                description="Subject of the mail that you want to send.",
                required=True,
            ),
            Parameter(
                name="body",
                param_type="string",
                description="HTML Body of the mail that you want to send.",
                required=True,
            ),
            Parameter(
                name="recipient",
                param_type="string",
                description="Mail id of the recipient.",
                required=True,
            ),
        ]

    def execute(self, input: str) -> str:
        json_data = json.loads(input)
        recipient = json_data['to']
        subject = json_data['subject']
        body = json_data['body']
        image_path = json_data['image']
        image_tag = ""
        if(image_path != ""):
            cloudinary.uploader.upload(image_path, public_id = 'figure_name')
            image_url = cloudinary.utils.cloudinary_url('figure_name')[0]
            image_tag = "<img src='{}'>".format(image_url)
        
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": recipient
                        }
                    ],
                    "subject": subject
                }
            ],
            "from": {
                "email": os.environ.get('MAIL')
            },
            "content": [
                {
                    "type": "text/html",
                    "value": "<html><p>"+body+"</p>{}</html>".format(image_tag)
                }
            ]
        }

        response = self.mail.client.mail.send.post(request_body=data)

        if str(response.status_code)[0] != '2':
            return "Mail not sent. Please try again later."
        
        return "Mail sent successfully!"