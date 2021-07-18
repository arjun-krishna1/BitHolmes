import tensorflow as tf
import numpy as np
import requests
import pandas as pd
import json

class AddressClassifier:
    # 1 is for sure fraud, 0 is for sure not fraud
    THRESHOLD = 0.3

    BASE_API = "https://blockchain.info/rawaddr/"
    MODEL_PATH = "dnn_model"
    STATS_PATH = "dataset_stats.json"

    ID_FEATURES = ["n_tx", "n_unredeemed", "total_received", "total_sent", "final_balance"]
    TRANSACTION_FEATURES = ["ver", "vin_sz", "vout_sz", "size", "weight", "fee", "lock_time", "time"]
    ALL_FEATURES = ID_FEATURES + TRANSACTION_FEATURES

    def __init__(self):
        self.model = tf.keras.models.load_model(self.MODEL_PATH)
        
        with open("dataset_stats1.json", "r") as o:
            dataset_stats = json.load(o)
        
        self.mean = pd.Series(dataset_stats["mean"], index=self.ALL_FEATURES, dtype=np.float64)
        self.std_dev = pd.Series(dataset_stats["std"], index=self.ALL_FEATURES, dtype=np.float64)
        
    def predict(self, address):
        all_data = self.get_data_api(address)

        if all_data == -1:
            return -1, -1

        flat_dict = self.flatten_entire_dict(all_data)
        flat_arr = self.dict_to_array(flat_dict)
        process_arr = self.preprocess(flat_arr)

        # get the average prediction from all of this key's transaction
        avg_pred = self.model.predict(process_arr).mean()

        return (avg_pred > self.THRESHOLD, str(int(avg_pred * 100)))
                 

    def get_data_api(self, address):
        url = self.BASE_API + address
        resp = requests.get(url)

        try:
            entire_dict = resp.json()
            return entire_dict
        except Exception as e:
            return -1

    def flatten_entire_dict(self, curr):
        id_dict_base = {feat: curr[feat] for feat in self.ID_FEATURES}
        tot_vals = []
        for tx in curr["txs"]:
            this_tx_vals = {}
            for tx_feat in self.TRANSACTION_FEATURES:
                this_tx_vals[tx_feat] = tx[tx_feat]
            tot_vals.append({**id_dict_base, **this_tx_vals})
        return tot_vals

    def dict_to_array(self, flat_dict):
        array = []
        for tx  in flat_dict:
            array.append([tx[feat] for feat in self.ALL_FEATURES])
        return array

    def preprocess(self, data):
        df = pd.DataFrame(data=data, columns=self.ALL_FEATURES)
        processed_df = (df - self.mean) / self.std_dev
        return processed_df


if __name__ == "__main__":
    test_address = "1JxmKkNK1b3p7r8DDPtnNmGeLZDcgPadJb"
    classifier = AddressClassifier()
    print(classifier.THRESHOLD)
    pred = classifier.predict(test_address)
    print(pred)
