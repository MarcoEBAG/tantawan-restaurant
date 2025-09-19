import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List
from models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        # Email configuration - can be set via environment variables
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.restaurant_email = os.environ.get('RESTAURANT_EMAIL', 'info@tantawan.ch')
        self.printer_email = os.environ.get('PRINTER_EMAIL', '')  # Email-to-print service
        
    def format_order_for_print(self, order: Order) -> str:
        """Format order for kitchen printing"""
        items_text = ""
        for item in order.items:
            items_text += f"- {item.quantity}x {item.name} (CHF {item.price:.2f})\n"
        
        pickup_time = order.pickup_time.strftime("%H:%M")
        pickup_date = order.pickup_time.strftime("%d.%m.%Y")
        
        order_text = f"""
=== NEUE BESTELLUNG ===
Bestellnummer: {order.order_number}
Datum: {pickup_date}
Abholzeit: {pickup_time}

KUNDE:
Name: {order.customer.name}
Telefon: {order.customer.phone}

BESTELLUNG:
{items_text}
TOTAL: CHF {order.total:.2f}

NOTIZEN:
{order.customer.notes or 'Keine Notizen'}

Status: {order.status.upper()}
Bestellt am: {order.created_at.strftime("%d.%m.%Y %H:%M")}

=== TANTAWAN RESTAURANT ===
        """.strip()
        
        return order_text
    
    def format_order_for_email(self, order: Order) -> str:
        """Format order for email notification"""
        items_html = ""
        for item in order.items:
            items_html += f"""
            <tr>
                <td>{item.name}</td>
                <td style="text-align: center;">{item.quantity}</td>
                <td style="text-align: right;">CHF {item.price:.2f}</td>
                <td style="text-align: right;">CHF {(item.price * item.quantity):.2f}</td>
            </tr>
            """
        
        pickup_time = order.pickup_time.strftime("%d.%m.%Y um %H:%M")
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .header {{ background-color: #ECEC75; padding: 20px; text-align: center; }}
                .order-info {{ background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-left: 4px solid #ECEC75; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; font-weight: bold; }}
                .total {{ background-color: #ECEC75; font-weight: bold; }}
                .notes {{ background-color: #fff3cd; padding: 15px; margin: 20px 0; border: 1px solid #ffeeba; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🍜 Neue Bestellung bei Tantawan</h1>
                <h2>Bestellnummer: {order.order_number}</h2>
            </div>
            
            <div class="order-info">
                <h3>📋 Bestellinformationen</h3>
                <p><strong>Kunde:</strong> {order.customer.name}</p>
                <p><strong>Telefon:</strong> {order.customer.phone}</p>
                <p><strong>Abholzeit:</strong> {pickup_time}</p>
                <p><strong>Status:</strong> <span style="color: #dc3545; font-weight: bold;">{order.status.upper()}</span></p>
            </div>
            
            <h3>🍴 Bestellte Gerichte</h3>
            <table>
                <thead>
                    <tr>
                        <th>Gericht</th>
                        <th style="text-align: center;">Menge</th>
                        <th style="text-align: right;">Preis</th>
                        <th style="text-align: right;">Gesamt</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                    <tr class="total">
                        <td colspan="3" style="text-align: right;"><strong>GESAMT:</strong></td>
                        <td style="text-align: right;"><strong>CHF {order.total:.2f}</strong></td>
                    </tr>
                </tbody>
            </table>
            
            {f'<div class="notes"><h3>📝 Notizen</h3><p>{order.customer.notes}</p></div>' if order.customer.notes else ''}
            
            <hr>
            <p style="text-align: center; color: #666; font-size: 12px;">
                Bestellt am {order.created_at.strftime("%d.%m.%Y um %H:%M")} Uhr<br>
                Tantawan Restaurant - Zürcherstrasse 232, Frauenfeld
            </p>
        </body>
        </html>
        """
        
        return html_content
    
    async def send_order_notification(self, order: Order) -> bool:
        """Send order notification email to restaurant"""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured, skipping email notification")
                return False
                
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'🍴 Neue Bestellung #{order.order_number} - Tantawan'
            msg['From'] = self.smtp_username
            msg['To'] = self.restaurant_email
            
            # Plain text version
            text_content = self.format_order_for_print(order)
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            
            # HTML version
            html_content = self.format_order_for_email(order)
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Order notification email sent successfully for order {order.order_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send order notification email: {str(e)}")
            return False
    
    async def send_order_to_printer(self, order: Order) -> bool:
        """Send order to printer via email-to-print service"""
        try:
            if not self.printer_email or not self.smtp_username:
                logger.warning("Printer email not configured, skipping print")
                return False
                
            msg = MIMEText(self.format_order_for_print(order), 'plain', 'utf-8')
            msg['Subject'] = f'PRINT: Bestellung #{order.order_number}'
            msg['From'] = self.smtp_username
            msg['To'] = self.printer_email
            
            # Send to printer
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Order sent to printer successfully for order {order.order_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send order to printer: {str(e)}")
            return False


# Global email service instance
email_service = EmailService()