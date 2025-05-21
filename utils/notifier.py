import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import EMAIL_SENDER, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT, SMTP_PASSWORD
from config import DATA_DIR, TIMESTAMP


class EmailNotifier:
    def __init__(self):
        self.sender = EMAIL_SENDER
        self.receiver = EMAIL_RECEIVER
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.password = SMTP_PASSWORD

    def send(self, changed_domains: list[str]):
        subject = f"Cambios detectados en dominios – {TIMESTAMP.replace('_', ' ')}"
        message = MIMEMultipart("related")
        message["From"] = self.sender
        message["To"] = self.receiver
        message["Subject"] = subject

        # HTML base
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <h2 style="color: #333;">Cambios detectados en los siguientes dominios:</h2>
        <ul style="list-style-type: disc; padding: 0;">
        """

        cid_map = {}

        for i, domain in enumerate(changed_domains):
            domain_clean = domain.replace("https://", "").replace("http://", "").replace("/", "_")
            diff_path = DATA_DIR / domain_clean / TIMESTAMP / "diff.png"
            cid = f"image{i}"
            cid_map[diff_path] = cid

            html += f"""
            <li style="margin-bottom: 30px;">
                <h3 style="color: #007BFF;">{domain}</h3>
                <img src="cid:{cid}" style="max-width: 600px; border: 2px solid #ddd; border-radius: 8px;">
            </li>
            """

        html += """
        </ul>
        <p style="color: #888; font-size: 12px;">Resumen automatizado del escaneo de cambios.</p>
        </body>
        </html>
        """

        message.attach(MIMEText(html, "html"))

        # Adjuntar las imágenes embebidas
        for diff_path, cid in cid_map.items():
            if diff_path.exists():
                with open(diff_path, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", f"<{cid}>")
                    img.add_header("Content-Disposition", "inline", filename=diff_path.name)
                    message.attach(img)

        # Enviar correo
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receiver, message.as_string())
                print(f"📧 Correo enviado a {self.receiver} con imágenes embebidas")
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")
