from PIL import Image, ImageDraw, ImageFont

# setting
command = input()
size = 128
n = len(command)*size//2*3
m = size

# make a blank image for the text
image = Image.new('RGB', (n, m),(255,255,255))

# getting env
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("Helvetica", size)

# draw text, half opacity
draw.text((0,0),command,font=font, fill=(0,0,0))

image.save('{}.jpg'.format(command.split()[0]))
