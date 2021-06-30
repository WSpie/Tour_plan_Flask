import base64


def img_base64(img_path):
    with open(img_path, 'rb') as img_f:
        img = img_f.read()
    return base64.b64encode(img).decode()