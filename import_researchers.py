"""Import researchers functionality"""

import asyncio
import csv
from config import RESEARCHERS_URL, RESEARCHER_IDS_CSV

def read_researcher_ids_from_csv(csv_file_path=RESEARCHER_IDS_CSV):
    """Read researcher IDs from a CSV file"""
    researcher_ids = []
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Skip header if exists
            next(reader, None)
            for row in reader:
                if row and row[0].strip():  # Assuming IDs are in the first column
                    researcher_ids.append(row[0].strip())
        print(f"Read {len(researcher_ids)} researcher IDs from {csv_file_path}")
        return researcher_ids
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

async def import_researcher(tab, researcher_id):
    """Import a single researcher using their ID - FIXED VERSION"""
    try:
        # Navigate to researchers page
        await tab.get(RESEARCHERS_URL)
        print(f"Importing researcher ID: {researcher_id}")
        
        # Wait for page to load
        await asyncio.sleep(5)
        
        # Click secondary button with simple approach first
        print("Clicking secondary button...")
        try:
            secondary_button = await tab.select('button[class="secondary action-link"] span')
            await secondary_button.click()
            print("✅ Secondary button clicked (span)")
        except Exception as e:
            try:
                secondary_button = await tab.select('button[class="secondary action-link"]')
                await secondary_button.click()
                print("✅ Secondary button clicked (parent)")
            except Exception as e2:
                # JavaScript fallback - FIXED syntax
                await tab.evaluate("""
                    (function() {
                        const button = document.querySelector('button[class="secondary action-link"] span') || 
                                     document.querySelector('button[class="secondary action-link"]');
                        if (button) {
                            button.click();
                            return true;
                        }
                        return false;
                    })();
                """)
                print("✅ Secondary button clicked via JavaScript")
        
        await asyncio.sleep(3)
        
        # Click import link
        print("Clicking import link...")
        try:
            import_link = await tab.select('button[class="link primary-link importResearchersLink"] span')
            await import_link.click()
            print("✅ Import link clicked")
        except Exception as e:
            try:
                import_link = await tab.select('button[class="link primary-link importResearchersLink"]')
                await import_link.click()
                print("✅ Import link clicked (parent)")
            except Exception as e2:
                await tab.evaluate("""
                    (function() {
                        const link = document.querySelector('button[class="link primary-link importResearchersLink"] span') ||
                                   document.querySelector('button[class="link primary-link importResearchersLink"]');
                        if (link) {
                            link.click();
                            return true;
                        }
                        return false;
                    })();
                """)
                print("✅ Import link clicked via JavaScript")
        
        await asyncio.sleep(5)
        
        # Enter researcher ID using Method 3
        print("Entering researcher ID...")
        await tab.evaluate(f"""
            (function() {{
                const idField = document.querySelector('#loadIDsArea');
                if (idField) {{
                    idField.focus();
                    idField.value = '';
                    
                    const researcherId = '{researcher_id}';
                    let currentValue = '';
                    
                    for (let i = 0; i < researcherId.length; i++) {{
                        currentValue += researcherId[i];
                        idField.value = currentValue;
                        
                        idField.dispatchEvent(new KeyboardEvent('keydown', {{ key: researcherId[i], bubbles: true }}));
                        idField.dispatchEvent(new KeyboardEvent('keypress', {{ key: researcherId[i], bubbles: true }}));
                        idField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        idField.dispatchEvent(new KeyboardEvent('keyup', {{ key: researcherId[i], bubbles: true }}));
                    }}
                    
                    idField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    idField.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    return true;
                }}
                return false;
            }})();
        """)
        
        await asyncio.sleep(3)
        
        # Click import next button
        print("Clicking import next button...")
        try:
            import_next_button = await tab.select('#importNextButton')
            await import_next_button.click()
            print("✅ Import next button clicked")
        except Exception as e:
            await tab.evaluate("""
                (function() {
                    const button = document.querySelector('#importNextButton');
                    if (button) {
                        button.click();
                        return true;
                    }
                    return false;
                })();
            """)
            print("✅ Import next button clicked via JavaScript")
        
        await asyncio.sleep(5)
        
        # Click organize first button
        print("Clicking organize first button...")
        try:
            organize_first_button = await tab.select('#organizeFirstButton')
            await organize_first_button.click()
            print("✅ Organize first button clicked")
        except Exception as e:
            await tab.evaluate("""
                (function() {
                    const button = document.querySelector('#organizeFirstButton');
                    if (button) {
                        button.click();
                        return true;
                    }
                    return false;
                })();
            """)
            print("✅ Organize first button clicked via JavaScript")
        
        await asyncio.sleep(3)
        
        # Click save button
        print("Clicking save button...")
        try:
            save_button = await tab.select('#saveButton')
            await save_button.click()
            print("✅ Save button clicked")
        except Exception as e:
            await tab.evaluate("""
                (function() {
                    const button = document.querySelector('#saveButton');
                    if (button) {
                        button.click();
                        return true;
                    }
                    return false;
                })();
            """)
            print("✅ Save button clicked via JavaScript")
        
        await asyncio.sleep(5)
        
        print(f"✅ Successfully imported researcher ID: {researcher_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error importing researcher {researcher_id}: {e}")
        import traceback
        traceback.print_exc()
        return False
