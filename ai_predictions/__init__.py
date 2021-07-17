import tensorflow as tf
import numpy as np
import requests

BASE_API = "https://blockchain.info/rawaddr/"
def get_data_api(address):
    url = BASE_API + address
    resp = requests.get(url)
    try:
        entire_dict = resp.json()
        return entire_dict
    except:
        return {}

id_features = ["n_tx", "n_unredeemed", "total_received", "total_sent", "final_balance"]
transaction_features = ["ver", "vin_sz", "vout_sz", "size", "weight", "fee", "lock_time", "double_spend", "time"]
all_features = id_features + transaction_features

def flatten_entire_dict(curr):
    id_dict_base = {feat: curr[feat] for feat in id_features}
    tot_vals = []
    for tx in curr["txs"]:
        this_tx_vals = {}
        for tx_feat in transaction_features:
            this_tx_vals[tx_feat] = tx[tx_feat]
        tot_vals.append({**id_dict_base, **this_tx_vals})
    return tot_vals

def dict_to_array(flat_dict):
    array = []
    for tx  in flat_dict:
        array.append([tx[feat] for feat in all_features])
    return array

if __name__ == "__main__":
    test_address = "1JxmKkNK1b3p7r8DDPtnNmGeLZDcgPadJb"
    data = get_data_api(test_address)
    flat_dict = flatten_entire_dict(data)
    array = dict_to_array(flat_dict)
    print(array)
