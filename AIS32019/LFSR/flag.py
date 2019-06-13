from PIL import Image, ImageDraw, ImageFont 
  
img = Image.new('RGB', (377, 30), color = (255, 255, 255)) 
  
fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15) 
d = ImageDraw.Draw(img) 
d.text((10,6), "AIS3{LFSR_i5_f0r_Linear_f33dback_shift_Re6isterrrr}", font=fnt, fill=(0, 0, 0)) 
  
img.save('flag.png')