#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 07:57:56 2019

@author: hbguo
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


image = mpimg.imread('test_images/test5.jpg')

def abs_sobel_thresh(gray, orient='x', sobel_kernel=3, thresh_min=0, thresh_max=255):
    # Calculate directional gradient
    # Apply threshold
    sobel = None
    if orient == 'x':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    elif orient == 'y':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    else:
        pass
    abs_sobel = np.absolute(sobel)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    return binary_output

def mag_thresh(gray, sobel_kernel=3, mag_thresh_min=0, mag_thresh_max=255):
    # Calculate gradient magnitude
    # Apply threshold
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    sobelxy = np.sqrt(sobelx**2 + sobely**2)
    scaled_sobel = np.uint8(255*sobelxy/np.max(sobelxy))
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= mag_thresh_min) & (scaled_sobel <= mag_thresh_max)] = 1
    return binary_output

def dir_threshold(gray, sobel_kernel=3, thresh_min=0, thresh_max=np.pi/2):
    # Calculate gradient direction
    # Apply threshold
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    direction_img = np.arctan2(abs_sobely, abs_sobelx)
    binary_output = np.zeros_like(direction_img)
    binary_output[(direction_img >= thresh_min) & (direction_img <= thresh_max)] = 1
    return binary_output

# Edit this function to create your own pipeline.
def pipeline(img, s_thresh=(180, 255), sx_thresh=(20, 100)):
    img = np.copy(img)
    # Convert to HLS color space and separate the V channel
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    # Sobel x
#    sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
#    abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
#    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
#    # Threshold x gradient
#    sxbinary = np.zeros_like(scaled_sobel)
#    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
    sxbinary = abs_sobel_thresh(l_channel, 'x', 3, sx_thresh[0], sx_thresh[1])
#    sxbinary = mag_thresh(l_channel, 3, 30, 100)
    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    # Stack each channel
    color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
    combined_binary = np.zeros_like(sxbinary)
    combined_binary[(s_binary == 1) | (sxbinary == 1)] = 1
    return color_binary
    
result = pipeline(image)

# Plot the result
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()

ax1.imshow(image)
ax1.set_title('Original Image', fontsize=40)

ax2.imshow(result)
ax2.set_title('Pipeline Result', fontsize=40)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)