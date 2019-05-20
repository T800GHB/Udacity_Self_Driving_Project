## Advanced-Lane-Lines writeup

### This file will describe how to detected lane line

---

**Advanced Lane Finding Project**

The steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Apply a perspective transform to rectify color image ("birds-eye view").
* Use color transforms, Sobel edge detector , connection region label to create a thresholded binary image.
* Detect lane pixels and fit to find the lane boundary.
* Apply look ahead filter to detect lane line from pervious peremeters
* Apply moving average to smooth detect output
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/calibration_undistorted.png "Undistorted"
[image2]: ./output_images/road_undistorted.png "Road Transformed"
[image3]: ./output_images/road_region.jpg "road region"
[image4]: ./output_images/brid_view.jpg "brid view"
[image5]: ./output_images/input_undist.jpg "input_undist"
[image6]: ./output_images/input_bv.jpg "input_bv"
[image7]: ./test_images/straight_lines1.jpg "input_original"
[image8]: ./output_images/sobelx.jpg "sobelx"
[image9]: ./output_images/hls.jpg "hls"
[image10]: ./output_images/lab_b.jpg "lab_b"
[image11]: ./output_images/combine.jpg "combine"
[image12]: ./output_images/connection_label.jpg "connection_label"
[image13]: ./output_images/fit_line.png "fit_line"
[image14]: ./output_images/final_output.jpg "final output"
[video1]: ./video/project_video.mp4 "original video"
[video2]: ./video/result.mp4 "result video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

The start script is main_process.py
This file will load video and provide single frame to process and write result image to a new video
frame_process() contain a base pipeline to handle single frame. 

---

### Writeup / README

#### 1. Provide a Writeup that includes all the rubric points and how you addressed each one.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how to computed the camera matrix and distortion coefficients. There is an example of a distortion corrected calibration image.

Camera calibration procedure contained in camera_calibration.py  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `GetPerspectiveTransformMatrix()`, which appears in the file `perspective_transform.py.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `DisplayPerspectiveTransform()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

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


This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 580, 460      | 300, 0        | 
| 700, 460      | 950, 0      |
| 1096, 720     | 950, 720      |
| 200, 720      | 300, 720       |

The selection region like this:
![alt text][image3]

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 3. Describe how (and identify where in your code) i used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
Before i use image process method, is use calibration to get undistorted image in MapPerspectiveTransformImage(), implementation at perspective_transform.py
take the input:
![alt text][image7]
use calibration parameters to produce undistorted image:
![alt text][image5]
use perspective matrix to generate brid view image :
![alt text][image6]

I used a combination of color and gradient thresholds to generate a binary image, all the steps contained in image_process.py
The main step of  image process is (implementation is Process()):
    1. I use sobel edge detector on x direction, accept threshold set from 30 to 100(abs_sobel_thresh() in in image_process.py)
![alt text][image8]
    2. I use HLS color space to get L channel, in this channel, set threshold from 210 to 255 to find bright white part(hls_thresh() in in image_process.py)
![alt text][image9]
    3. I use Lab color space to get b channel, in this channel, set threshold from 195 to 255 to find bright yellow part(lab_b_thresh() in in image_process.py)
![alt text][image10]
    4. I combine 3 of above result to get binary output image, and delete some noise in combine image(Process() in in image_process.py)
![alt text][image11]
    5. I use connection region label to find the small area region of the binary image as noise, then delete all of them as  area threshold 150 pixels(connection_label() in image_utils.py)
![alt text][image12]
    At this point, I get a final output of image process
#### 4. Describe how to identified lane-line pixels and fit their positions with a polynomial
    This part of function implemented in file lane_detection.py
    The main step of lane detection is following step:
    1. Get histogram of bottom of binary from image process output (in method find_lane_pixels())
    2. Find the peak of histogram to locate the start search position (in method find_lane_pixels())
    3. Use slide windows to find all pixel belong to lane line (in method find_lane_pixels())
    4. Use pixels x,y position to fit 2nd order polynomal
![alt text][image13]

    In the sequence of frames, use lane parameter from previous procedure to start search pixel belong to lane, this implemention at search_around_poly()
    I will record most two recent parameters, use moving average to smooth final output
    If there is detection failed with prior parameter, detection lane line from full image will be restarted.


#### 5. Describe how to calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I define a factor from pxiel to real world, in my code lane_detection.py with measure_curvature_real() method


ym_per_pix = 30/720 # meters per pixel in y dimension
xm_per_pix = 3.7/700 # meters per pixel in x dimension

I convert all fit points to real world and fit 2nd polynomial in read world data, save new parameter as
left_fit_cr and right_fit_cr

and use max value of y to calculate left and right curvature
by formla:

left_curverad = (np.sqrt((1 + ( 2 * left_fit_cr[0] * y_eval + left_fit_cr[1]) ** 2) ** 3)
                    / abs(2 * left_fit_cr[0])) 
right_curverad = (np.sqrt((1 + ( 2 * right_fit_cr[0] * y_eval + right_fit_cr[1]) ** 2) ** 3)
                / abs(2 * right_fit_cr[0]))  

I use output curveture from left and right, to calculate mean of them as final output curveture

I get nearest lane line point from left and right lane line intersec with bottom of image as center of road
I get bottom center of image as car center
Then i get the depature of road center by (road_center - car_center)

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lanne_detection.py in the function DrawBack().  
Here is an example of my result on a test image:

![alt text][image14]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a test video
./video/project_video.mp4
The lane detection output video
./video/result.mp4

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

The main problem of lane detection is image process, when the algorithm face to shade of tree or road with different color, here are so much noise to affect final output.

Sometimes it will make algorithm crash.

In some sence, my algorithm will fialed:
1. Lane line with other color, like green or blue
2. Lane line cover by car or something else on raod
3. So brighe light condition, can't find lane line from image
4. In the night
5. At the road intersection
6. Very large curvature
7. Poor lane line condition on the road
8. Rain day or other bad weather
9. Switch between flatten road and ramp

There are some ideas to make my algorithm more robust:
1. Try more color space
2. Track lane line on more than two frame
3. Use deep learning semantic segmentation to detect lane line