//
// Created by hbguo on 19-8-2.
//

#ifndef PATH_PLANNING_PATH_PLANNING_H
#define PATH_PLANNING_PATH_PLANNING_H

#include <cstdint>

const double kLaneWidth = 4.0;
const double kLaneCenter = 2.0;
const double kMaxSpeed = 49.5;
const double kMaxAcc = 0.224;
const double kSafeDis = 30.0;
const double kExecuteTime = 0.02;
const double kMilePerHoursFactor = 2.24;
const double kDisSegment = 30.0;
const int32_t kSeneorDataDim = 7;
const int32_t kNumPoints = 50;
const int32_t kDefaultEgoLane = 1;

struct TargetCar {
    int32_t ahead_count;
    int32_t left_count;
    int32_t right_count;
    TargetCar(int32_t a, int32_t l, int32_t r):ahead_count(a), left_count(l), right_count(r){}
    TargetCar():TargetCar(0,0,0){}
    TargetCar&operator=(const TargetCar&) = default;
};

int32_t LocateLane(double d);

void LocateTargetCarLaneWithSafeDis(double target_car_s, double ego_s, int32_t ego_lane, int32_t target_car_lane, TargetCar* output);

void Behavior(const TargetCar &targets, const double &ego_velocity, int32_t &ego_lane, double &speed_adjust);



#endif //PATH_PLANNING_PATH_PLANNING_H
