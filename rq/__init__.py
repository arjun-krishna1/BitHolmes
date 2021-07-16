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
        return int(count)

    #for element in response.json():
     #   print(element)


check_addr("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2")
