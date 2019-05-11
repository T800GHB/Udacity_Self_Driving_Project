# **Finding Lane Lines on the Road** 


---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
- [x] Make a pipeline that finds lane lines on the road
- [x] Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./test_images_output/solidWhiteCurve.jpg "detect example1"
[image2]: ./test_images_output/solidWhiteRight.jpg "detect example2"

---

### Reflection

### 1. Description of current pipeline.

My pipeline consisted of 5 steps. 
1. I converted the images to grayscale.
2. I use gaussian_blur function to smooth image.
3. I use canny edge detector to find all gradient changes in the image
4. I use a ROI to restrict area in the image
5. I use hough transfrom to find all lines in image with specific paramters,
   In this module , there are many small steps need to describe:
    1. Seprate lines as left group or right group by slope
    2. Delete lines which those definitely short in current group
    3. Delete lines with abnormal slope
    4. Fit line for each group
    5. Draw line on a blank image
6. Merge detected result to original color image

Detected lane line like thhis: 

![alt text][image1]
![alt text][image2]


### 2. Identify potential shortcomings of current pipeline


- Current line detection will restrict to identify stright line

- Light condition is very important to this algorithm

- The lane line could not be detected which far from ego car, so fit result is not precise


### 3. Suggest possible improvements to current pipeline

* Zoom in central part of image to find lane line far from ego car
* Use other color space to be insensitive for light condition
* Use another polynomial to fit lane line with curve
