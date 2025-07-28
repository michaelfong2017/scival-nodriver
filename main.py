import asyncio
import nodriver as uc
from dotenv import load_dotenv
import os

async def navigate_and_login():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    username = os.getenv('ELSEVIER_USERNAME')
    password = os.getenv('ELSEVIER_PASSWORD')
    email = os.getenv('ELSEVIER_EMAIL')
    second_password = os.getenv('ELSEVIER_SECOND_PASSWORD')
    
    if not username or not password or not email or not second_password:
        print("Error: Username, password, email, or second password not found in .env file")
        return
    
    # Create a browser instance
    browser = await uc.start(headless=False)
    
    try:
        # Step 1: Navigate to the corrected first URL
        tab = await browser.get('https://lbsystem.lib.cityu.edu.hk/ezlogin/index.aspx?url=https%3a%2f%2fwww.scival.com')
        
        # Wait for the page to load
        await asyncio.sleep(3)
        
        # Wait for and find the username input field
        username_field = await tab.select('#cred_userid_inputtext')
        await username_field.send_keys(username)
        
        # Wait for and find the password input field
        password_field = await tab.select('#cred_password_inputtext')
        await password_field.send_keys(password)
        
        # Wait a moment before clicking
        await asyncio.sleep(1)
        
        # Find and click the sign-in button
        sign_in_button = await tab.select('#cred_sign_in_button')
        await sign_in_button.click()
        
        # Wait for login to process
        await asyncio.sleep(5)
        
        print("First login completed, navigating to second URL...")
        
        # Step 2: Navigate to the second URL
        await tab.get('https://id-elsevier-com.ezproxy.cityu.edu.hk/as/authorization.oauth2?platSite=SVE%2FSciVal&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info&response_type=code&redirect_uri=https%3A%2F%2Fwww.scival.com%2Fidp%2Fcode&prompt=login&client_id=SCIVAL')
        
        # Wait for the page to load
        await asyncio.sleep(3)
        
        # Step 3: Enter email using Method 3 (character by character with events)
        await tab.evaluate(f"""
            const field = document.querySelector('#bdd-email');
            if (field) {{
                field.focus();
                field.value = '';
                
                const email = '{email}';
                let currentValue = '';
                
                for (let i = 0; i < email.length; i++) {{
                    currentValue += email[i];
                    field.value = currentValue;
                    
                    // Dispatch events for each character
                    field.dispatchEvent(new KeyboardEvent('keydown', {{ key: email[i], bubbles: true }}));
                    field.dispatchEvent(new KeyboardEvent('keypress', {{ key: email[i], bubbles: true }}));
                    field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    field.dispatchEvent(new KeyboardEvent('keyup', {{ key: email[i], bubbles: true }}));
                }}
                
                // Final events
                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
        """)
        
        # Wait for form validation
        await asyncio.sleep(2)
        
        # Step 4: Click the primary button (Continue)
        primary_button = await tab.select('#bdd-elsPrimaryBtn')
        await primary_button.click()
        print("Continue button clicked successfully")
        
        # Wait for next page to load
        await asyncio.sleep(3)
        
        print("Entering second password on next screen...")
        
        # Step 5: Enter SECOND password using Method 3 on the next screen
        await tab.evaluate(f"""
            const passwordField = document.querySelector('#bdd-password');
            if (passwordField) {{
                passwordField.focus();
                passwordField.value = '';
                
                const secondPassword = '{second_password}';
                let currentValue = '';
                
                for (let i = 0; i < secondPassword.length; i++) {{
                    currentValue += secondPassword[i];
                    passwordField.value = currentValue;
                    
                    // Dispatch events for each character
                    passwordField.dispatchEvent(new KeyboardEvent('keydown', {{ key: secondPassword[i], bubbles: true }}));
                    passwordField.dispatchEvent(new KeyboardEvent('keypress', {{ key: secondPassword[i], bubbles: true }}));
                    passwordField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    passwordField.dispatchEvent(new KeyboardEvent('keyup', {{ key: secondPassword[i], bubbles: true }}));
                }}
                
                // Final events
                passwordField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                passwordField.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
        """)
        
        await asyncio.sleep(1)
        
        # Step 6: Uncheck the "Remember Me" checkbox using standard nodriver practice
        try:
            remember_me_checkbox = await tab.select('#rememberMe')
            
            # Check if it's currently checked
            is_checked = await remember_me_checkbox.get_attribute('checked')
            
            if is_checked:
                await remember_me_checkbox.click()
                print("Remember Me checkbox unchecked using nodriver click")
            else:
                print("Remember Me checkbox was already unchecked")
                
        except Exception as e:
            print(f"Could not uncheck Remember Me with standard method: {e}")
            # Fallback to JavaScript if needed
            await tab.evaluate("""
                const rememberMeCheckbox = document.querySelector('#rememberMe');
                if (rememberMeCheckbox && rememberMeCheckbox.checked) {
                    rememberMeCheckbox.checked = false;
                    rememberMeCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """)
            print("Remember Me checkbox unchecked using JavaScript fallback")
        
        await asyncio.sleep(1)
        
        # Step 7: Click the primary button using Method 3 approach
        await tab.evaluate("""
            const button = document.querySelector('#bdd-elsPrimaryBtn');
            if (button) {
                // Focus and click with events
                button.focus();
                
                // Dispatch mouse events for more realistic interaction
                button.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                button.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                button.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            }
        """)
        
        print("Final submit button clicked successfully")
        
        # Wait for the process to complete
        await asyncio.sleep(5)
        
        # Check current page title
        title = await tab.evaluate('document.title')
        print(f"Final page title: {title}")
        print("Login process completed successfully!")
        
        # Stay open infinitely - keep the browser running
        print("Browser will stay open indefinitely. Press Ctrl+C to exit.")
        try:
            while True:
                await asyncio.sleep(60)  # Check every minute
                # Optional: Check if browser is still alive
                try:
                    current_title = await tab.evaluate('document.title')
                    print(f"Still running... Current page: {current_title}")
                except:
                    print("Browser may have been closed by user")
                    break
        except KeyboardInterrupt:
            print("Received keyboard interrupt, closing browser...")
        
    except Exception as e:
        print(f"Error during process: {e}")
    finally:
        # Only close if there was an error or keyboard interrupt
        print("Closing browser...")
        await browser.stop()

if __name__ == "__main__":
    asyncio.run(navigate_and_login())
