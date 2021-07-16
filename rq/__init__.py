import requests


def get_token():
    with open('../secrets.txt', 'r') as f:
        t = f.read()
        f.close()
        return t


def check_addr(address):
    key = get_token()
    call = f"https://www.bitcoinabuse.com/api/reports/check?address={address}&api_token={key}"
    response_json = requests.api.get(call).json()
    count = response_json["count"]
    if count:
        count = int(count)
        if count > 0:
            return 1  # 1 or more fraud reports on this address
        else:
            return 3  # no fraud reports for this address
    else:
        return -1  # count is missing


print(check_addr("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"))
