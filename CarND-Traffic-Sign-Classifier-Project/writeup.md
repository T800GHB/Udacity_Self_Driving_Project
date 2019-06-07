# **Traffic Sign Recognition** 

## Writeup

---

**Build a Traffic Sign Recognition Project**

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Data augmentation
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/raw_distribution.png "raw_distribution"
[image2]: ./examples/basic_image_show.png "basic_image_show"
[image3]: ./examples/gray_scale.png "gray_scale"
[image4]: ./examples/shift.png "shift"
[image5]: ./examples/scaling.png "scaling"
[image6]: ./examples/affine_transform.png "affine_transform"
[image7]: ./examples/brightness.png "brightness"
[image8]: ./examples/after_data_aug.png "after_data_aug"
[image9]: ./examples/compare.png "compare"
[image10]: ./test_web_images/0.jpeg "0"
[image11]: ./test_web_images/1.jpeg "1"
[image12]: ./test_web_images/2.jpeg "2"
[image13]: ./test_web_images/3.jpeg "3"
[image14]: ./test_web_images/4.jpeg "4"
[image15]: ./test_web_images/5.jpeg "5"


## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/481/view) individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how I addressed each one. 

You're reading it! and here is a link to my [project code](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/Traffic_Sign_Classifier.ipynb)

### Data Set Summary & Exploration

#### 1. Basic summary of the data set. In the code, the analysis should be done using python, numpy and/or pandas methods rather than hardcoding results manually.

I used the numpy library to calculate summary statistics of the traffic
signs data set:

* The size of training set is 34799
* The size of the validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is 32x32x3
* The number of unique classes/labels in the data set is 43

#### 2. Include an exploratory visualization of the dataset.

Here is an exploratory visualization of the data set. It is a bar chart showing how the data distribute

![alt text][image1]

I also plot one image for every class as increasing order

![alt text][image2]

### Design and Test a Model Architecture

#### 1. Describe how you preprocessed the image data. What techniques were chosen and why did you choose these techniques? Consider including images showing the output of each preprocessing technique. Pre-processing refers to techniques such as converting to grayscale, normalization, etc. (OPTIONAL: As described in the "Stand Out Suggestions" part of the rubric, if you generated additional data for training, describe why you decided to generate additional data, how you generated the data, and provide example images of the additional data. Then describe the characteristics of the augmented training set like number of images in the set, number of images for each class, etc.)

1. I decided to convert the images to grayscale because the main content of traffic sign is graphical pattern, not color.  I just get mean of 3 channel to calculate gray scale image.

Here is an example of a traffic sign image before and after grayscaling.

![alt text][image3]

2.  I augement train data set.
   I decided to generate additional data because i found, in the stage of data dataset exploratory, data distribution is so unbalance for each class. the minimum quantity for one class is 210.
   I want to generate some new data for those class of sample, at least 800 ones.

    To add more data to the the data set, I used the 4 following techniques to produce new data
    * Random shift position, implement by method random_translate()
    I consider that traffic sign will not always keep center position in the image, so i random choose offset then transform it, just like this:
    ![alt text][image4]
    * Random scaling, implement by method random_scaling()
    Traffic sign will occupy differne ratio in the image, this method will bring more diversity on observation distance, just like this:
    ![alt text][image5]
    * Random affine transform, implement by method random_warp()
    By this method ,we could get image that observe from different visual angle, just like this:
    ![alt text][image6]
    * Random brightness change, implement by method random_brightness()
    We may face bright or dark light condition, use this method to simulate it, just like this:
    ![alt text][image7]

    I use those method to extend train data set, keep samples minimum number is 800. After data augmention, data distribution like this:
    ![alt text][image8]

    Here is an example of an original image and an augmented image:

    ![alt text][image9]

    The difference between the original data set and the augmented data set is the new data contain useless part, like black edge.

3. I normalized the image data because this could lead network converge to better solution faster. 


#### 2. Final model architecture
My final model consisted of the following layers:

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input         		| 32x32x1 RGB image   							| 
| Convolution 5x5x6   	| 1x1 stride, valid padding, outputs 28x28x6 	|
| RELU					|												|
| Max pooling	      	| 2x2 stride,  outputs 14x14x16 				|
| Convolution 5x5x16    | 1x1 stride, valid padding, outputs 10x10x16   |
| RELU                  |                                               |
| Max pooling           | 2x2 stride,  outputs 5x5x16                   |
| Convolution 3x3x100   | 1x1 stride, valid padding, outputs 3x3x100    |
| RELU                  |                                               |
| Convolution 3x3x200   | 1x1 stride, valid padding, outputs 1x1x200    |
| RELU                  |                                               |
| Flatten               | Flatten layer from second, third, forth convolution output|
| Concat                | Concat all output from flatten layer          |
| Dropout               |                                               |
| Fully connected		| input: 1500, output n_class=43                |
| Softmax				| final classify								|
 
This network refer to DenseNet.

#### 3. How I trained model.

To train the model, hyperparameter setting like this
- Cross entropy as loss function
- Use adam as optimizer
- Set batch size as 128
- Set train epoch 10
- Set learning rate 0.001, after 5 epoch decrease to 0.0001

#### 4. Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

My final model results were:
* training set accuracy of 0.997
* validation set accuracy of 0.959
* test set accuracy of 0.937

I calculate accuracy by the method evaluate(X_data, y_data), this method will load data and label, then compare label to the ground truth. I use correct prediction divided by total number of input data to get accuracy.

If an iterative approach was chosen:
* What was the first architecture that was tried and why was it chosen?
  I first to extend lenet as network named FullConvLeNet().
  I just want to use global pooling instead of full connect layer as final output.
* What were some problems with the initial architecture?
  This network is big and achive lower accuracy on validation data set.
* How was the architecture adjusted and why was it adjusted? 
  I think the first try of network is too easy to overfitting, so prune some redundent parameter and combine feature from different layer, just like DenseNet pattern.
* Which parameters were tuned? How were they adjusted and why?
  In the training step, if i use a same learning rate in whole procedure, network will converge to a solution fast, but it will not optimize to a better after that.
  So, i decrese learning rate 10 times after 5 epoch, network could continue to find better solution.
* What are some of the important design choices and why were they chosen? For example, why might a convolution layer work well with this problem? How might a dropout layer help with creating a successful model?
  Dropout layer could prevent network overfit too much. 
  For this task, i don't need a too big network, it will bring me another problem, underfit.

If a well known architecture was chosen:
* What architecture was chosen?
  I refer to DenseNet.
* Why did you believe it would be relevant to the traffic sign application?
  I think feature from different layer need to fusion, it will be more expressive
* How does the final model's accuracy on the training, validation and test set provide evidence that the model is working well?
  Validation set accuracy is highest that network could hit. Training set achive almost 100% accuracy, test set preform reasonable accuracy.
 

### Test a Model on New Images

#### 1. Choose six German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

Here are six German traffic signs that I found on the web:

![alt text][image10] ![alt text][image11] ![alt text][image12] 
![alt text][image13] ![alt text][image14] ![alt text][image15] 

The first image might be difficult to classify because pattern are similar

#### 2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).

Here are the results of the prediction:

| Image			        |     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| Speed limit (30km/h)  | Speed limit (30km/h)  						| 
| Speed limit (20km/h)  | Speed limit (20km/h)      					|
| Turn left ahead		| Turn left ahead								|
| Stop          		| Stop      					 				|
| Right-of-way at the next intersection		| Beware of ice/snow  		|
| Road work             | Road work                                     |


The model was able to correctly guess 5 of the 6 traffic signs, which gives an accuracy of 83.3%. 
The test image found on the web has different background compare to the test set image. So, I think network learn feature by backgound. As another view to analysis result, incorrect prediction is small black pattern in the traffic sign, with low resolution of image, label 11 are so similar to label 30, so network get difficult to work well with low resolution image.  

#### 3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

The code for making predictions on my final model is located in the next to last cell of the Ipython notebook.

For the first image, the model is absolutly sure that this is a Speed limit (30km/h) sign (probability of 0.99), and the image contain a speed limit sign. The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 0.9999968        		| Speed limit (30km/h)		    				| 
| 2.3805962e-06   		| Speed limit (20km/h)							|
| 8.554746e-07			| Speed limit (50km/h)  						|
| 1.4211358e-11	 		| Roundabout mandatory			 				|
| 3.5257425e-14		    | Speed limit (80km/h) 							|



For the second image, prediction is correct, but output is little low

The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 0.81902033       		| Speed limit (20km/h)		    				| 
| 0.10536235   		| General caution							|
| 0.05064181			| Speed limit (30km/h)  						|
| 0.024797065	 		| Children crossing			 				|
| 7.334092e-05	    | Roundabout mandatory 							|


For the third image, traffic sign is correct with very high score

The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 0.99994147       		| Turn left ahead		    				| 
| 5.8422258e-05   		| Ahead only							|
| 6.467423e-08			| Go straight or right  						|
| 6.647964e-11	 		| Speed limit (20km/h)			 				|
| 3.8573266e-11	    | Beware of ice/snow 							|

For the fourth image traffic sign is correct with very high score

The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 0.9998827        		| Stop		    				| 
| 7.1666465e-05   		| General caution							|
| 4.5630073e-05			| Go straight or right  						|
| 1.0013309e-08	 		| Ahead only			 				|
| 7.458596e-09		    | Children crossing 							|

For the fifth image, this is incorrect prediction, and top 2 is correct prediction, but with very low score, this may caused by test image is so different from training set. 

The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 0.9641316        		| Beware of ice/snow		    				| 
| 0.035765406   		| Right-of-way at the next intersection			|
| 0.000102933365			| Double curve  						|
| 6.4807686e-08	 		| Slippery road			 				|
| 9.706613e-09	    | Road narrows on the right 				|

For the sixth image with very high score

The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 0.999204        		| Road work		    				| 
| 0.00030789358   		| Beware of ice/snow							|
| 0.00019235561			| Roundabout mandatory  						|
| 0.00012727917 		| Priority road			 				|
| 9.176908e-05		    | Bumpy road							|

