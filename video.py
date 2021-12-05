from skimage import io
from pyxelate import Pyx, Pal
import os
import ffmpeg
import cv2
import glob
import shutil


# # load image with 'skimage.io.imread()'
# image = io.imread("examples/blazkowicz.jpg")  

# downsample_by = 5  # new image will be 1/14th of the original in size
# palette = 7  # find 7 colors

# # 1) Instantiate Pyx transformer
# pyx = Pyx(factor=downsample_by, palette=palette)

# # 2) fit an image, allow Pyxelate to learn the color palette
# pyx.fit(image)

# # 3) transform image to pixel art using the learned color palette
# new_image = pyx.transform(image)

# # save new image with 'skimage.io.imsave()'
# io.imsave("pixel.png", new_image)

files = os.listdir()
if 'temp_output' in files:
	shutil.rmtree('temp_output')
if 'temp' in files:
	shutil.rmtree('temp')
files = os.listdir()
if 'temp_output' not in files:
	os.makedirs('temp_output')
if 'temp' not in files:
	os.makedirs('temp')

downsample_by = 5
palette = 20
pyx = Pyx(factor=downsample_by, palette=palette)

for filename in os.listdir("input"):
	video = cv2.VideoCapture("input/" + filename)
	fps = video.get(cv2.CAP_PROP_FPS)
	# print(fps, filename)
	if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
		clean_filename = ".".join(filename.split(".")[:-1])
		os.system("ffmpeg -i {0} -vf fps={1} temp/{2}%d.png".format("input/"+filename, fps, clean_filename))
	else:
		continue
	# print(filename)

count = 0
for filename in os.listdir("temp"):
	clean_filename = ".".join(filename.split(".")[:-1])

	if (filename.endswith(".png")):
		image = io.imread("temp/" + filename)
		pyx.fit(image)
		new_image = pyx.transform(image)
		io.imsave("temp_output/"+clean_filename+".png", new_image)
		count += 1
	print(clean_filename, "frame: "+str(count), "done")

for filename in os.listdir("temp_output"):
	clean_filename = ".".join(filename.split(".")[:-1])
	clean_filename2 = clean_filename.rstrip("1")
	os.system("ffmpeg -i {0} -vf fps={1} -pix_fmt yuv420p output/{2}_output.mp4".format("temp_output/"+clean_filename2+"%d.png", fps, clean_filename2))
	break

shutil.rmtree('temp')
shutil.rmtree('temp_output')