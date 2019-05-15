#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 08:24:44 2019

@author: hbguo
"""

import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

def GetCalibrationParameters(show_corners=False, show_undistorted=False):

    nx = 9
    ny = 6
    
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    
    objp = np.zeros((nx*ny,3), np.float32)
    objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)
    
    images = glob.glob('camera_cal/calibration*.jpg')
    show_img = cv2.imread('camera_cal/calibration1.jpg')
    img_size = (show_img.shape[1], show_img.shape[0])
    
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            if show_corners: 
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
                #write_name = 'corners_found'+str(idx)+'.jpg'
                #cv2.imwrite(write_name, img)
                cv2.imshow('img', img)
                cv2.waitKey(500)
      
    if show_corners:
        cv2.destroyAllWindows()
    
    
    # Do camera calibration given object points and image points
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)
    undistorted = cv2.undistort(show_img, mtx, dist, None, mtx)
    
    if show_undistorted:
        #cv2.imwrite('output_images/test_undist.jpg',undistorted)
        
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
        f.tight_layout()
        ax1.imshow(show_img)
        ax1.set_title('Original Image', fontsize=50)
        ax2.imshow(undistorted)
        ax2.set_title('Undistorted Image', fontsize=50)
        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.savefig('output_images/calibration_undistorted.png')
        
    return mtx, dist
