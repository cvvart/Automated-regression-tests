'''
Structured Similarity Index Measurement (SSIM)
Description: A series of functions required to compute the measure of structured
                similarity. Used for image comparisons.
Last Modified: 08/17/2018    

Requires:
pip install opencv-python (for cv2)
pip install --upgrade scikit-image (for SSIM computations)
pip install tornado
pip install nose

'''

from skimage.metrics import structural_similarity as compare_ssim
from PIL import ImageChops, Image, ImageFont, ImageDraw
import cv2
#########################################################################################
# Using the scikit-image implementation of SSIM, compute the index of
# two images
#
# baseImage                     - The benchmark image, a filepath.
#
# newImage                      - The path to an image to compare against baseImage.
#
# useGrayScale                  - A boolean. If true, then the images will be grayscaled
#                                   before the comparison. Use this if you don't care about
#                                   color deviations.
#########################################################################################
def computeSSIM(baseImage, newImage, useGrayScale):
    im_base = cv2.imread(baseImage, 0)
    im_new = cv2.imread(newImage, 0)
    if(useGrayScale):
        im_base = cv2.cvtColor(im_base, cv2.COLOR_BGR2GRAY)
        im_new = cv2.cvtColor(im_new, cv2.COLOR_BGR2GRAY)
    index = compare_ssim(im_base, im_new, channel_axis=(not useGrayScale))
    return index
#########################################################################################
# Generates a grayscale image that highlights the differences between two images.
#
# baseImage                     - The benchmark image, a filepath.
#
# newImage                      - The path to an image to compare against baseImage.
#
# diffImage                     - The path where the difference image is to be saved to.
#########################################################################################
def generateDiffImage(baseImage, newImage, diffImage):
    val = ImageChops.difference(Image.open(baseImage).convert('LA'), Image.open(newImage).convert('LA'))
    val.save(diffImage)

#########################################################################################
# Function to generate a combined image from a given benchmark, actual screenshot, and
# the difference image created from the two. 
#
# benchmark, screenshot, diff   - PIL.Image variables representing what images are to be
#                                 placed in the output image
# percentDif                    - The value for the percent difference of the two images.
#                                 This value will be shown on the resulting image.
# title                         - Any additional text. It will be placed at the bottom of
#                                 of the image.
# out                           - Path that the image will be saved to included the filename
#########################################################################################
def generateCompareResultImg(benchmark, screenshot, diff,percentDif,title, out):
    font = ImageFont.truetype("arial.ttf", (int)(benchmark.height/8.0))
    ascent, descent = font.getmetrics()
    fontHeight = ascent+descent

    newWidth = diff.width + screenshot.width
    newHeight = max(benchmark.height,screenshot.height,diff.height)*2 + (3*fontHeight)
    newImage = Image.new('RGB', (newWidth, newHeight),"white")
    newImage.paste(benchmark,(0,fontHeight))
    newImage.paste(screenshot,(benchmark.width,fontHeight))
    newImage.paste(diff,((int)(benchmark.width/2.0),benchmark.height+2*fontHeight))
    canvas = ImageDraw.Draw(newImage)

    canvas.text((0,0),"Benchmark", "black", font=font)
    canvas.text((benchmark.width+10,0),"Actual", "black", font=font)
    canvas.text((int(benchmark.width/2.0),benchmark.height+fontHeight),"Diff = %%%.2f"%percentDif,"black",font=font)
    canvas.text((0,newImage.height-fontHeight),title,"black",font=font)
    newImage.save(out)

