# test_email_fixed.py
from dotenv import load_dotenv  # ADD THIS
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables FIRST
load_dotenv()

def test_email_basic():
    """Test basic email sending without the full system"""
    print("Testing basic email functionality...")
    
    # Get credentials
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD") 
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    print(f"Sender email: {sender_email}")
    print(f"Recipient email: {recipient_email}")
    print(f"Password configured: {'Yes' if sender_password else 'No'}")
    
    if not all([sender_email, sender_password, recipient_email]):
        print("ERROR: Missing email configuration")
        print("Please set environment variables:")
        print("  SENDER_EMAIL=your_gmail@gmail.com")
        print("  SENDER_PASSWORD=your_app_password")
        print("  RECIPIENT_EMAIL=your_phone_email@gmail.com")
        return False
    
    try:
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Trading System Test - {datetime.now().strftime('%H:%M:%S')}"
        
        body = f"""This is a test email from your Trading Signal System.

If you received this, email notifications are working correctly!

Test details:
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Sender: {sender_email}
- Recipient: {recipient_email}

Next step: Deploy your system to start receiving real trading signals.
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        print("Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("Logging in...")
        server.login(sender_email, sender_password)
        
        print("Sending test email...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("SUCCESS: Test email sent!")
        print(f"Check {recipient_email} inbox (including spam folder)")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("ERROR: SMTP Authentication failed")
        print(f"Details: {e}")
        print("Common fixes:")
        print("1. Verify your Gmail app password is correct (16 characters)")
        print("2. Ensure 2-factor authentication is enabled on Gmail")
        print("3. Generate a new app password if needed")
        print("4. Make sure you're using the app password, not your regular Gmail password")
        return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_email_with_fake_signal():
    """Test email with a fake trading signal using the actual system"""
    print("\nTesting email with fake trading signal...")
    
    # Import after loading env vars
    from strategies.base_strategy import Signal
    from notifications.email_notifier import EmailNotifier
    from config.settings import EmailConfig
    
    # Create fake signal
    fake_signal = Signal(
        strategy_name="TEST SYSTEM",
        symbol="SPY",
        signal_type="BUY_CROSS",
        confidence=85,
        timestamp=datetime.now(),
        current_price=475.25,
        sma_10=474.50,
        sma_50=472.80,
        distance_from_50sma=0.5,
        stop_loss=472.00,
        action="BUY SPY calls or UPRO shares - THIS IS A TEST",
        notes="TEST SIGNAL ONLY - Golden cross confirmed! This is a test of the notification system. Do not trade on this signal."
    )
    
    # Send via email notifier
    notifier = EmailNotifier(EmailConfig())
    
    print(f"Email config check:")
    print(f"  Sender: {notifier.config.sender_email}")
    print(f"  Recipient: {notifier.config.recipient_email}")
    print(f"  Password set: {'Yes' if notifier.config.sender_password else 'No'}")
    
    if not notifier.config.sender_email:
        print("ERROR: EmailConfig not loading environment variables")
        return False
    
    success = notifier.send_signals([fake_signal])
    
    if success:
        print("SUCCESS: Trading signal email sent!")
        print("Check your inbox for a properly formatted trading signal")
    else:
        print("FAILED: Could not send trading signal email")
    
    return success

if __name__ == "__main__":
    print("Testing email functionality with environment variables...")
    
    # Test 1: Basic email
    basic_success = test_email_basic()
    
    # Test 2: Trading signal format (if basic works)
    if basic_success:
        signal_success = test_email_with_fake_signal()
    else:
        print("\nSkipping signal test due to basic email failure")