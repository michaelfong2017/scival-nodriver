"""Configuration settings for SciVal automation"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Credentials
ELSEVIER_USERNAME = os.getenv('ELSEVIER_USERNAME')
ELSEVIER_PASSWORD = os.getenv('ELSEVIER_PASSWORD')
ELSEVIER_EMAIL = os.getenv('ELSEVIER_EMAIL')
ELSEVIER_SECOND_PASSWORD = os.getenv('ELSEVIER_SECOND_PASSWORD')

# URLs
CITYU_LOGIN_URL = 'https://lbsystem.lib.cityu.edu.hk/ezlogin/index.aspx?url=https%3a%2f%2fwww.scival.com'
OAUTH2_URL = 'https://id-elsevier-com.ezproxy.cityu.edu.hk/as/authorization.oauth2?platSite=SVE%2FSciVal&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info&response_type=code&redirect_uri=https%3A%2F%2Fwww.scival.com%2Fidp%2Fcode&prompt=login&client_id=SCIVAL'
RESEARCHERS_URL = 'https://www-scival-com.ezproxy.cityu.edu.hk/mySciVal?selection=researchers'

# Paths
DOWNLOAD_DIR = "./scival_downloads"
RESEARCHER_IDS_CSV = 'researcher_ids.csv'

# Browser configuration
BROWSER_ARGS = ['--no-sandbox', '--disable-setuid-sandbox']

# Operation Mode Selection
# Set to "full" for complete workflow (export -> import -> extract)
# Set to "extract" for login -> extract only
OPERATION_MODE = "extract"  # Change this to "full" or "extract"
