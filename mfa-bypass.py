import requests

def direct_endpoint_access(login, mfa, dest):
    '''
    Check for direct endpoint access to bypass 2FA.
    '''
    session = requests.Session()
    login_page = session.get(login) # Generate CSRF token
    login_data = {} # Fill this with valid login data, including other fields like CSRF token if required, extract from login_page.

    login_response = session.post(login, data=login_data)
    if login_response.status_code == 200 and login_response.url != login:
        print("[+] Logged in succesfully!")
    else:
        print("[-] Login failed! Check login parameters again.")
        return

    headers = {
        'Referer': mfa,
        'User-Agent': 'Mozilla/5.0 (Direct-Access)',
        # Add any additionally required headers
    }

    try:
        destination = session.get(dest, headers=headers, allow_redirects=True, timeout=10)
        return {
            'status': destination.status_code,
            'url': destination.url,
            'redirects': len(destination.history),
            'text_snippet': destination.text[:200]
        }
    except requests.RequestException as e:
        return {'error': str(e)}
    
# Calling all functions here:
direct_bypass = direct_endpoint_access(
    login="https://example.com/login",
    mfa="https://example.com/mfa",
    dest="https://example.com/dashboard"
)
if direct_bypass is not None: print(direct_bypass)