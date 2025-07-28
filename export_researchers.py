"""Export existing researchers functionality - simplified with file moving"""

import asyncio
import csv
import pandas as pd
from pathlib import Path
import re
import shutil
from config import RESEARCHERS_URL, DOWNLOAD_DIR

async def export_existing_researchers(tab, download_dir=DOWNLOAD_DIR):
    """Export existing researchers - simplified with file moving"""
    try:
        # Create custom download directory
        custom_path = Path(download_dir).resolve()
        custom_path.mkdir(exist_ok=True)
        
        # System download folder (where files actually go)
        system_downloads = Path.home() / "Downloads"
        
        # Navigate to researchers page
        await tab.get(RESEARCHERS_URL)
        await asyncio.sleep(5)
        
        print("Checking for existing researchers...")
        
        # Simple 3-step export
        try:
            select_all_label = await tab.select('label[for="selectAllCheckbox"]')
            await select_all_label.click()
            print("✅ Select all checkbox clicked")
        except Exception as e:
            print("❌ No select all checkbox - no existing researchers")
            return [], None
        
        await asyncio.sleep(2)
        
        # Export button
        export_button = await tab.select('#exportButton')
        await export_button.click()
        print("✅ Export button clicked")
        await asyncio.sleep(2)
        
        # CSV export
        csv_button = await tab.select('#entityExportCsv')
        await csv_button.click()
        print("✅ CSV export clicked")
        
        # Wait for download and move file
        print("Waiting for download...")
        moved_file = await wait_and_move_scival_file(system_downloads, custom_path)
        
        if moved_file:
            print(f"✅ File moved to: {moved_file}")
            existing_ids = read_existing_scopus_ids(moved_file)
            return existing_ids, str(moved_file)
        else:
            print("❌ No SciVal file found")
            return [], None
            
    except Exception as e:
        print(f"❌ Export error: {e}")
        return [], None

async def wait_and_move_scival_file(source_dir, target_dir, max_wait=30):
    """Wait for SciVal file in Downloads, then move it to custom folder"""
    pattern = re.compile(r'^mySciVal_Researchers_Export(\s\(\d+\))?\.csv$', re.IGNORECASE)
    
    # Get initial files to detect new ones
    initial_files = set()
    if source_dir.exists():
        for file in source_dir.glob("*.csv"):
            if pattern.match(file.name):
                initial_files.add(file.name)
    
    print(f"Monitoring {source_dir} for new SciVal files...")
    
    for i in range(max_wait):
        if source_dir.exists():
            current_files = []
            for file in source_dir.glob("*.csv"):
                if pattern.match(file.name):
                    current_files.append(file)
            
            # Find new files
            new_files = [f for f in current_files if f.name not in initial_files]
            
            if new_files:
                # Get the newest file
                newest_file = max(new_files, key=lambda x: x.stat().st_mtime)
                
                # Wait a bit for download to complete
                await asyncio.sleep(3)
                
                # Check if file is ready
                try:
                    if newest_file.stat().st_size > 0:
                        # Move file to custom directory
                        target_file = target_dir / newest_file.name
                        shutil.move(str(newest_file), str(target_file))
                        print(f"✅ Moved {newest_file.name} from Downloads to {target_dir}")
                        return target_file
                except Exception as e:
                    print(f"⚠ File not ready: {e}")
        
        if i % 5 == 0:
            print(f"Still waiting... ({i}/{max_wait}s)")
        
        await asyncio.sleep(1)
    
    print("❌ No new SciVal file detected")
    return None

def read_existing_scopus_ids(csv_file_path):
    """Read Scopus Author IDs from CSV"""
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        print(f"✅ CSV loaded: {len(df)} rows")
        
        # Find Scopus Author ID column
        for col in df.columns:
            if 'scopus author id' in col.lower():
                ids = df[col].dropna().astype(str).tolist()
                ids = [id.strip() for id in ids if id.strip() and id.strip().lower() != 'nan']
                print(f"✅ Found {len(ids)} Scopus IDs")
                return ids
        
        print(f"❌ No Scopus column found. Columns: {list(df.columns)}")
        return []
        
    except Exception as e:
        print(f"❌ CSV read error: {e}")
        return []
