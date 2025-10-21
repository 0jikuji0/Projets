import qrcode
from PIL import Image

data = input("Enter the data to encode in the QR code: ")

# Création du QR Code
qr = qrcode.QRCode(
    version=3, 
    box_size=10, 
    border=4
)
qr.add_data(data)
qr.make(fit=True)

# Génération et sauvegarde du QR code
img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode.png")

# Ouvrir le QR code avec PIL
img = Image.open("qrcode.png")
img.show()
