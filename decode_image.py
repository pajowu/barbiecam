import cv2
import numpy as np
from PIL import Image

from matplotlib import pyplot as plt

imcols = 164
imrows = 126
imsize = imcols * imrows

with open("test.bin", "rb") as f:
    data = f.read()

bayer_img = np.frombuffer(data, np.dtype("u1"), imsize).reshape(
    (imrows * 2, imcols // 2)
)
# bayer_img = np.frombuffer(data[82:], np.dtype("u1"), imsize).reshape(
#     (imrows * 2, imcols // 2)
# )[::2]
# bayer_img = np.concatenate((bayer_img[::-1, -1:], bayer_img[:, :-1]), axis=1)
# testarray = np.zeros((164, 120))
# testarray[(0::2), (0::2)] = 0
# testarray =

# print(bayer_img.shape)
# plt.imshow(bayer_img)
# plt.show()
# colour = cv2.cvtColor(bayer_img, cv2.COLOR_BAYER_BG2BGR)
# plt.imshow(colour)
# plt.show()

# testarray = np.zeros((164, 120))
# OFF = 7
# for y in range(imrows):
#     xoff = 0
#     for x in range(imcols):
#         if ((y & 1) == 0) and (x >= (imcols / 2)):
#             off = y * imcols + x + OFF
#             print(xoff)
#             testarray[xoff + 1 + 2, y // 2] = data[off]
#             xoff += 1

# print(testarray)
# im = Image.fromarray(testarray.astype(np.uint8))
# im.save("test.bmp")

testarray = np.zeros((imrows, imcols), dtype="u1")

# red = bayer_img[::2, : imcols // 2]
# print(f"{testarray[::2, ::2].shape}")
testarray[::2, ::2] = bayer_img[::4]
testarray[1::2, ::2] = bayer_img[::4]
testarray[::2, 1::2] = bayer_img[::4]
testarray[1::2, 1::2] = bayer_img[::4]
# colour = cv2.cvtColor(testarray, cv2.COLOR_BAYER_RGGB2RGB)
# plt.imshow(colour)
# plt.show()

# print(testarray.shape)
im = Image.fromarray(testarray.astype(np.uint8))
# im = Image.fromarray(bayer_img.astype(np.uint8))
im.save("test.bmp")

colour = cv2.cvtColor(testarray, cv2.COLOR_BAYER_RGGB2RGB)
im = Image.fromarray(colour.astype(np.uint8))
# im = Image.fromarray(bayer_img.astype(np.uint8))
im.save("test.bmp")
