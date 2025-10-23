from typing import Tuple, List, Dict
from datetime import datetime
import time
from ..core.models import Contact, ProcessingResult, BatchResult
from ..core.api_client import KotlinGatewayClient
from ..core.excel_processor import ExcelProcessor
from ..utils.logger import get_logger

class BatchProcessor:
    def __init__(self, gateway_url: str = "http://localhost:8080"):
        self.excel_processor = ExcelProcessor()
        self.api_client = KotlinGatewayClient(gateway_url)
        self.logger = get_logger(__name__)
    
    def process_excel_file(self, excel_file_path: str) -> Tuple[BatchResult, List[Dict]]:
        """Process Excel file and return both results and validation errors"""
        start_time = time.time()
        batch_id = f"batch_{int(datetime.now().timestamp())}"
        
        self.logger.info(f"Starting batch {batch_id} with file: {excel_file_path}")
        
        try:
            valid_contacts, validation_errors = self.excel_processor.load_contacts_from_excel(excel_file_path)
            
            self.logger.info(f"Loaded {len(valid_contacts)} valid contacts, {len(validation_errors)} validation errors")
            
            for error in validation_errors:
                self.logger.warning(f"Row {error['row_index']} - {error['name']}: {error['error']}")
            
            if not self.api_client.health_check():
                raise Exception("Kotlin gateway is not available. Please ensure the mobile app is running.")
            
            if valid_contacts:
                processing_results = self.api_client.send_batch_sms(valid_contacts)
            else:
                processing_results = []
                self.logger.warning("No valid contacts to process")
            
            successful = len([r for r in processing_results if r.status == "sent"])
            failed = len([r for r in processing_results if r.status == "failed"])
            
            processing_time = time.time() - start_time
            
            batch_result = BatchResult(
                batch_id=batch_id,
                total_contacts=len(valid_contacts),
                successful=successful,
                failed=failed,
                results=processing_results,
                processing_time=processing_time
            )
            
            self.logger.info(f"Batch {batch_id} completed: {successful} successful, {failed} failed, {len(validation_errors)} validation errors")
            
            return batch_result, validation_errors
            
        except Exception as e:
            self.logger.error(f"Batch {batch_id} failed: {str(e)}")
            raise