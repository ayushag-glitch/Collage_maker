# from skimage.color import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from skimage import feature
from skimage import io
from skimage import util

import glob

def CollageCreate(AddressofFolder):
  image_dict={}
  for filename in glob.glob(AddressofFolder):
    image_dict[filename]=io.imread(filename)
  hsv_dict={}
  greenpercentage_dict={}
  # img_height=len(image_dict["image1.png"])
  # img_width=len(image_dict["image1.png"][0])
  for key in image_dict:
    temp=0
    hsv_dict[key]=(rgb2hsv((image_dict[key][:,:,:3])/255)*360)
    for tick1 in hsv_dict[key]:
      for tick2 in tick1:
        if tick2[0]>121 and tick2[0]<180:
          temp=temp+1
    greenpercentage_dict[key]=(temp*100)/(len(image_dict[key])*len(image_dict[key][0]))

  greenpercentage_dict=dict(sorted(greenpercentage_dict.items(), key=lambda item: item[1]))
  edge_perc_dict={}
  for key in image_dict:
    temp=rgb2gray(image_dict[key])
    temp = feature.canny(temp,sigma = 3) 
    edge_perc_dict[key] = 100*np.count_nonzero(temp)/(len(temp)*len(temp[0]))

  edge_perc_dict= dict(sorted(edge_perc_dict.items(), key=lambda item: item[1]))
  green_perc_keys=list(greenpercentage_dict.keys())
  upper_row=green_perc_keys[0:3]
  lower_row=green_perc_keys[3:6]

  upper_row.sort(key=lambda x: edge_perc_dict[x])
  lower_row.sort(key=lambda x: edge_perc_dict[x])
  upper_row.extend(lower_row)
  final_order=upper_row
  image_array=[]
  for tick in final_order:
    image_array.append(image_dict[tick][:,:,:3])
  image_array=np.array(image_array)
  collage = util.montage(image_array, fill='mean', rescale_intensity=False, grid_shape=(2,3), padding_width=0, multichannel=True)
  io.imsave('collagecreate.png', collage)
  print("Image Saved as collagecreate.png")
  return collage
# skimage.io.imshow(collage)

img_dir = './assignment1/*.png'
collage = CollageCreate(img_dir)
io.imshow(collage)