import os
import sys
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv 

load_dotenv() 

def send_email():
    """Función que envía el correo utilizando las variables de entorno."""
    sender_email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    
    if not sender_email or not password or not receiver_email:
        print("Error: Faltan las variables de entorno necesarias.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = "Recordatorio de Proyecto"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
Hola Juan,

Este es tu recordatorio programado para revisar el proyecto.

¡Ánimo y sigue adelante!
"""
    message.attach(MIMEText(text, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def run_scheduler():
    """Ejecuta el scheduler para pruebas locales o desarrollo."""
    # Ejemplo: programar envío cada minuto para pruebas
    schedule.every(1).minutes.do(send_email)
    
    print("Iniciando scheduler. Presiona Ctrl+C para detener.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Revisa cada 60 segundos
    except KeyboardInterrupt:
        print("Scheduler detenido.")

if __name__ == "__main__":
    # Si se pasa el argumento '--send-email', ejecuta solo la función de envío y termina.
    if "--send-email" in sys.argv:
        send_email()
    else:
        # Para desarrollo o pruebas locales, se puede ejecutar el scheduler.
        run_scheduler()
