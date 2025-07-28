"""Main script to orchestrate SciVal automation"""

import asyncio
from browser_utils import create_browser, safe_browser_cleanup
from login import login
from export_researchers import export_existing_researchers
from import_researchers import read_researcher_ids_from_csv, import_researcher
from config import DOWNLOAD_DIR

async def main():
    browser = None
    try:
        # Create browser (no download path setting needed)
        browser = await create_browser()
        
        # Step 1: Login
        print("=== STEP 1: LOGIN ===")
        tab = await login(browser)
        
        if not tab:
            print("❌ Login failed, exiting...")
            return
        
        print("✅ Login successful!")
        
        # Step 2: Export existing researchers
        print(f"\n=== STEP 2: EXPORT TO CUSTOM PATH ({DOWNLOAD_DIR}) ===")
        existing_ids, export_file = await export_existing_researchers(tab, DOWNLOAD_DIR)
        
        if existing_ids:
            print(f"✅ Found {len(existing_ids)} existing researchers")
            print(f"📁 Export file: {export_file}")
            # Show first few for verification
            for i, existing_id in enumerate(existing_ids[:5]):
                print(f"  {i+1}. {existing_id}")
            if len(existing_ids) > 5:
                print(f"  ... and {len(existing_ids) - 5} more")
        else:
            print("⚠ No existing researchers found")
        
        # Step 3: Read new researcher IDs to import
        print("\n=== STEP 3: READ TARGET RESEARCHER IDs ===")
        new_researcher_ids = read_researcher_ids_from_csv()
        
        if not new_researcher_ids:
            print("❌ No researcher IDs found in CSV file")
            return
        
        print(f"✅ Found {len(new_researcher_ids)} target researcher IDs")
        
        # Step 4: Compare and find missing IDs
        print("\n=== STEP 4: COMPARE AND FIND MISSING IDs ===")
        ids_to_import = []
        existing_count = 0
        
        for new_id in new_researcher_ids:
            if new_id in existing_ids:
                existing_count += 1
                print(f"✓ {new_id} - already exists")
            else:
                ids_to_import.append(new_id)
                print(f"+ {new_id} - MISSING, will import")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total existing: {len(existing_ids)}")
        print(f"   Total targets: {len(new_researcher_ids)}")
        print(f"   Already exist: {existing_count}")
        print(f"   Missing (to import): {len(ids_to_import)}")
        
        if not ids_to_import:
            print("🎉 All researchers already exist!")
        else:
            # Step 5: Import missing researchers
            print(f"\n=== STEP 5: IMPORT {len(ids_to_import)} MISSING RESEARCHERS ===")
            successful = 0
            failed = 0
            
            for researcher_id in ids_to_import:
                success = await import_researcher(tab, researcher_id)
                if success:
                    successful += 1
                    print(f"✅ Imported {researcher_id}")
                else:
                    failed += 1
                    print(f"❌ Failed to import {researcher_id}")
                
                await asyncio.sleep(2)
            
            print(f"\n🎉 IMPORT COMPLETE!")
            print(f"   Successful: {successful}")
            print(f"   Failed: {failed}")
        
        # Stay open infinitely
        print("\n🌐 Browser will stay open indefinitely. Press Ctrl+C to exit.")
        try:
            while True:
                await asyncio.sleep(60)
                try:
                    current_title = await tab.evaluate('document.title')
                    print(f"Still running... Current page: {current_title}")
                except:
                    print("Browser may have been closed by user")
                    break
        except KeyboardInterrupt:
            print("Received keyboard interrupt, closing browser...")
        
    except Exception as e:
        print(f"❌ Error in main process: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await safe_browser_cleanup(browser)

if __name__ == "__main__":
    asyncio.run(main())
