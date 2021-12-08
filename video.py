from skimage import io
from pyxelate import Pyx, Pal
import os
import ffmpeg
import cv2
import shutil
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--downsample_by', type=int, default=14,help='Specify down sample size')
	parser.add_argument('--palette', type=int, default=7,help='Specify palette colors')
	args = parser.parse_args()


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

	downsample_by = args.downsample_by
	palette = args.palette
	pyx = Pyx(factor=downsample_by, palette=palette)


	for filename in os.listdir("input"):
			video = cv2.VideoCapture("input/" + filename)
			fps = video.get(cv2.CAP_PROP_FPS)
		if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
			clean_filename = ".".join(filename.split(".")[:-1])
			os.system("ffmpeg -i {0} -vf fps={1} temp/{2}%d.png".format("input/"+filename, fps, clean_filename))
		else:
			continue
		# print(filename)

	count = 0
	first = True
	for filename in os.listdir("temp"):
		clean_filename = ".".join(filename.split(".")[:-1])

		if (filename.endswith(".png")):
			image = io.imread("temp/" + filename)
			if first:
				pyx.fit(image)
				first = False
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