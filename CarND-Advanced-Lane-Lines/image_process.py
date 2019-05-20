#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 07:57:56 2019

@author: hbguo
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
    # Calculate directional gradient
    # Apply threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel = None
    if orient == 'x':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    elif orient == 'y':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    else:
        pass
    abs_sobel = np.absolute(sobel)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    return binary_output

def lab_b_thresh(img, thresh=(195, 255)):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    lab_b = lab[:,:,2]
    binary_output = np.zeros_like(lab_b)
    # don't normalize if there are no yellows in the image
    if np.max(lab_b) > 150:
        lab_b = lab_b*(255/np.max(lab_b))
        
        binary_output[((lab_b > thresh[0]) & (lab_b <= thresh[1]))] = 1
        return binary_output
    else:
        return binary_output

def hls_thresh(img, thresh=(210, 255), s_thresh=(170, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    l_channel = l_channel*(255/np.max(l_channel))
    
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    l_binary = np.zeros_like(l_channel)
    l_binary[(l_channel > thresh[0]) & (l_channel <= thresh[1])] = 1
    return l_binary

# Edit this function to create your own pipeline.
def Process(img, s_thresh=(170, 255), sx_thresh=(30, 100)):
    # Sobel xs
    sxbinary = abs_sobel_thresh(img, 'x', sx_thresh[0], sx_thresh[1])
    hls_binary = hls_thresh(img)
    lab_binary = lab_b_thresh(img)
    # Stack each channel
    combined_binary = np.zeros_like(sxbinary)
    combined_binary[(sxbinary == 1) | (hls_binary == 1) | (lab_binary == 1)] = 1
    
    # Under the current threshold setting for perspective transform, 
    # Clear useless detected edge by Sobel 
    combined_binary[660:720, 0:150] = 0
    combined_binary[660:720, 1100:1280] = 0
    # Clear noise before ego-vehicle
    combined_binary[600:720, 500: 800] = 0
    return combined_binary
    
def show_result(img, s_thresh=(170, 255), sx_thresh=(30, 100)):
    img = np.copy(img)
    # Convert to HLS color space and separate the V channel
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    h_channel = hls[:,:,0]
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    # Sobel xs
    sxbinary = abs_sobel_thresh(l_channel, 'x', 3, sx_thresh[0], sx_thresh[1])
    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    h_binary = np.zeros_like(h_channel)
    h_binary[(h_channel >= 10) & (h_channel <=120)] = 1
    # Stack each channel
    color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
    combined_binary = np.zeros_like(sxbinary)
#    combined_binary[((s_binary == 1) | (sxbinary == 1)) & (h_binary == 1)] = 1
    combined_binary[(s_binary == 1) | (sxbinary == 1)] = 1

#     Plot the result
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    
    ax1.imshow(image)
    ax1.set_title('Original Image', fontsize=40)
    
    ax2.imshow(color_binary)
    ax2.set_title('Pipeline Result', fontsize=40)
    plt.gray()
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    
