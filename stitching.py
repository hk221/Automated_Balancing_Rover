import cv2
import glob
import matplotlib.pyplot as plt
import math

# Read Images and append into list

imagefiles = glob.glob("boat/*")
imagefiles.sort()

images = []
for filename in imagefiles:
  img = cv2.imread(filename)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  images.append(img)

num_images = len(images)

# Display Images
#plt.figure(figsize=[30,10]) 
#num_cols = 3
#num_rows = math.ceil(num_images / num_cols)
#for i in range(0, num_images):
#  plt.subplot(num_rows, num_cols, i+1) 
#  plt.axis('off')
#  plt.imshow(images[i])

# Stitch Images
stitcher = cv2.Stitcher_create()
status, result = stitcher.stitch(images)
if status == 0:
  plt.figure(figsize=[30,10]) 
  plt.imshow(result)