import sys
import os

# Add the src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.api_client import KotlinGatewayClient

def manual_test():
    print("🔍 Manual API Client Test")
    
    client = KotlinGatewayClient("http://localhost:8080")
    
    # Test health check
    print("1. Testing health check...")
    healthy = client.health_check()
    print(f"   Health check: {'✅ SUCCESS' if healthy else '❌ FAILED'}")
    
    if healthy:
        # Test sending a single SMS
        from core.models import Contact
        print("2. Testing single SMS...")
        contact = Contact("Test User", "11 - 9999 - 9999", "Test message")
        result = client.send_sms(contact)
        print(f"   Single SMS: {result.status} - {result.error_message}")
        
        # Test batch SMS
        print("3. Testing batch SMS...")
        contacts = [
            Contact("User 1", "11 - 9999 - 9999", "Message 1"),
            Contact("User 2", "11 - 8888 - 8888", "Message 2"),
        ]
        results = client.send_batch_sms(contacts)
        print(f"   Batch SMS: {len(results)} results")
        for r in results:
            print(f"     - {r.contact.name}: {r.status}")

if __name__ == "__main__":
    manual_test()