# **Behavioral Cloning** 

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./images/model.png "Model Visualization"
[image2]: ./images/crop.jpg "crop"
[image3]: ./images/gamma.jpg "gamma"
[image4]: ./images/resize.jpg "resize"
[image5]: ./images/center.jpg "center"
[image6]: ./images/left.jpg "left"
[image7]: ./images/right.jpg "right"
[image8]: ./images/flip.jpg "flip"
[image9]: ./images/left_shear.jpg "left_shear"
[image10]: ./images/right_shear.jpg "right_shear"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of a convolution neural network with 3x3 filter sizes and depths between 24 and 64 (model.py lines 16-58) 

The model includes RELU layers to introduce nonlinearity (code line 14), and the data is normalized in the model using a Keras lambda layer (code line 18). 

#### 2. Attempts to reduce overfitting in the model

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 10-16). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 61), the inital learning rate set as 1e-4.
I just train model 1 epoch

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road, I adjust the steering angle, for left image, add 0.229 as offset to center, for right image, minus 0.229 as offset to center

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to input a image to network and predict steering angle as specific speed.

My first step was to use a convolution neural network model similar to the NVIDIA's "End to End Learning for Self-Driving Cars" paper, I thought this model might be appropriate because this model could establish relationship between image and streeing angle appropriately.

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. 

#### 2. Final Model Architecture

The final model architecture (model.py lines 16-58) consisted of a convolution neural network with the following layers and layer sizes ...

Here is a visualization of the architecture 
![alt text][image1]

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving and low speed. Here is an example image of center lane driving:

![alt text][image5]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would learn to turn from differnt view point. These images show what a recovery looks like starting from center view :

![alt text][image6]
![alt text][image9]
![alt text][image7]
![alt text][image10]

Then I repeated this process on track 4 times in order to get more data points.

After the collection process, I had 26432 number of data points. I then preprocessed this data online by random rotate and shear. After that i also flipped images and angles thinking that this would make our model more robust. For example, here is an image that has then been flipped:

![alt text][image5]
![alt text][image8]

I also random adjust brightness for image
![alt text][image5]
![alt text][image3]

Crop out the most important part of region
![alt text][image2]

To reduce the compution for this model, resize input image to 64x64
![alt text][image4]

With this size, image from left and right will not show too much differ from center image. 

I finally randomly shuffled the data set and put 25% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 1 as evidenced by train loss 0.012, valid loss 0.0086. I used an adam optimizer so that manually training the learning rate wasn't necessary.

The test result show as video named "track_result.mp4"
