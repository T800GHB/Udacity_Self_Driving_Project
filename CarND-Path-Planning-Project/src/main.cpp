#include <uWS/uWS.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include "Eigen-3.3/Eigen/Core"
#include "Eigen-3.3/Eigen/QR"
#include "helpers.h"
#include "json.hpp"
#include "spline.h"
#include "path_planning.h"

// for convenience
using nlohmann::json;
using std::string;
using std::vector;

int main() {
  uWS::Hub h;

  // Load up map values for waypoint's x,y,s and d normalized normal vectors
  vector<double> map_waypoints_x;
  vector<double> map_waypoints_y;
  vector<double> map_waypoints_s;
  vector<double> map_waypoints_dx;
  vector<double> map_waypoints_dy;

  // Waypoint map to read from
  string map_file_ = "../data/highway_map.csv";
  // The max s value before wrapping around the track back to 0
  double max_s = 6945.554;

  std::ifstream in_map_(map_file_.c_str(), std::ifstream::in);

  string line;
  while (getline(in_map_, line)) {
    std::istringstream iss(line);
    double x;
    double y;
    float s;
    float d_x;
    float d_y;
    iss >> x;
    iss >> y;
    iss >> s;
    iss >> d_x;
    iss >> d_y;
    map_waypoints_x.emplace_back(x);
    map_waypoints_y.emplace_back(y);
    map_waypoints_s.emplace_back(s);
    map_waypoints_dx.emplace_back(d_x);
    map_waypoints_dy.emplace_back(d_y);
  }
    // Default ego lane and start velocity
    int32_t ego_lane = kDefaultEgoLane;

    double ego_velocity = 0.0;

  h.onMessage([&ego_lane, &ego_velocity, &map_waypoints_x,&map_waypoints_y,&map_waypoints_s,
               &map_waypoints_dx,&map_waypoints_dy]
              (uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length,
               uWS::OpCode opCode) {
    // "42" at the start of the message means there's a websocket message event.
    // The 4 signifies a websocket message
    // The 2 signifies a websocket event
    if (length && length > 2 && data[0] == '4' && data[1] == '2') {

      auto s = hasData(data);

      if (s != "") {
        auto j = json::parse(s);
        
        string event = j[0].get<string>();
        
        if (event == "telemetry") {
          // j[1] is the data JSON object
          
          // Main car's localization Data
          double car_x = j[1]["x"];
          double car_y = j[1]["y"];
          double car_s = j[1]["s"];
          double car_d = j[1]["d"];
          double car_yaw = j[1]["yaw"];
          double car_speed = j[1]["speed"];

          // Previous path data given to the Planner
          auto previous_path_x = j[1]["previous_path_x"];
          auto previous_path_y = j[1]["previous_path_y"];
          // Previous path's end s and d values 
          double end_path_s = j[1]["end_path_s"];
          double end_path_d = j[1]["end_path_d"];

          // Sensor Fusion Data, a list of all other cars on the same side 
          //   of the road.
          auto sensor_fusion = j[1]["sensor_fusion"];

          json msgJson;

          vector<double> next_x_vals;
          vector<double> next_y_vals;

          /**
           * Define a path made up of (x,y) points that the car will visit
           *   sequentially every .02 seconds
           */
            int32_t previous_size = previous_path_x.size();

            // Start from latest position
            if (previous_size > 0) {
                car_s = end_path_s;
            }

            // Find environment car around ego
            TargetCar targets;
            for (const auto& sd : sensor_fusion) {
                double target_car_x = sd[1];
                double target_car_y = sd[2];
                double target_car_xv = sd[3];
                double target_car_yv = sd[4];
                double target_car_s = sd[5];
                double target_car_d = sd[6];

                double x_increase = target_car_xv * kExecuteTime * previous_size;
                double y_increase = target_car_yv * kExecuteTime * previous_size;
                double future_x = target_car_x + x_increase;
                double future_y = target_car_y + y_increase;
                double angle = atan2(y_increase, x_increase);
                vector<double> target_frenet = getFrenet(future_x, future_y, angle, map_waypoints_x, map_waypoints_y);
                double future_target_car_s = target_frenet[0];
                double future_target_car_d = target_frenet[1];
                int32_t target_car_lane = LocateLane(future_target_car_d);
                if (target_car_lane < 0) {
                    continue;
                }
                LocateTargetCarLaneWithSafeDis(target_car_s, car_s, ego_lane, target_car_lane, &targets);
            }

            // Perform behavior
            double speed_adjust = 0.0;
            Behavior(targets, ego_velocity, ego_lane, speed_adjust);
            
            vector<double> ptsx;
            vector<double> ptsy;

            double ref_x = car_x;
            double ref_y = car_y;
            double ref_yaw = deg2rad(car_yaw);
            // Get a previous point by current direction
            if (previous_size <= 1) {

                double prev_car_x = car_x - cos(car_yaw);
                double prev_car_y = car_y - sin(car_yaw);

                ptsx.emplace_back(prev_car_x);
                ptsx.emplace_back(car_x);

                ptsy.emplace_back(prev_car_y);
                ptsy.emplace_back(car_y);
            } else {
                ref_x = previous_path_x.back();
                ref_y = previous_path_y.back();

                double ref_x_prev = previous_path_x[previous_size - 2];
                double ref_y_prev = previous_path_y[previous_size - 2];
                ref_yaw = atan2(ref_y-ref_y_prev, ref_x-ref_x_prev);

                ptsx.emplace_back(ref_x_prev);
                ptsx.emplace_back(ref_x);

                ptsy.emplace_back(ref_y_prev);
                ptsy.emplace_back(ref_y);
            }

            // Define far location to fit spline
            vector<double> next_wp0 = getXY(car_s + kDisSegment, kLaneCenter + kLaneWidth * ego_lane, map_waypoints_s, map_waypoints_x, map_waypoints_y);
            vector<double> next_wp1 = getXY(car_s + 2 * kDisSegment, kLaneCenter + kLaneWidth * ego_lane, map_waypoints_s, map_waypoints_x, map_waypoints_y);
            vector<double> next_wp2 = getXY(car_s + 3 * kDisSegment, kLaneCenter + kLaneWidth * ego_lane, map_waypoints_s, map_waypoints_x, map_waypoints_y);

            ptsx.emplace_back(next_wp0[0]);
            ptsx.emplace_back(next_wp1[0]);
            ptsx.emplace_back(next_wp2[0]);

            ptsy.emplace_back(next_wp0[1]);
            ptsy.emplace_back(next_wp1[1]);
            ptsy.emplace_back(next_wp2[1]);

            // Convert to ego car coordinate frame, so the spline begin from 0 degree and 0 offset, easy to do calculation
            for (int32_t i = 0; i < ptsx.size(); ++i) {
                double shift_x = ptsx[i] - ref_x;
                double shift_y = ptsy[i] - ref_y;
                Rotate(shift_x, shift_y, -ref_yaw, &(ptsx[i]), &(ptsy[i]));
            }

            // Create the spline.
            tk::spline s;
            s.set_points(ptsx, ptsy);

            // Inherit path points from previous path for continuity.
            for ( int i = 0; i < previous_size; i++ ) {
                next_x_vals.emplace_back(previous_path_x[i]);
                next_y_vals.emplace_back(previous_path_y[i]);
            }

            // Calculate distance y position on ahead.
            double target_x = kDisSegment;
            double target_y = s(target_x);
            double target_dist = sqrt(target_x*target_x + target_y*target_y);

            double x_add_on = 0;

            const int32_t num_generate = kNumPoints - previous_size - 1;
            for (int32_t i = 0; i < num_generate; ++i) {
                ego_velocity += speed_adjust;
                if (ego_velocity > kMaxSpeed) {
                    ego_velocity = kMaxSpeed;
                } else if (ego_velocity < kMaxAcc) {
                    ego_velocity = kMaxAcc;
                }
                double N = target_dist/(kExecuteTime * ego_velocity / kMilePerHoursFactor);
                double x_point = x_add_on + target_x/N;
                double y_point = s(x_point);

                x_add_on = x_point;

                double x_ref = x_point;
                double y_ref = y_point;
                Rotate(x_ref, y_ref, ref_yaw, &x_point, &y_point);

                x_point += ref_x;
                y_point += ref_y;

                next_x_vals.emplace_back(x_point);
                next_y_vals.emplace_back(y_point);
            }

          msgJson["next_x"] = next_x_vals;
          msgJson["next_y"] = next_y_vals;

          auto msg = "42[\"control\","+ msgJson.dump()+"]";

          ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
        }  // end "telemetry" if
      } else {
        // Manual driving
        std::string msg = "42[\"manual\",{}]";
        ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
      }
    }  // end websocket if
  }); // end h.onMessage

  h.onConnection([&h](uWS::WebSocket<uWS::SERVER> ws, uWS::HttpRequest req) {
    std::cout << "Connected!!!" << std::endl;
  });

  h.onDisconnection([&h](uWS::WebSocket<uWS::SERVER> ws, int code,
                         char *message, size_t length) {
    ws.close();
    std::cout << "Disconnected" << std::endl;
  });

  int port = 4567;
  if (h.listen(port)) {
    std::cout << "Listening to port " << port << std::endl;
  } else {
    std::cerr << "Failed to listen to port" << std::endl;
    return -1;
  }
  
  h.run();
}
