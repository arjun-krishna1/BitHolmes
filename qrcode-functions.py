from qrcode import make

def make_qr(data, name = "qr-code.png"):
    code = make(data)
    code.save(name)

def make_website_link_qr(public_key, name = "qr-code.png"):
    make_qr(public_key, name)



    
