import sys
from PIL import Image
# from StringIO import StringIO
import pickle

#Twice the actual chunk size so we can downscale for anti-aliasing
chunkSize = 20

def crystallise(image):

    #trim the image down to the chunksize
    w,h = image.size
    newW = (w-(w%(chunkSize/2)))
    newH = (h-(h%(chunkSize/2)))
    image = image.crop((0,0,newW,newH))

    w,h = image.size

    image = image.resize((w*2,h*2), Image.ANTIALIAS)
    pixelMap = image.load()

    for x in range(0,w*2,chunkSize):
        for y in range(0,h*2,chunkSize):
            drawTopHalf(x,y,pixelMap)
            drawBottomHalf(x,y,pixelMap)

    image = image.resize((w,h), Image.ANTIALIAS)
    return image

def drawTopHalf(xOrigin, yOrigin, pixelMap):
    rgba = [0,0,0,0]
    counter = 0
    for y in range(0,chunkSize-1,4):
        for x in range(0,(chunkSize - 1 - y) - (y % 2),4):
            pixel = pixelMap[xOrigin+x,yOrigin+y]
            rgba = [sum(val) for val in zip(rgba,pixel)]
            counter+= 1

    averageChunkRGBA = [val / counter for val in rgba]

    #Change all the pixels in the group to this colour
    for y in range(chunkSize-1):
        for x in range((chunkSize - 1 - y) - (y % 2)):
            pixelMap[xOrigin+x,yOrigin+y] = tuple(averageChunkRGBA)

def drawBottomHalf(xOrigin, yOrigin, pixelMap):
    rgba = [0,0,0,0]
    counter = 0
    for y in range(1,chunkSize,4):
        for x in range(((chunkSize - 1 - y) + (y+1)%2),chunkSize,4):
            pixel = pixelMap[xOrigin+x,yOrigin+y]
            rgba = [sum(val) for val in zip(rgba,pixel)]
            counter += 1

    averageChunkRGBA = [val / counter for val in rgba]

    #Change all pixels in the group to this colour
    for y in range(1,chunkSize):
        for x in range(((chunkSize - 1 - y) + (y+1)%2),chunkSize):
            pixelMap[xOrigin+x,yOrigin+y] = tuple(averageChunkRGBA)

# blargh
image = Image.open(sys.argv[1])
image = crystallise(image)
image.save('cryst.png')
