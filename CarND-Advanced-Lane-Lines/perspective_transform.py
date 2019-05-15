#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 08:03:15 2019

@author: hbguo
"""

import camera_calibration
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def GetPerspectiveTransformMatrix(mtx, dist):
    # This region make sense on image size of 720P
    src_pt1 = (576, 463)
    src_pt2 = (707, 463)
    src_pt3 = (1044, 676)
    src_pt4 = (262, 676)
    
    dst_pt1 = (320, 0)
    dst_pt2 = (960, 0)
    dst_pt3 = (960, 719)
    dst_pt4 = (320, 719)
    src_pts = np.float32([src_pt1, src_pt2, src_pt3, src_pt4])
    dst_pts = np.float32([dst_pt1, dst_pt2, dst_pt3, dst_pt4])
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
    return M

def GetPerspectiveTransformImage(file_name, mtx, dist, M):
    img = cv2.imread(file_name)
    
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    
    img_size = (img.shape[1], img.shape[0])
    
    warped = cv2.warpPerspective(undistorted_img, M, img_size, flags=cv2.INTER_LINEAR) 
    
    return warped

def DisplayPerspectiveTransform(file_name, mtx, dist):
    img = cv2.imread(file_name)
    
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
        
    src_pt1 = (576, 463)
    src_pt2 = (707, 463)
    src_pt3 = (1044, 676)
    src_pt4 = (262, 676)
    green = (0, 255, 0)
    
    dst_pt1 = (320, 0)
    dst_pt2 = (960, 0)
    dst_pt3 = (960, 719)
    dst_pt4 = (320, 719)
    img_size = (1280, 720)
    
    src_pts = np.float32([src_pt1, src_pt2, src_pt3, src_pt4])
    dst_pts = np.float32([dst_pt1, dst_pt2, dst_pt3, dst_pt4])
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(undistorted_img, M, img_size, flags=cv2.INTER_LINEAR) 
    
    
    pts = [src_pt1, src_pt2, src_pt3, src_pt4, src_pt1]
    for i in range(4):
        cv2.line(undistorted_img, pts[i], pts[i + 1], green, 3)
    
    cv2.line(warped, dst_pt1, dst_pt4, green, 3)
    cv2.line(warped, dst_pt2, dst_pt3, green, 3)   
    
    cv2.imshow('undistorted_img',undistorted_img)
    out_undist = 'output_images/undistorted_img.jpg'
    out_bv = 'output_images/brid_view.jpg'
    cv2.imwrite(out_undist, undistorted_img)
    cv2.imwrite(out_bv, warped)
    
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    ax1.imshow(mpimg.imread(out_undist))
    ax1.set_title('Original Image', fontsize=50)
    ax2.imshow(mpimg.imread(out_bv))
    ax2.set_title('Undistorted Image', fontsize=50)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    plt.savefig('output_images/calibration_undistorted.png')
        

mtx, dist = camera_calibration.GetCalibrationParameters()
#DisplayPerspectiveTransform('test_images/straight_lines1.jpg', mtx, dist, True)
M = GetPerspectiveTransformMatrix(mtx, dist)
img = GetPerspectiveTransformImage('test_images/straight_lines1.jpg', mtx, dist, M)
cv2.imwrite('t.jpg',img)