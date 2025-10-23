import requests
import time

def test_kotlin_connection():
    print("🔍 Testing connection to Kotlin server...")
    
    try:
        # Test basic connection
        response = requests.get("http://localhost:8080/health", timeout=5)
        print(f"✅ Connection successful! Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server not running or wrong port")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout - server not responding")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_kotlin_connection()