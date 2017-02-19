import subprocess
import glob


def getImages(image_file):
    subprocess.call("math -script pictester.m " + image_file, shell=True)
    new_names = glob.glob('./tempdir/*')
    return new_names


#image = open("grace.jpg","r+").read()
#images = getImages(image)
