import requests
from typing import Dict, Any, Optional
from .models import Contact, ProcessingResult
import json
from datetime import datetime

class KotlinGatewayClient:
    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
    def health_check(self) -> bool:
        """Check if Kotlin gateway is available"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def send_sms(self, contact: Contact) -> ProcessingResult:
        """Send single SMS via Kotlin gateway"""
        try:
            payload = {
                "phone": contact.phone,
                "message": contact.message,
                "name": contact.name
            }
            
            response = self.session.post(
                f"{self.base_url}/api/sms/send",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return ProcessingResult(
                    contact=contact,
                    status="sent",
                    timestamp=datetime.now()
                )
            else:
                return ProcessingResult(
                    contact=contact,
                    status="failed",
                    timestamp=datetime.now(),
                    error_message=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return ProcessingResult(
                contact=contact,
                status="failed", 
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def send_batch_sms(self, contacts: List[Contact]) -> List[ProcessingResult]:
        """Send batch SMS via Kotlin gateway"""
        try:
            payload = {
                "contacts": [
                    {
                        "name": contact.name,
                        "phone": contact.phone, 
                        "message": contact.message
                    }
                    for contact in contacts
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/sms/batch",
                json=payload,
                timeout=self.timeout * 2  # Longer timeout for batches
            )
            
            if response.status_code == 200:
                # Parse batch response
                results = []
                response_data = response.json()
                
                for i, contact in enumerate(contacts):
                    result_status = response_data.get('results', [{}] * len(contacts))[i]
                    results.append(ProcessingResult(
                        contact=contact,
                        status=result_status.get('status', 'unknown'),
                        timestamp=datetime.now(),
                        error_message=result_status.get('error')
                    ))
                
                return results
            else:
                # If batch fails, mark all as failed
                return [
                    ProcessingResult(
                        contact=contact,
                        status="failed",
                        timestamp=datetime.now(),
                        error_message=f"Batch failed: HTTP {response.status_code}"
                    )
                    for contact in contacts
                ]
                
        except Exception as e:
            return [
                ProcessingResult(
                    contact=contact,
                    status="failed",
                    timestamp=datetime.now(),
                    error_message=str(e)
                )
                for contact in contacts
            ]