import numpy as np
from PIL import Image
image = np.array(Image.open( "misc1.png"))
image = image[259:359,:]


# for i in range(2,98,2):
#     if i%2 != 0 :
#         image[i] = np.array([0]*384)
#     up = image[i-2,:]
#     line = image[i,:]
#     down = image[i+2,:]
#     for x in range(383):
#         diff = np.sum(np.power(np.roll(line,x) - up,2)) + np.sum(np.power(np.roll(line,x) - down,2))
#         if diff < minimum :
#             minimum = diff 
#             mini_idx = x
#     image[i] = np.roll(image[i,:],mini_idx)

# for i in range(1,383):
#     minimum = 1e10
#     mini_idx = 1e10
#     left = image[:,i-1]
#     line = image[:,i]
#     right = image[:,i+1]
#     for j in range(100):
#         diff = np.sum(np.power(np.roll(line,j) - left,2)) + np.sum(np.power(np.roll(line,j) - right,2))
#         if diff < minimum :
#             minimum = diff 
#             mini_idx = j

#     image[:,i] = np.roll(line,mini_idx)

# for i in range(100):
#     image[i] = (image[i,:] == 3) * 255



# for x in range(384) :
#     for i in range(100):
#         image[i] = np.roll(image[i],i*33+10)

# # for i in range(100):
#     image[i] = (image[i,:] == 0) * 255

# img = Image.fromarray(image)
# #     img.save('TMPimage/image'+ str(x) + '.png')
# #     # img.save('test.png')
# img.show()


# # 161 204 222 352



image = np.array(Image.open( "image336.png"))

# for x in range(384) :
for i in range(0,100):
    if i%2 == 1 :
        image[i] = np.array([255]*384)
    # image[i] = np.roll(image[i],)
    img = Image.fromarray(image)
    img.save('evenimg.png')

img.show()

# EOF{Messageln}