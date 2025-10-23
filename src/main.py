import argparse
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

from services.batch_processor import BatchProcessor
from utils.config import Config
from utils.logger import get_logger

def main():
    parser = argparse.ArgumentParser(description='SMS Automation Backend')
    parser.add_argument('excel_file', help='Path to Excel file with contacts')
    
    args = parser.parse_args()
    
    excel_file_path = os.path.abspath(args.excel_file)
    
    print(f"🔍 File path debug:")
    print(f"   Input path: {args.excel_file}")
    print(f"   Absolute path: {excel_file_path}")
    print(f"   File exists: {os.path.exists(excel_file_path)}")
    
    if not os.path.exists(excel_file_path):
        print(f"❌ Error: File '{excel_file_path}' not found!")
        print(f"💡 Current directory: {os.getcwd()}")
        print("💡 Try these solutions:")
        print("   1. Use absolute path: /full/path/to/file.xlsx")
        print("   2. Make sure file is in current directory")
        print("   3. Check for typos in file name")
        sys.exit(1)
    
    if not excel_file_path.lower().endswith(('.xlsx', '.xls')):
        print(f"❌ Error: File '{excel_file_path}' is not an Excel file!")
        print("Please provide an .xlsx or .xls file.")
        sys.exit(1)
    
    config = Config()
    logger = get_logger("main")
    
    try:
        processor = BatchProcessor(
            gateway_url=config.get('gateway.base_url')
        )
        
        print(f"📁 Processing file: {excel_file_path}")
        result, validation_errors = processor.process_excel_file(excel_file_path)
        
        print(f"\n🎉 BATCH PROCESSING COMPLETED!")
        print(f"📋 Batch ID: {result.batch_id}")
        print(f"👥 Valid Contacts Found: {result.total_contacts}")
        print(f"✅ Successfully Sent: {result.successful}")
        print(f"❌ Failed to Send: {result.failed}")
        print(f"⚠️  Validation Errors: {len(validation_errors)}")
        print(f"⏱️  Processing Time: {result.processing_time:.2f} seconds")
        
        if validation_errors:
            print(f"\n📝 VALIDATION ERRORS (These contacts were NOT processed):")
            for error in validation_errors:
                print(f"   📍 Row {error['row_index']}: {error['name']}")
                print(f"      📞 {error['phone_attempted']}")
                print(f"      ❗ {error['error']}")
        
        if result.failed > 0:
            print(f"\n🔥 SENDING FAILURES:")
            for failed_result in [r for r in result.results if r.status == "failed"]:
                print(f"   ❌ {failed_result.contact.name}: {failed_result.error_message}")
        
        if result.failed == 0 and len(validation_errors) == 0:
            print(f"\n✨ SUCCESS: All contacts processed successfully!")
            sys.exit(0)
        else:
            print(f"\n⚠️  COMPLETED WITH ISSUES: Check the report above")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"💥 Application failed: {str(e)}")
        print(f"💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()