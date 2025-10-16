from dotenv import load_dotenv
import os

def test_env_loading():
    """Test if environment variables are loading correctly"""
    
    # Load the .env file
    load_dotenv()
    
    print("Environment Variable Test")
    print("=" * 40)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ .env file found")
        
        # Read and display .env contents (safely)
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        print(f"✓ .env file has {len(lines)} lines")
        
        # Check for required variables
        for line in lines:
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0]
                print(f"  Found variable: {key}")
    else:
        print("✗ .env file NOT found")
        print("  Create .env file in project root directory")
        return False
    
    # Test loading variables
    print("\nLoaded Environment Variables:")
    print("-" * 40)
    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    print(f"SENDER_EMAIL: {sender_email or 'NOT SET'}")
    print(f"SENDER_PASSWORD: {'SET' if sender_password else 'NOT SET'}")
    print(f"RECIPIENT_EMAIL: {recipient_email or 'NOT SET'}")
    
    # Validate
    if all([sender_email, sender_password, recipient_email]):
        print("\n✓ All required variables are set!")
        return True
    else:
        print("\n✗ Missing required variables")
        print("\nYour .env file should contain:")
        print("SENDER_EMAIL=your_gmail@gmail.com")
        print("SENDER_PASSWORD=your_16_char_app_password")
        print("RECIPIENT_EMAIL=your_phone_email@gmail.com")
        return False

if __name__ == "__main__":
    test_env_loading()
