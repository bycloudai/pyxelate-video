<p align="center">
  <img width="450" height="110" src="examples/logo.png">
</p>

Super Pyxelate converts images to 8-bit pixel art. It is an improved, faster implementation of the [original Pyxelate](https://github.com/sedthh/pyxelate/releases/tag/1.2.1) algorithm with palette transfer support and enhanced dithering. Or you can find the original version of pyxelate [here](https://github.com/sedthh/pyxelate).

This is an implemented version where you can convert **videos** and images into "pixel art". Follow this YouTube [tutorial](https://youtu.be/uCTa4NUSwBs) or if you have any questions feel free to join my [discord](https://discord.gg/sE8R7e45MV) and ask there.

![Pixel art corgi](/examples/p_corgi.png)

# Setup
This repo's codes are made for Windows. No guarantee that it'll run on Linux or MacOS. 

## Start
Clone this repository and place it anywhere you want on your PC. We'll need the file path later.

## Setup environment
We are going to use Anaconda3, download [Anaconda3](https://www.anaconda.com/products/individual) if you don't have it.  

Step 1. Create conda environment:
```
conda create -n pyxelate python=3.7
conda activate pyxelate
```
Step 2-1. Setup conda env for nvidia non-30 series GPU:
```
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
```
Step 2-2. Setup conda env for nvidia 30 series GPU:
```
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```
Step 2-3. Setup conda env for non-nvidia GPU: (Running on CPU)
```
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```
Step 3. Install the dependencies
```
cd WHERE_YOU_CLONED_THIS_REPO
pip install -r requirements.txt
pip install ffmpeg-python
```
- *To reuse the created conda environment after you close the prompt, you just need to*:
```
conda activate pyxelate
```

# Usage
I've implemented so you can run it easily on both images or videos locally. 
## Image
To run through pyxelate on a single image:
```
python image.py --input INPUT_IMAGE_PATH --palette INTEGERS --downsample_by INTEGERS
```
- `--input`: The input image file path
- `--palette`: find this many colors. Default is 7, so it'll find 7 colors. 
- `--downsample_by`: new image will be this many times smaller of the original in size. Default is 14, so it'll be 1/14th smaller.
To use the default values, you don't have to specify the arguments in the command. 

eg. 
```
python image.py --input input/china6.jpg
```
Result would be in the `output` folder.

## Video
To run through pyxelate on a single video:
```
python video.py --input INPUT_VIDEO_PATH --palette INTEGERS --downsample_by INTEGERS
```
See above for arguments explanations. 

Video will use the very first frame's palette for the rest of the video. This is to prevent new palette being created, because it'll look horrible with flickering. 

eg.
```
python video.py --input input/csgo.mp4 --palette 20 --downsample_by 6
```
Result would be in the `output` folder.

To view the video in a pixel art format, I suggest using this video player called [MPC-HC](https://github.com/clsid2/mpc-hc/releases/tag/1.9.17).

To perform the "Integer Scaling" effect, you have to go settings “View” → “Options” → “Playback” → “Output” → “Resizer” → “Nearest neighbor”. The setting is available when using rendering engines “Video Mixing Renderer 9 (renderless)”, “Enhanced Video Renderer (custom presenter)” and “Sync Renderer”. A rendering engine can be selected via the “DirectShow Video” dropdown on the same settings’ page. [*Credit*](https://tanalin.com/en/articles/integer-scaling/#h-partial-viewers)

```python
from skimage import io
from pyxelate import Pyx, Pal

# load image with 'skimage.io.imread()'
image = io.imread("examples/blazkowicz.jpg")  

downsample_by = 14  # new image will be 1/14th of the original in size
palette = 7  # find 7 colors

# 1) Instantiate Pyx transformer
pyx = Pyx(factor=downsample_by, palette=palette)

# 2) fit an image, allow Pyxelate to learn the color palette
pyx.fit(image)

# 3) transform image to pixel art using the learned color palette
new_image = pyx.transform(image)

# save new image with 'skimage.io.imsave()'
io.imsave("pixel.png", new_image)
```
![Definitely not cherry picking](/examples/p_blazkowicz.png)

Pyxelate extends scikit-learn transformers, allowing the same learned palette to be reused on other, aesthetically **similar** images (so it's somewhat like an 8-bit style transfer): 

```python
car = io.imread("examples/f1.jpg")
robocop = io.imread("examples/robocop.jpg")

# fit a model on each
pyx_car = Pyx(factor=5, palette=8, dither="none").fit(car)
pyx_robocop = Pyx(factor=6, palette=7, dither="naive").fit(robocop)

"""
pyx_car.transform(car)
pyx_car.transform(robocop)
pyx_robocop.transform(car)
pyx_robocop.transform(robocop)
"""
```
![Fit Transform Palette](/examples/p_fit_transform.png)

For a single image, it is possible to call both fit() and transform() at the same time:

```python
# fit() and transform() on image with alpha channel
trex = io.imread("examples/trex.png")
trex_p = Pyx(factor=9, palette=4, dither="naive", alpha=.6).fit_transform(trex)
```
![Transparency for sprites](/examples/p_trex.png)

## Hyperparameters for Pyx()
| Parameter | Description |
| --- | --- |
| height | The height of the transformed image. If only height is set, the width of the transofmed image will be calculated to maintain the aspect ratio of the original. |
| width | The width of the transformed image. If only width is set, the height of the transofmed image will be calculated to maintain the aspect ratio of the original. |
| factor | The size of the transformed image will be `1. / factor` of the original. **Can be used instead of setting width or height.** |
| upscale | Resizes the pixels of the transformed image by upscale. Can be a positive `int` or a tuple of ints for `(h, w)`. Default is `1`. |
| palette | The number of colors in the transformed image. <br /> - If it's an `int` that is larger than 2, Pyxelate will search for this many colors automatically. Default is `8`. <br /> - If it's a `Pal` palette enum object, Pyxelate will use palette transfer to match these colors.|
| dither | The type of dithering to use on the  transformed image (see more exampels below):<br />- `"none"` no dithering is applied (default, takes no additional time)<br />- `"naive"` Pyxelate's naive dithering based on probability mass function (use for images with **alpha channel**) <br />- `"bayer"` Bayer-like ordered dithering using a [4x4 Bayer Matrix](https://www.visgraf.impa.br/Courses/ip00/proj/Dithering1/) (fastest dithering method, use for large images)<br />- `"floyd"` Floyd-Steinberg inspired [error diffusion dithering](https://en.m.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering) (slowest)<br />- `"atkinson"` Atkinson inspired [error diffusion dithering](https://surma.dev/things/ditherpunk/) (slowest) |
| alpha | For images with transparency, the transformed image's pixel will be either visible/invisible above/below this threshold. Default is `0.6`. |
| sobel | The size of the sobel operator (N*N area to calculate the gradients for downsampling), must be an `int` larger than 1. Default is `3`, try `2` for a much faster but less accurate output. |
| depth | How many times should the Pyxelate algorithm be applied to downsample the image. More iteratrions will result in blockier aesthatics. Must be a positive `int`, although it is really time consuming and should never be more than 3. Raise it only for really small images. Default is `1`. |
| boost | Adjust contrast and apply preprocessing on the image before transformation for better results. In case you see unwanted dark pixels in your image set this to `False`. Default is `True`. |

Showcase of available dithering methods:
![Dithering methods](/examples/p_palms.png)

See more examples in [the example Jupyter Notebook](examples.ipynb).

## Assigning existing palette
Common retro palettes are available in `Pal`:

```python
from pyxelate import Pyx, Pal

vangogh = io.imread("examples/vangogh.jpg")

vangogh_apple = Pyx(factor=12, palette=Pal.APPLE_II_HI, dither="atkinson").fit_transform(vangogh)
vangogh_mspaint = Pyx(factor=6, palette=Pal.MICROSOFT_WINDOWS_PAINT, dither="none").fit_transform(vangogh)
```

![Ever wondered how classical paintings would look like in MS Paint?](/examples/p_vangogh.png)
Assign your own palette:
```python
my_pal = Pal.from_hex(["#FFFFFF", "#000000"])

# same but defined with RGB values
my_pal = Pal.from_rgb([[255, 255, 255], [0, 0, 0]])
```

Fitting existing palettes on different images will also have different results for `transform()`.

# Installation
```
pip install git+https://github.com/sedthh/pyxelate.git --upgrade
```

Pyxelate relies on the following libraries to run (included in *requirements.txt*):
- [sklearn 0.24.1](https://scikit-learn.org/stable/)
- [skimage 0.18.1](https://scikit-image.org/)
- [numba 0.53.1](https://numba.pydata.org/)
![The cathode that burns twice as bright, burns half the resolution](/examples/p_br.png)
# FAQ
The source code is available under the **MIT license** 
but I would appreciate the credit if your work uses Pyxelate (for instance you may add me in the Special Thanks section in the credits of your videogame)!

## How does it work?
Pyxelate downsamples images by (iteratively) dividing it to 3x3 tiles and calculating the orientation of edges inside them. Each tile is downsampled to a single pixel value based on the angle the magnitude of these gradients, resulting in the approximation of a pixel art. This method was inspired by the [Histogram of Oriented Gradients](https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_hog.html) computer vision technique.

Then an unsupervised machine learning method, a [Bayesian Gaussian Mixture](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.BayesianGaussianMixture.html) model is fitted (instead of conventional K-means) to find a reduced palette. The tied gaussians give a better estimate (than  Euclidean distance) and allow smaller centroids to appear and then lose importance to larger ones further away. The probability mass function returned by the uncalibrated model is then used as a basis for different dithering techniques.

Preprocessing and color space conversion tricks are also applied for better results.

## PROTIPs
- There is **no one setting fits all**, try experimenting with different parameters for better results! A setting that generates visually pleasing result on one image might not work well for another.
- The bigger the resulting image, the longer the process will take. Note that most parts of the algorithm are **O(H*W)** so an image that is twice the size will take 4 times longer to compute. 
- Assigning existing palettes will take longer for larger palettes, because [LAB color distance](https://scikit-image.org/docs/dev/api/skimage.color.html#skimage.color.deltaE_ciede2000) has to be calculated between each color separately. 
- Dithering takes time (especially *atkinson*) as they are mostly implemented in plain python with loops.
![You look like a good pixel](/examples/p_br2.png)
## TODOs
- Add CLI tool for Pyxelate so images can be batch converted from command line.
- Re-implement Pyxelate for animations / sequence of frames in video.
- Include PIPENV python environment files instead of just setup.py.
- Implement Yliluoma's ordered dithering algorithm and experiment with improving visuals through gamma correction. 
- Write a whitepaper on the Pyxelate algorithm.
