import argparse
import sys
import os
from services.batch_processor import BatchProcessor
from utils.config import Config
from utils.logger import get_logger

def main():

    args.excel_file = os.path.abspath(args.excel_file)

    parser = argparse.ArgumentParser(description='SMS Automation Backend')
    parser.add_argument('excel_file', help='Path to Excel file with contacts')
    # Removed the --config argument since we're using the default
    
    args = parser.parse_args()
    
    # ✅ VALIDATE FILE EXISTS
    if not os.path.exists(args.excel_file):
        print(f"❌ Error: File '{args.excel_file}' not found!")
        print("Please provide a valid Excel file path.")
        sys.exit(1)
    
    # ✅ CHECK FILE EXTENSION
    if not args.excel_file.lower().endswith(('.xlsx', '.xls')):
        print(f"❌ Error: File '{args.excel_file}' is not an Excel file!")
        print("Please provide an .xlsx or .xls file.")
        sys.exit(1)
    
    # Initialize config (uses default 'config.yaml' in project root)
    config = Config()  # No argument needed - uses default path
    logger = get_logger("main")
    
    try:
        # Create processor
        processor = BatchProcessor(
            gateway_url=config.get('gateway.base_url')
        )
        
        # ✅ PROCESS THE FILE - args.excel_file contains the path you provided!
        print(f"📁 Processing file: {args.excel_file}")
        result, validation_errors = processor.process_excel_file(args.excel_file)
        
        # Display results
        print(f"\n=== BATCH PROCESSING COMPLETED ===")
        print(f"Batch ID: {result.batch_id}")
        print(f"Valid Contacts Found: {result.total_contacts}")
        print(f"Successfully Sent: {result.successful}")
        print(f"Failed to Send: {result.failed}")
        print(f"Validation Errors: {len(validation_errors)}")
        print(f"Processing Time: {result.processing_time:.2f} seconds")
        
        # Show validation errors if any
        if validation_errors:
            print(f"\n=== VALIDATION ERRORS (Not Processed) ===")
            for error in validation_errors:
                print(f"Row {error['row_index']}: {error['name']}")
                print(f"  Phone: {error['phone_attempted']}")
                print(f"  Error: {error['error']}")
                print()
        
        # Show sending failures if any
        if result.failed > 0:
            print(f"\n=== SENDING FAILURES ===")
            for failed_result in [r for r in result.results if r.status == "failed"]:
                print(f"  - {failed_result.contact.name}: {failed_result.error_message}")
        
        # Exit with appropriate code
        sys.exit(0 if result.failed == 0 and len(validation_errors) == 0 else 1)
        
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()