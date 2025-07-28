"""Extract information from all researchers - FIXED COUNT"""

import asyncio
from pathlib import Path

async def extract_all_researchers_info(tab):
    """Extract information from all researchers - simple approach with working count"""
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
        
        # Step 4: Get researcher count using the WORKING XPath method
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
        
        # Step 5: Iterate through each researcher
        for i in range(researcher_count):
            print(f"\n--- Processing Researcher {i+1}/{researcher_count} ---")
            
            try:
                # Click the button inside the li element using XPath (0-based index)
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
                
                # Click collaborators link
                try:
                    collaborators_link = await tab.select('//a[normalize-space()="Current collaborators (Authors)"]')
                    await collaborators_link.click()
                    print("✅ Clicked Current collaborators link")
                    await asyncio.sleep(5)
                    
                    print("TODO: Extract researcher information here")
                    
                except Exception as e:
                    print(f"⚠ Could not click collaborators link: {e}")
                
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

async def run_extraction(tab):
    """Run the extraction process"""
    print("=== STARTING RESEARCHER EXTRACTION ===")
    await extract_all_researchers_info(tab)
    return []
