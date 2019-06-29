# Extended Kalman Filter Project Starter Code
Self-Driving Car Engineer Nanodegree Program

[image1]: ./images/fusion.png "detect example1"
[image2]: ./images/lidar.png "detect example2"
[image3]: ./images/radar.png "radar"
In this project, extended kalman filter used to fuse signal from lidar and radar.

How to build project:

1. mkdir build
2. cd build
3. cmake ..
4. make
5. ./ExtendedKF

How to run test:
1. ./ExtendedKF
2. run term2_sim.x86_64 program

term2_sim.x86_64 could be download [here](https://github.com/udacity/self-driving-car-sim/releases/)

**INPUT**: values provided by the simulator to the c++ program

["sensor_measurement"] => the measurement that the simulator observed (either lidar or radar)


**OUTPUT**: values provided by the c++ program to the simulator

["estimate_x"] <= kalman filter estimated position x

["estimate_y"] <= kalman filter estimated position y

["rmse_x"]

["rmse_y"]

["rmse_vx"]

["rmse_vy"]

### Result & analysis
#### Fusion
This is fusion result, EKF could fuse signal from lidar and radar
So, it achive good RMSE
![alt text][image1]

#### Lidar
Only use lidar signal, it perform as normal kalman filter
It has reasonable RMSE, but RMSE is lower to fusion
![alt text][image2]

##### Radar
Only use radar signal, it show us, 
Radar could provide better measurement for speed than lidar(could not measure it directly)
But it position measurement has big variance, so ,it achive lower position RMSE than lidar

![alt text][image3]

---

## Other Important Dependencies

* cmake >= 3.5
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)

## Code Style

Please (do your best to) stick to [Google's C++ style guide](https://google.github.io/styleguide/cppguide.html).

## Generating Additional Data

This is optional!

If you'd like to generate your own radar and lidar data, see the
[utilities repo](https://github.com/udacity/CarND-Mercedes-SF-Utilities) for
Matlab scripts that can generate additional data.

## Hints and Tips!

* You don't have to follow this directory structure, but if you do, your work
  will span all of the .cpp files here. Keep an eye out for TODOs.
* Students have reported rapid expansion of log files when using the term 2 simulator.  This appears to be associated with not being connected to uWebSockets.  If this does occur,  please make sure you are conneted to uWebSockets. The following workaround may also be effective at preventing large log files.

    + create an empty log file
    + remove write permissions so that the simulator can't write to log
 * Please note that the ```Eigen``` library does not initialize ```VectorXd``` or ```MatrixXd``` objects with zeros upon creation.
