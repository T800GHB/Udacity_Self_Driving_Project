# CarND-PID-Control-Project


#Rubric Points

##Your code should compile
Follow steps:

+ mkdir build && cd build
+ Compile: cmake .. && make
+ Run it: ./pid.

compile passed!

##The PID procedure follows what was taught in the lessons
All the TODO item has completed.

##Describe the effect each of the P, I, D components had in your implementation

PID Parameters

### 1 P Parameter
The P parameter controls the proportional of cross track error which will be corrected by the controller.

Setting this parameter too high caused the vehicle to oscillate between track border with high frequency. I could not find a parameter which made the controller work well, but I chosed initially a value of 0.2, which was acceptable as a starting point.
Using proportional control alone will conduct overshooting and an error between the setpoint and the actual expected state.

### 2 D Parameter
The D component is a best estimate of the future trend of the SetPoint, it could provide the stability for controller, since it anticipates the amount of correction based on difference of the steering angle. 
Setting this parameter too high lead the vehicle to be continiously steering, wheels just like chatter
If this parameter is too low, the the effect of stability will be lost.

### 3 I Parameter
The I component accounts for past cross track error, it will eliminate systematic bias. In our case the vehicle, the problem of systematic bias was not very noticeable. So, this parameter will be set as small value, increasing this parameter adds a lot of instability in the controller, because the integration will be lager over time, big cross track error will not be compensated by other item.

##Describe how the final hyperparameters were chosen
The parameters were chosen by manual tuning. A twiddle is kind of approch, but it will take long time to converge. Bucause our simulation is running in real time, in this case the parameter tuning procedure which cause the vehicle to fall out of the track - no automatic restart of the simulator was possible.
I follow the step [here](https://robotics.stackexchange.com/questions/167/what-are-good-strategies-for-tuning-pid-loops), try and error.

1. Set all gains to zero.
2. Increase the P gain until the response to a disturbance is steady oscillation.
3. Increase the D gain until the the oscillations go away (i.e. it's critically damped).
4. Repeat steps 2 and 3 until increasing the D gain does not stop the oscillations.
5. Set P and D to the last stable values.
6. Increase the I gain until it brings you to the setpoint with the number of oscillations desired (normally zero but a quicker response can be had if you don't mind a couple oscillations of overshoot)


## Simulator
The project aim to control steering angle for vehicle in the Udacity Term 2 Simulator. Download link [here](https://github.com/udacity/self-driving-car-sim/releases/)

This was a simple project for manual tuning. Final parameter set as kp: 0.15, ki: 0.0001, kd: 3
Result like this video show
[Video](./demo_video/show_01.avi)
As those parateter setting, car could drive a lap around the track successfully, but not perfect, there are a lot of swing that does not eliminate. 
An improvement could be to try to find out the parameter of the car by twiddle for the controller. Another improvement might be to control the speed also by using a PID.




