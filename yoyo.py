import subprocess

def getImages(image_file):
    subprocess.call(['math', '-script', 'pictester.m', str(image_file)])
    image_names = subprocess.check_output(['ls','tempdir/'])
    new_names = []
    for image_name in image_names:
        new_names.append('tempdir/'+image_name)
    return new_names

#image = open("grace.jpg","r+").read()
#images = getImages(image)
