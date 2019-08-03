//
// Created by hbguo on 19-8-2.
//
#include <cmath>
#include "path_planning.h"

int32_t LocateLane(double d) {
    int32_t ret = -1;
    double lane_idx = d / kLaneWidth;
    ret = static_cast<int32_t>(lane_idx);
    return ret;
}

void LocateTargetCarLaneWithSafeDis(double target_car_s, double ego_s, int32_t ego_lane, int32_t target_car_lane,
                                    TargetCar *output) {
    int32_t lane_diff = target_car_lane - ego_lane;
    if (lane_diff == 0) {
        if (target_car_s > ego_s and target_car_s - ego_s < kSafeDis) {
            output->ahead_count++;
        }
    } else if (lane_diff < 0) {
        if (fabs(target_car_s - ego_s) < kSafeDis) {
            output->left_count++;
        }
    } else if (lane_diff > 0) {
        if (fabs(target_car_s - ego_s) < kSafeDis) {
            output->right_count++;
        }
    }
}

void Behavior(const TargetCar &targets, const double &ego_velocity, int32_t &ego_lane, double &speed_adjust) {
    if (targets.ahead_count) {
        if ((not targets.left_count) and ego_lane > 0) {
            ego_lane -= 1;
        } else if ((not targets.right_count) and ego_lane < 2) {
            ego_lane += 1;
        } else {
            // Slow down keep safe distance
            speed_adjust -= kMaxAcc;
        }
    } else {
        if (ego_lane != kDefaultEgoLane) {
            if (ego_lane < kDefaultEgoLane and (not targets.right_count)){
                ego_lane += 1;
            } else if (ego_lane > kDefaultEgoLane and (not targets.left_count)) {
                ego_lane -= 1;
            }
        }
        if (ego_velocity < kMaxSpeed) {
            speed_adjust += kMaxAcc;
        }
    }
}

