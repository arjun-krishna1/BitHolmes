from qrcode import make
from time import time
import os, glob

static_path = os.path.dirname(os.path.abspath(__file__)) + "\\static"

def make_qr(data):
    code = make(data)
    name = str(time()) + ".png"
    code.save("static/" + name)
    return name

def make_website_link_qr(public_key):
    return make_qr(public_key)

def delete_old_files():
    print("checking deletions")
    print(os.listdir(static_path))
    files = os.listdir(static_path)
    png_to_float = lambda file : float(file.replace(".png", ""))
    for file in files:
        time_change = time() - png_to_float(file)
        if time_change > 86400: # a day
            os.remove(static_path + '\\' + file)
            print("removed", file)





delete_old_files()