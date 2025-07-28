"""Extract information from all researchers - Extended collaborators process"""

import asyncio
import shutil
import re
from pathlib import Path

async def extract_all_researchers_info(tab):
    """Extract information from all researchers - with extended collaborators workflow"""
    try:
        # Step 1: Navigate to overview page
        overview_url = "https://www-scival-com.ezproxy.cityu.edu.hk/overview/summary?uri=Institution%2F205002"
        await tab.get(overview_url)
        await asyncio.sleep(5)
        print("✅ Navigated to overview summary page")
        
        # Step 2: Click toggle button
        toggle_btn = await tab.select('#entityListToggleBtn')
        await toggle_btn.click()
        print("✅ Entity list toggle button clicked")
        await asyncio.sleep(3)
        
        # Step 3: Check researchers radio button
        researchers_radio = await tab.select('label[for="entityFilter_researchers"]')
        await researchers_radio.click()
        print("✅ Researchers radio button selected")
        await asyncio.sleep(3)
        
        # Step 4: Get researcher count using XPath
        researcher_count = await tab.evaluate("""
            (function() {
                try {
                    const xpath = '//div[@id="entityListPanel"]//li';
                    const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    return result.snapshotLength;
                } catch (error) {
                    console.error('XPath evaluation error:', error);
                    return 0;
                }
            })()
        """)
        
        print(f"XPath '//div[@id=\"entityListPanel\"]//li' found {researcher_count} researchers")
        
        if researcher_count == 0:
            print("❌ No researchers found")
            return []
        
        # Custom download folder
        custom_download_path = Path("./scival_downloads").resolve()
        custom_download_path.mkdir(exist_ok=True)
        system_downloads = Path.home() / "Downloads"
        
        # Step 5: Iterate through each researcher
        for i in range(researcher_count):
            print(f"\n--- Processing Researcher {i+1}/{researcher_count} ---")
            
            try:
                # Click the button inside the li element using XPath
                button_clicked = await tab.evaluate(f"""
                    (function() {{
                        try {{
                            const xpath = '//div[@id="entityListPanel"]//li[{i+1}]';
                            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                            const li = result.singleNodeValue;
                            
                            if (li) {{
                                const button = li.querySelector('button');
                                if (button) {{
                                    button.click();
                                    return true;
                                }}
                            }}
                            return false;
                        }} catch (error) {{
                            console.error('Error clicking button:', error);
                            return false;
                        }}
                    }})()
                """)
                
                if button_clicked:
                    print(f"✅ Clicked researcher {i+1} button")
                else:
                    print(f"❌ No button found in researcher {i+1}")
                    continue
                
                await asyncio.sleep(3)
                
                # Click collaborators link using JavaScript evaluation
                collaborators_clicked = await tab.evaluate("""
                    (function() {
                        try {
                            const xpath = '//a[normalize-space()="Current collaborators (Authors)"]';
                            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                            const link = result.singleNodeValue;
                            
                            if (link) {
                                link.click();
                                return true;
                            }
                            return false;
                        } catch (error) {
                            console.error('Error clicking collaborators link:', error);
                            return false;
                        }
                    })()
                """)
                
                if collaborators_clicked:
                    print("✅ Clicked Current collaborators link")
                    
                    # Wait longer for loading as requested
                    print("⏳ Waiting longer for collaborators page to load...")
                    await asyncio.sleep(10)
                    
                    # Extended collaborators workflow
                    await process_collaborators_page(tab, system_downloads, custom_download_path)
                    
                else:
                    print("❌ Could not find collaborators link")
                
                # Navigate back to list
                toggle_btn = await tab.select('#entityListToggleBtn')
                await toggle_btn.click()
                await asyncio.sleep(2)
                
                researchers_radio = await tab.select('label[for="entityFilter_researchers"]')
                await researchers_radio.click()
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"❌ Error processing researcher {i+1}: {e}")
                continue
        
        print(f"\n🎉 Iteration complete!")
        return []
        
    except Exception as e:
        print(f"❌ Error in extract_all_researchers_info: {e}")
        return []

async def process_collaborators_page(tab, system_downloads, custom_download_path):
    """Process the collaborators page with BOTH programmatic change AND visual click"""
    try:
        # Step 1: Click span[id="authorCountSel-button"] span[class="ui-selectmenu-text"]
        print("🔸 Step 1: Clicking author count selector...")
        try:
            author_count_selector = await tab.select('span[id="authorCountSel-button"] span[class="ui-selectmenu-text"]')
            await author_count_selector.click()
            print("✅ Author count selector clicked")
        except Exception as e:
            print(f"❌ Failed to click author count selector: {e}")
            return
        
        # Wait for dropdown to appear
        print("⏳ Waiting for dropdown to appear...")
        await asyncio.sleep(3)
        
        # Step 2A: VISUAL CLICK - Show the user the dropdown interaction
        print("🔸 Step 2A: Visual click for user feedback...")
        
        visual_click_done = await tab.evaluate("""
            (function() {
                try {
                    // Find the visual menu item by text content for user to see
                    const menuItems = document.querySelectorAll('.ui-menu-item-wrapper');
                    
                    for (let item of menuItems) {
                        const text = item.textContent.trim();
                        
                        // Look for "< = 10 authors" text
                        if (text.includes('10 authors')) {
                            console.log('Visually clicking option:', text);
                            
                            // Visual click for user feedback
                            item.focus();
                            item.click();
                            
                            // Dispatch visual mouse events
                            item.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                            item.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                            item.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                            
                            return true;
                        }
                    }
                    return false;
                } catch (error) {
                    console.error('Error with visual click:', error);
                    return false;
                }
            })()
        """)
        
        if visual_click_done:
            print("✅ Visual click completed for user feedback")
        else:
            print("⚠ Visual click failed, but will proceed with programmatic change")
        
        await asyncio.sleep(1)
        
        # Step 2B: PROGRAMMATIC CHANGE - Ensure the value actually changes
        print("🔸 Step 2B: Programmatic value change (ensuring it works)...")
        
        dropdown_changed = await tab.evaluate("""
            (function() {
                try {
                    // Target the specific select element #authorCountSel
                    const selectElement = document.querySelector('#authorCountSel');
                    
                    if (selectElement) {
                        console.log('Found #authorCountSel select element');
                        console.log('Current value:', selectElement.value);
                        
                        // Check if option[value="10"] exists
                        const targetOption = selectElement.querySelector('option[value="10"]');
                        if (targetOption) {
                            console.log('Found option[value="10"]:', targetOption.text);
                            
                            // Set the select element value to "10"
                            selectElement.value = '10';
                            
                            // Mark the option as selected
                            targetOption.selected = true;
                            
                            console.log('Set select value to "10" and marked option as selected');
                            
                            // Trigger change events on the select element
                            selectElement.dispatchEvent(new Event('change', { bubbles: true }));
                            selectElement.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // Trigger the jQuery UI selectmenu update
                            if (window.jQuery && window.jQuery.fn.selectmenu) {
                                try {
                                    window.jQuery('#authorCountSel').selectmenu('refresh');
                                    console.log('jQuery selectmenu refreshed');
                                } catch (e) {
                                    console.log('jQuery selectmenu refresh failed:', e.message);
                                }
                            }
                            
                            // Execute the data-callback: collaborationTable.changeAuthorCount
                            const callback = selectElement.getAttribute('data-callback');
                            if (callback === 'collaborationTable.changeAuthorCount') {
                                try {
                                    if (window.collaborationTable && typeof window.collaborationTable.changeAuthorCount === 'function') {
                                        window.collaborationTable.changeAuthorCount();
                                        console.log('Executed collaborationTable.changeAuthorCount()');
                                    } else {
                                        console.log('collaborationTable.changeAuthorCount function not found');
                                    }
                                } catch (e) {
                                    console.log('Callback execution failed:', e.message);
                                }
                            }
                            
                            // Close the dropdown visually
                            const dropdownMenu = document.querySelector('.ui-selectmenu-menu');
                            if (dropdownMenu) {
                                dropdownMenu.style.display = 'none';
                            }
                            
                            // Verify the change
                            console.log('Final value:', selectElement.value);
                            console.log('Option selected:', targetOption.selected);
                            
                            return true;
                        } else {
                            console.log('option[value="10"] not found in #authorCountSel');
                            return false;
                        }
                    } else {
                        console.log('#authorCountSel select element not found');
                        return false;
                    }
                    
                } catch (error) {
                    console.error('Error changing dropdown value:', error);
                    return false;
                }
            })()
        """)
        
        if dropdown_changed:
            print("✅ Dropdown value changed programmatically to option[value='10']")
            await asyncio.sleep(3)
        else:
            print("❌ Could not change dropdown value")
            return
        
        # Step 3: Click div[class="header-wrapper"] button[class="link action-link"]
        print("🔸 Step 3: Clicking header action link...")
        try:
            header_action_link = await tab.select('div[class="header-wrapper"] button[class="link action-link"]')
            await header_action_link.click()
            print("✅ Header action link clicked")
        except Exception as e:
            print(f"❌ Failed to click header action link: {e}")
            return
        
        await asyncio.sleep(2)
        
        # Step 4: Click indexed XPath (//button[@data-format='spreadsheet'])[1]
        print("🔸 Step 4: Clicking spreadsheet download button...")
        try:
            download_clicked = await tab.evaluate("""
                (function() {
                    try {
                        const xpath = "(//button[@data-format='spreadsheet'])[1]";
                        const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                        const button = result.singleNodeValue;
                        
                        if (button) {
                            button.click();
                            return true;
                        }
                        return false;
                    } catch (error) {
                        console.error('Error clicking spreadsheet button:', error);
                        return false;
                    }
                })()
            """)
            
            if download_clicked:
                print("✅ Spreadsheet download button clicked")
                
                # Wait for download and move file
                print("⏳ Waiting for download to complete...")
                moved_file = await wait_and_move_collaborators_file(system_downloads, custom_download_path)
                
                if moved_file:
                    print(f"✅ File moved to custom folder: {moved_file}")
                else:
                    print("❌ No collaborators file found to move")
                    
            else:
                print("❌ Could not click spreadsheet download button")
                
        except Exception as e:
            print(f"❌ Failed to click spreadsheet button: {e}")
        
    except Exception as e:
        print(f"❌ Error in collaborators page processing: {e}")

async def wait_and_move_collaborators_file(source_dir, target_dir, max_wait=30):
    """Wait for Authors_collaborating_with_*.csv file and move it to custom folder"""
    # Pattern to match: Authors_collaborating_with_[AuthorName].csv
    pattern = re.compile(r'^Authors_collaborating_with_.*\.csv$', re.IGNORECASE)
    
    # Get initial files to detect new ones
    initial_files = set()
    if source_dir.exists():
        for file in source_dir.glob("*.csv"):
            if pattern.match(file.name):
                initial_files.add(file.name)
    
    print(f"📁 Monitoring {source_dir} for new collaborators CSV files...")
    
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
            print(f"Still waiting for collaborators file... ({i}/{max_wait}s)")
        
        await asyncio.sleep(1)
    
    print("❌ No new collaborators CSV file detected")
    return None

async def run_extraction(tab):
    """Run the extraction process"""
    print("=== STARTING RESEARCHER EXTRACTION ===")
    await extract_all_researchers_info(tab)
    return []
