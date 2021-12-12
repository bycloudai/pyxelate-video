from skimage import io
from pyxelate import Pyx, Pal
import os
import ffmpeg
import cv2
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="",help='Locate the input video')
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

video_location = args.input # input/csgo.mp4
if "/" in video_location:
	video_file = "".join(args.input.split("/")[-1:]) # csgo.mp4
else:
	video_file = video_location
video_filename = ".".join(video_file.split(".")[:-1]) # csgo


video = cv2.VideoCapture(video_location)
fps = video.get(cv2.CAP_PROP_FPS)
os.system("ffmpeg -i {0} -vf fps={1} temp/{2}%d.png".format(video_location, fps, video_filename))


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
	os.system("ffmpeg -i {0} -vf \"fps={1},pad=ceil(iw/2)*2:ceil(ih/2)*2\" -c:v libx264 -pix_fmt yuv420p output/{2}_output_d{3}_p{4}.mp4".format("temp_output/"+video_filename+"%d.png", fps, video_filename,str(downsample_by),str(palette)))
	break

shutil.rmtree('temp')
shutil.rmtree('temp_output')