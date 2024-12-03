import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from fastapi import HTTPException,status
from schemas.schemas import InvitePayload

def send_invitation_email(payload: InvitePayload, image_data: bytes, image_filename: str):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        server.login(sender_email,sender_password)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['Subject'] = "Invitation to Review API Documentation"
        
        body = f"""
        Dear Team,
        
        Please find below the details to review my solution for the provided task:
        
        - API Documentation (Redoc) : {payload.redoc_link}
        - Swagger Documentation : {payload.swagger_link}
        - Github Repository : {payload.github_code_link}
        
        Additionally I have attached the screenshot of GCP Firestore Database.
        
        Thanks and Best Regards,
        Soundarya G
        """
        
        msg.attach(MIMEText(body,"plain"))
        
        image = MIMEImage(image_data, name = image_filename)
        msg.attach(image)
        
        for recipient in payload.recipient_email:
            msg["To"] = recipient
            server.sendmail(sender_email, recipient, msg.as_string())
        
        server.quit()
        
        return {"message" : "Invitation email sent successfully"}
    
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to send invitation email")