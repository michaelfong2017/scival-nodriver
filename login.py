"""Login functionality for SciVal"""

import asyncio
from config import (
    ELSEVIER_USERNAME, ELSEVIER_PASSWORD, ELSEVIER_EMAIL, 
    ELSEVIER_SECOND_PASSWORD, CITYU_LOGIN_URL, OAUTH2_URL
)

async def login(browser):
    """Complete login process - returns the authenticated tab"""
    if not ELSEVIER_USERNAME or not ELSEVIER_PASSWORD or not ELSEVIER_EMAIL or not ELSEVIER_SECOND_PASSWORD:
        print("Error: Missing credentials in .env file")
        return None
    
    try:
        # Step 1: Navigate to CityU login
        tab = await browser.get(CITYU_LOGIN_URL)
        await asyncio.sleep(3)
        
        # Enter username
        username_field = await tab.select('#cred_userid_inputtext')
        await username_field.send_keys(ELSEVIER_USERNAME)
        
        # Enter password
        password_field = await tab.select('#cred_password_inputtext')
        await password_field.send_keys(ELSEVIER_PASSWORD)
        await asyncio.sleep(1)
        
        # Click sign-in
        sign_in_button = await tab.select('#cred_sign_in_button')
        await sign_in_button.click()
        await asyncio.sleep(5)
        
        print("First login completed, navigating to OAuth2...")
        
        # Step 2: Navigate to OAuth2 URL
        await tab.get(OAUTH2_URL)
        await asyncio.sleep(3)
        
        # Step 3: Enter email using Method 3
        await tab.evaluate(f"""
            const field = document.querySelector('#bdd-email');
            if (field) {{
                field.focus();
                field.value = '';
                
                const email = '{ELSEVIER_EMAIL}';
                let currentValue = '';
                
                for (let i = 0; i < email.length; i++) {{
                    currentValue += email[i];
                    field.value = currentValue;
                    
                    field.dispatchEvent(new KeyboardEvent('keydown', {{ key: email[i], bubbles: true }}));
                    field.dispatchEvent(new KeyboardEvent('keypress', {{ key: email[i], bubbles: true }}));
                    field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    field.dispatchEvent(new KeyboardEvent('keyup', {{ key: email[i], bubbles: true }}));
                }}
                
                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
        """)
        
        await asyncio.sleep(2)
        
        # Step 4: Click continue
        primary_button = await tab.select('#bdd-elsPrimaryBtn')
        await primary_button.click()
        print("Continue button clicked successfully")
        await asyncio.sleep(3)
        
        print("Entering second password...")
        
        # Step 5: Enter second password using Method 3
        await tab.evaluate(f"""
            const passwordField = document.querySelector('#bdd-password');
            if (passwordField) {{
                passwordField.focus();
                passwordField.value = '';
                
                const secondPassword = '{ELSEVIER_SECOND_PASSWORD}';
                let currentValue = '';
                
                for (let i = 0; i < secondPassword.length; i++) {{
                    currentValue += secondPassword[i];
                    passwordField.value = currentValue;
                    
                    passwordField.dispatchEvent(new KeyboardEvent('keydown', {{ key: secondPassword[i], bubbles: true }}));
                    passwordField.dispatchEvent(new KeyboardEvent('keypress', {{ key: secondPassword[i], bubbles: true }}));
                    passwordField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    passwordField.dispatchEvent(new KeyboardEvent('keyup', {{ key: secondPassword[i], bubbles: true }}));
                }}
                
                passwordField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                passwordField.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
        """)
        
        await asyncio.sleep(1)
        
        # Step 6: Uncheck "Remember Me" checkbox
        try:
            remember_me_checkbox = await tab.select('#rememberMe')
            is_checked = await remember_me_checkbox.get_attribute('checked')
            
            if is_checked:
                await remember_me_checkbox.click()
                print("Remember Me checkbox unchecked")
        except Exception as e:
            print(f"Could not uncheck Remember Me: {e}")
            await tab.evaluate("""
                const rememberMeCheckbox = document.querySelector('#rememberMe');
                if (rememberMeCheckbox && rememberMeCheckbox.checked) {
                    rememberMeCheckbox.checked = false;
                    rememberMeCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """)
        
        await asyncio.sleep(1)
        
        # Step 7: Final submit
        await tab.evaluate("""
            const button = document.querySelector('#bdd-elsPrimaryBtn');
            if (button) {
                button.focus();
                button.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                button.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                button.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            }
        """)
        
        print("Final submit button clicked successfully")
        await asyncio.sleep(5)
        
        title = await tab.evaluate('document.title')
        print(f"Login completed - Page title: {title}")
        
        return tab
        
    except Exception as e:
        print(f"Error during login process: {e}")
        return None
