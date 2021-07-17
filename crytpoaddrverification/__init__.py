import requests

def verify_bitcoin(public_key):
    public_key = public_key.strip()
    for i in public_key:
        value = ord(i)
        if value < 48 or value > 122 or (value > 57 and value < 65) or (value > 91 and value < 96):
            return False
    page = requests.get(f'https://www.blockchain.com/btc/address/{public_key}')
    if page.ok:
        return True
    return False
