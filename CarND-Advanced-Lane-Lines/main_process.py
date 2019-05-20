#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:25:43 2019

@author: hbguo
"""

import cv2
import numpy as np
import os
import os.path as op
import camera_calibration as cc
import perspective_transform as pt
import image_process as ip
import shutil
import image_utils as iu
import lane_detection as ld
from tqdm import tqdm

mtx, dist = cc.GetCalibrationParameters()
M, M_inv = pt.GetPerspectiveTransformMatrix(mtx, dist)

left_params_record = []
right_params_record = []
smooth_left = None
smooth_right = None
moving_average_coff = 0.65

def frame_process(frame, mtx, dist, M, M_inv, restart, prior_left_params, prior_right_params):
    warped_img, undist = pt.MapPerspectiveTransformImage(frame, mtx, dist, M)
    binary = ip.Process(warped_img)
    clear_warped = iu.connection_label(binary, 100, 4)
    out_status = None
    if restart:
        out_status = False
        leftx, lefty, rightx, righty = ld.find_lane_pixels(clear_warped)
        prior_left_params, prior_right_params, left_fitx, right_fitx, ploty = \
            ld.fit_lane_line(leftx, lefty, rightx, righty, clear_warped.shape[0])
        
    else:
        prior_left_params, prior_right_params, left_fitx, right_fitx, ploty, flag = \
            ld.search_around_poly(clear_warped, prior_left_params, prior_right_params)
        out_status = flag
    if len(left_fitx) and len(right_fitx):    
        left_params_record.append(left_fitx)
        right_params_record.append(right_fitx)
        if (len(left_params_record) > 1 and len(right_params_record) > 1
            and len(left_params_record) == len(right_params_record)):
            smooth_left = moving_average_coff * left_params_record[-1] + (1-moving_average_coff) * left_params_record[-2]
            smooth_right = moving_average_coff * right_params_record[-1] + (1-moving_average_coff) * right_params_record[-2]
        else :
            smooth_left = left_params_record[-1]
            smooth_right = right_params_record[-1]
            
        while len(left_params_record) > 2:
            left_params_record.pop(0)
        
        while len(right_params_record) > 2:
            right_params_record.pop(0)
        
        blp, brp, best_left, best_right, best_y = ld.fit_poly(clear_warped.shape, smooth_left, ploty, smooth_right, ploty)
    
        warped_back = ld.DrawBack(binary, best_left, best_right, best_y, M_inv, undist)
        curvature_radius, offset_road_center = ld.measure_curvature_real(best_left, best_right, best_y)
        out_str = 'Curvature radius: '+ str(curvature_radius)+ 'm'
        cv2.putText(warped_back, out_str, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)
        out_offset = ''
        if offset_road_center > 0:
            out_offset = 'Right of center: '+ str(offset_road_center) + 'm'
        else:
            out_offset = 'Left of center: ' + str(-offset_road_center) + 'm'
            
        cv2.putText(warped_back, out_offset, (50, 90),  cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)
        return warped_back, out_status, blp, brp
    else:
        return undist, out_status, prior_left_params, prior_right_params
    
src_video = './videos/project_video.mp4'
dst_video = './videos/result.mp4'

videoCapture = cv2.VideoCapture(src_video)
fps = videoCapture.get(cv2.CAP_PROP_FPS)
frame_size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

total_frame_count = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

video_writer = cv2.VideoWriter(dst_video, cv2.VideoWriter_fourcc('M','J','P','G') , fps, frame_size)

restart = True
prior_left_params = None
prior_right_params = None
while True:
    success, frame = videoCapture.read()    
    if not success:
        break
    output, restart, prior_left_params, prior_right_params= \
     frame_process(frame, mtx, dist, M, M_inv, restart, prior_left_params, prior_right_params)
    video_writer.write(output)
    
video_writer.release()
