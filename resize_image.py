
from PIL import Image
image = Image.open('bmw2.jpg')
new_image = image.resize((32, 32))
new_image.save('bmw2.jpg')

print(image.size)
print(new_image.size)
