from pyzbar.pyzbar import decode
from PIL import Image

def scanner(object):
    image = decode(Image.open(object))
    data = image[0].data
    print(data)
    data = str(data)
    c = len(data)
    n = int(data[2:c-1])
    return n