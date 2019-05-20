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
    src_pt1 = (580, 460)
    src_pt2 = (700, 460)
    src_pt3 = (1096, 720)
    src_pt4 = (200, 720)
    
    
    dst_pt1 = (300, 0)
    dst_pt2 = (950, 0)
    dst_pt3 = (950, 720)
    dst_pt4 = (300, 720)
    src_pts = np.float32([src_pt1, src_pt2, src_pt3, src_pt4])
    dst_pts = np.float32([dst_pt1, dst_pt2, dst_pt3, dst_pt4])
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    M_inv = cv2.getPerspectiveTransform(dst_pts, src_pts)
    
    return M, M_inv

def GetPerspectiveTransformImage(file_name, mtx, dist, M):
    img = cv2.imread(file_name)
    
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    
    img_size = (img.shape[1], img.shape[0])
    
    warped = cv2.warpPerspective(undistorted_img, M, img_size, flags=cv2.INTER_LINEAR) 
    
    return warped

def MapPerspectiveTransformImage(img, mtx, dist, M):
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    
    img_size = (img.shape[1], img.shape[0])
    
    warped = cv2.warpPerspective(undistorted_img, M, img_size, flags=cv2.INTER_LINEAR) 
    
    return warped, undistorted_img

def DisplayPerspectiveTransform(file_name, mtx, dist):
    img = cv2.imread(file_name)
    
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    
    img_size = (1280, 720)
    green = (0, 255, 0)
    src_pt1 = (580, 460)
    src_pt2 = (700, 460)
    src_pt3 = (1096, 720)
    src_pt4 = (200, 720)
    
    
    dst_pt1 = (300, 0)
    dst_pt2 = (950, 0)
    dst_pt3 = (950, 720)
    dst_pt4 = (300, 720)
    
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
        
