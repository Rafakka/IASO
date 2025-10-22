import argparse
import sys
from services.batch_processor import BatchProcessor
from utils.config import Config
from utils.logger import get_logger

def main():
    parser = argparse.ArgumentParser(description='SMS Automation Backend')
    parser.add_argument('excel_file', help='Path to Excel file with contacts')
    parser.add_argument('--config', '-c', default='config.yaml', help='Path to config file')
    
    args = parser.parse_args()
    
    # Initialize
    config = Config(args.config)
    logger = get_logger("main")
    
    try:
        # Create processor
        processor = BatchProcessor(
            gateway_url=config.get('gateway.base_url')
        )
        
        # Process the file
        result = processor.process_excel_file(args.excel_file)
        
        # Display results
        print(f"\n=== BATCH PROCESSING COMPLETED ===")
        print(f"Batch ID: {result.batch_id}")
        print(f"Total Contacts: {result.total_contacts}")
        print(f"Successful: {result.successful}")
        print(f"Failed: {result.failed}")
        print(f"Processing Time: {result.processing_time:.2f} seconds")
        
        if result.failed > 0:
            print(f"\nFailed contacts:")
            for failed_result in [r for r in result.results if r.status == "failed"]:
                print(f"  - {failed_result.contact.name}: {failed_result.error_message}")
        
        # Exit with appropriate code
        sys.exit(0 if result.failed == 0 else 1)
        
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()