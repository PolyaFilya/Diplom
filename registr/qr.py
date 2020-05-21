import qrcode

def make_qr_code(int):
    return qrcode.make(int, version="3", box_size=10, border=1)
