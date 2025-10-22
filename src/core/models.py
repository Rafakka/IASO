from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Contact:
    name: str
    phone: str
    message: str
    message_type: str = "SMS"  # SMS, WHATSAPP, CALL
    
@dataclass
class ProcessingResult:
    contact: Contact
    status: str  # "pending", "sent", "failed"
    timestamp: datetime
    error_message: Optional[str] = None
    
@dataclass
class BatchResult:
    batch_id: str
    total_contacts: int
    successful: int
    failed: int
    results: List[ProcessingResult]
    processing_time: float