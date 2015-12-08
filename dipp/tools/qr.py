import qrcode

def make_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('Some data')
    qr.make(fit=True)

    return qr.make_image()


if __name__ == '__main__':
    img = make_qr_code('http:www.hbz-nrw.de')
    print dir(img)
