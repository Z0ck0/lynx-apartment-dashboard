"""
Export Helpers for Lynx Apartment Dashboard Reports

This module provides functions and documentation for exporting reports
as PDF, saving to Google Drive, and sending via email.

IMPORTANT: These are implementation stubs. Full integration requires
additional setup and API credentials.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st


# ========== PDF EXPORT ==========

def export_report_to_pdf(
    report_html: str,
    output_path: Optional[Path] = None,
    template_name: str = "report",
) -> Optional[bytes]:
    """
    Export a report HTML string to PDF.
    
    IMPLEMENTATION OPTIONS:
    
    Option 1: Using xhtml2pdf (Recommended for HTML to PDF)
    ------------------------
    Install: pip install xhtml2pdf
    
    from xhtml2pdf import pisa
    
    def export_report_to_pdf(report_html: str, output_path: Path) -> bytes:
        result_file = open(output_path, "w+b")
        pisa_status = pisa.CreatePDF(
            report_html,
            dest=result_file,
        )
        result_file.close()
        if pisa_status.err:
            raise Exception("PDF generation failed")
        return open(output_path, "rb").read()
    
    Option 2: Using reportlab (More control, but requires manual layout)
    ---------------------------
    Install: pip install reportlab
    
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    def export_report_to_pdf(metrics: Dict, output_path: Path) -> bytes:
        c = canvas.Canvas(str(output_path), pagesize=letter)
        # Manually add text, charts, etc.
        c.save()
        return open(output_path, "rb").read()
    
    Option 3: Using weasyprint (Best HTML/CSS support)
    ---------------------------
    Install: pip install weasyprint
    
    from weasyprint import HTML
    
    def export_report_to_pdf(report_html: str, output_path: Path) -> bytes:
        HTML(string=report_html).write_pdf(output_path)
        return open(output_path, "rb").read()
    
    Option 4: Using pdfkit (Requires wkhtmltopdf binary)
    ---------------------------
    Install: pip install pdfkit
    Also install: wkhtmltopdf binary (system dependency)
    
    import pdfkit
    
    def export_report_to_pdf(report_html: str, output_path: Path) -> bytes:
        pdfkit.from_string(report_html, str(output_path))
        return open(output_path, "rb").read()
    
    RECOMMENDED: Use weasyprint for best HTML/CSS support, or xhtml2pdf
    for simpler setup.
    """
    st.warning("PDF export not yet implemented. See export_helpers.py for implementation options.")
    return None


def generate_report_html(
    template: Dict[str, Any],
    metric_info: Dict[str, Dict],
    filter_params: Dict[str, Any],
    generated_time: str,
) -> str:
    """
    Generate HTML representation of a report for PDF export.
    
    This function should convert the Streamlit report into HTML
    that can be converted to PDF.
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{template['name']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .metric-card {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; }}
            .metric-label {{ font-size: 0.9em; color: #666; }}
            .metric-value {{ font-size: 1.5em; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>{template['name']}</h1>
        <p>Generated: {generated_time}</p>
        <h2>Key Metrics</h2>
    """
    
    for metric_key in template.get('metrics', []):
        if metric_key in metric_info:
            mi = metric_info[metric_key]
            html += f"""
            <div class="metric-card">
                <div class="metric-label">{mi['label']}</div>
                <div class="metric-value">{mi['prefix']}{mi['value']}</div>
                <div class="metric-explanation">{mi['explanation']}</div>
            </div>
            """
    
    html += """
    </body>
    </html>
    """
    
    return html


# ========== GOOGLE DRIVE EXPORT ==========

def save_to_google_drive(
    file_path: Path,
    folder_name: str = "Lynx Reports",
    file_name: Optional[str] = None,
) -> Optional[str]:
    """
    Upload a file to Google Drive.
    
    IMPLEMENTATION REQUIREMENTS:
    ----------------------------
    1. Install required packages:
       pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    
    2. Set up Google Cloud Project:
       - Go to https://console.cloud.google.com/
       - Create a new project or select existing
       - Enable Google Drive API
       - Create OAuth 2.0 credentials (Desktop app)
       - Download credentials JSON file
    
    3. Store credentials:
       - Save credentials JSON as 'google_drive_credentials.json' in app directory
       - Or use environment variables for production
    
    4. Implementation example:
    
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import os
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def get_drive_service():
        creds = None
        token_file = 'token.json'
        
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_drive_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        return build('drive', 'v3', credentials=creds)
    
    def save_to_google_drive(file_path: Path, folder_name: str = "Lynx Reports"):
        service = get_drive_service()
        
        # Find or create folder
        folder_id = None
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query).execute()
        items = results.get('files', [])
        
        if items:
            folder_id = items[0]['id']
        else:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            folder_id = folder.get('id')
        
        # Upload file
        file_metadata = {'name': file_path.name, 'parents': [folder_id]}
        media = MediaFileUpload(str(file_path), mimetype='application/pdf')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return file.get('id')
    
    ALTERNATIVE: Use Streamlit Secrets for credentials:
    - Store credentials in .streamlit/secrets.toml
    - Access via st.secrets["google_drive"]
    """
    st.warning("Google Drive integration not configured. See export_helpers.py for setup instructions.")
    return None


# ========== EMAIL EXPORT ==========

def send_report_via_email(
    file_path: Path,
    recipient_email: str,
    subject: str = "Lynx Apartment Report",
    body: str = "Please find attached the requested report.",
) -> bool:
    """
    Send a report file via email.
    
    IMPLEMENTATION OPTIONS:
    -----------------------
    
    Option 1: SMTP (Gmail, Outlook, etc.)
    ------------------------
    Requires: smtplib (built-in), email (built-in)
    
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    def send_report_via_email(file_path: Path, recipient_email: str):
        # Configuration (store in Streamlit secrets)
        smtp_server = st.secrets["email"]["smtp_server"]  # e.g., "smtp.gmail.com"
        smtp_port = st.secrets["email"]["smtp_port"]  # e.g., 587
        sender_email = st.secrets["email"]["sender_email"]
        sender_password = st.secrets["email"]["sender_password"]  # App password for Gmail
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {file_path.name}',
        )
        msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True
    
    Option 2: SendGrid API (More reliable, requires API key)
    ------------------------
    Install: pip install sendgrid
    
    import sendgrid
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
    
    def send_report_via_email(file_path: Path, recipient_email: str):
        sg = sendgrid.SendGridAPIClient(api_key=st.secrets["sendgrid"]["api_key"])
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encoded_file = base64.b64encode(data).decode()
        
        attached_file = Attachment(
            FileContent(encoded_file),
            FileName(file_path.name),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        
        message = Mail(
            from_email=st.secrets["sendgrid"]["from_email"],
            to_emails=recipient_email,
            subject=subject,
            html_content=body
        )
        message.attachment = attached_file
        
        response = sg.send(message)
        return response.status_code == 202
    
    Option 3: AWS SES (For production apps)
    ------------------------
    Install: pip install boto3
    
    import boto3
    from botocore.exceptions import ClientError
    
    def send_report_via_email(file_path: Path, recipient_email: str):
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=st.secrets["aws"]["access_key"],
            aws_secret_access_key=st.secrets["aws"]["secret_key"],
            region_name=st.secrets["aws"]["region"]
        )
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        try:
            response = ses_client.send_raw_email(
                Source=st.secrets["aws"]["from_email"],
                Destinations=[recipient_email],
                RawMessage={'Data': create_email_with_attachment(...)}
            )
            return True
        except ClientError as e:
            st.error(f"Email sending failed: {e}")
            return False
    
    RECOMMENDED: Use SendGrid for production, SMTP for simple setups.
    """
    st.warning("Email integration not configured. See export_helpers.py for implementation options.")
    return False


# ========== STREAMLIT SECRETS CONFIGURATION ==========

"""
To configure email/Google Drive, create a .streamlit/secrets.toml file:

# Email Configuration (SMTP)
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"  # Use App Password for Gmail

# Or SendGrid
[sendgrid]
api_key = "your-sendgrid-api-key"
from_email = "your-email@example.com"

# Google Drive (store credentials JSON path)
[google_drive]
credentials_path = "google_drive_credentials.json"

# AWS SES (if using)
[aws]
access_key = "your-access-key"
secret_key = "your-secret-key"
region = "us-east-1"
from_email = "your-email@example.com"
"""

