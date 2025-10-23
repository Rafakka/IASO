from flask import Flask, request, jsonify
import time
import threading
from datetime import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    print(f"✅ Health check received at {datetime.now()}")
    return jsonify({
        "status": "healthy", 
        "service": "mock_kotlin_server",
        "timestamp": int(time.time() * 1000)
    })

@app.route('/api/sms/batch', methods=['POST'])
def mock_batch_sms():
    """Mock Kotlin server - simulates SMS sending"""
    print(f"\n🎯 BATCH REQUEST RECEIVED at {datetime.now()}")
    
    data = request.json
    contacts = data.get('contacts', [])
    
    print("="*60)
    print("📱 MOCK KOTLIN SERVER - BATCH SMS REQUEST")
    print("="*60)
    print(f"📨 Received {len(contacts)} contacts from Python:")
    
    for i, contact in enumerate(contacts, 1):
        print(f"   {i:2d}. {contact.get('name', 'No Name'):20} → {contact.get('phone', 'No Phone')}")
        if 'message' in contact:
            print(f"        💬 '{contact['message']}'")
    
    print("\n📲 Simulating SMS sending (2 seconds)...")
    time.sleep(2)  # Simulate SMS sending time
    
    # Create results
    results = []
    for i, contact in enumerate(contacts):
        # Alternate between success and failure for testing
        if i % 2 == 0:
            results.append({
                "status": "sent", 
                "error": None,
                "timestamp": int(time.time() * 1000)
            })
            print(f"   ✅ SMS sent to {contact.get('name', 'Unknown')}")
        else:
            results.append({
                "status": "failed",
                "error": "Mock: Simulated network failure",
                "timestamp": int(time.time() * 1000)
            })
            print(f"   ❌ SMS failed for {contact.get('name', 'Unknown')}")
    
    successful = len([r for r in results if r['status'] == 'sent'])
    failed = len([r for r in results if r['status'] == 'failed'])
    
    print(f"\n📊 BATCH COMPLETE: {successful} successful, {failed} failed")
    print("="*60)
    
    return jsonify({
        "results": results,
        "total": len(contacts),
        "successful": successful,
        "failed": failed,
        "batch_id": f"mock_batch_{int(time.time())}"
    })

@app.route('/api/sms/send', methods=['POST'])
def mock_single_sms():
    """Mock single SMS endpoint"""
    data = request.json
    print(f"📱 Single SMS to {data.get('name')} at {data.get('phone')}")
    
    return jsonify({
        "status": "sent",
        "timestamp": int(time.time() * 1000)
    })

def start_server():
    print("🚀 STARTING MOCK KOTLIN SERVER")
    print("📍 http://localhost:8080")
    print("🔧 Available endpoints:")
    print("   - GET  /health")
    print("   - POST /api/sms/send") 
    print("   - POST /api/sms/batch")
    print("="*50)
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

if __name__ == '__main__':
    start_server()