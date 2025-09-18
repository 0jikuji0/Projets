#pip install rembg
from rembg import remove 
from PIL import Image
input_path = 'NameImage.jpg'
outputpath = 'NameImage.png'
inp = Image.open(input_path)
output = remove(inp)
output.save(outputpath)
Image.open(outputpath)