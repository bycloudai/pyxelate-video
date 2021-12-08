from skimage import io
from pyxelate import Pyx, Pal
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="",help='Locate the input image')
parser.add_argument('--downsample_by', type=int, default=14,help='Specify down sample size')
parser.add_argument('--palette', type=int, default=7,help='Specify palette colors')
args = parser.parse_args()



# load image with 'skimage.io.imread()'
image = io.imread(args.input)  

downsample_by = args.downsample_by  # if 14, new image will be 1/14th of the original in size
palette = args.palette  # if 7, find 7 colors

# 1) Instantiate Pyx transformer
pyx = Pyx(factor=downsample_by, palette=palette)

# 2) fit an image, allow Pyxelate to learn the color palette
pyx.fit(image)

# 3) transform image to pixel art using the learned color palette
new_image = pyx.transform(image)

# save new image with 'skimage.io.imsave()'
io.imsave("output/"+"".join("".join(args.input.split("/")[1:]).split(".")[:1])+".png", new_image)