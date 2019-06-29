#include "FusionEKF.h"
#include <iostream>
#include "Eigen/Dense"
#include "tools.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::cout;
using std::endl;
using std::vector;

/**
 * Constructor.
 */
FusionEKF::FusionEKF() {
  is_initialized_ = false;

  previous_timestamp_ = 0;

  // initializing matrices
  ekf_.R_laser_ = MatrixXd(2, 2);
  ekf_.R_radar_ = MatrixXd(3, 3);
    //measurement covariance matrix - laser
  ekf_.R_laser_ << 0.0225, 0,
              0, 0.0225;

  //measurement covariance matrix - radar
  ekf_.R_radar_ << 0.09, 0, 0,
              0, 0.0009, 0,
              0, 0, 0.09;

  /**
   * TODO: Finish initializing the FusionEKF.
   * TODO: Set the process and measurement noises
   */
    ekf_.x_ = VectorXd(4);

    // state covariance matrix P
    ekf_.P_ = MatrixXd(4, 4);
    ekf_.P_ << 1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 100, 0,
            0, 0, 0, 100;

    // the initial transition matrix F_
    ekf_.F_ = MatrixXd(4, 4);
    ekf_.F_ << 1, 0, 1, 0,
            0, 1, 0, 1,
            0, 0, 1, 0,
            0, 0, 0, 1;

    // laser measurement matrix
    ekf_.H_laser_ = MatrixXd(2, 4);
    ekf_.H_laser_ << 1, 0, 0, 0,
                    0, 1, 0, 0;

    ekf_.Hj_ = MatrixXd(3,4);

    // set the acceleration noise components
    ekf_.noise_ax_ = 9;
    ekf_.noise_ay_ = 9;
}

/**
 * Destructor.
 */
FusionEKF::~FusionEKF() {}

void FusionEKF::ProcessMeasurement(const MeasurementPackage &measurement_pack) {
  /**
   * Initialization
   */
  if (!is_initialized_) {
    /**
     * TODO: Initialize the state ekf_.x_ with the first measurement.
     * TODO: Create the covariance matrix.
     * You'll need to convert radar from polar to cartesian coordinates.
     */

    // first measurement
    cout << "EKF: " << endl;
    ekf_.x_ = VectorXd(4);
    ekf_.x_ << 1, 1, 1, 1;

    if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR) {
      // TODO: Convert radar from polar to cartesian coordinates 
      //         and initialize state.
        double rho = measurement_pack.raw_measurements_[0];
        double phi = measurement_pack.raw_measurements_[1];
        double rhodot = measurement_pack.raw_measurements_[2];
      ekf_.x_ << rho * cos(phi),
                 rho * sin(phi),
                 rhodot * cos(phi),
                 rhodot * sin(phi);

    }
    else if (measurement_pack.sensor_type_ == MeasurementPackage::LASER) {
      // TODO: Initialize state.
        // set the state with the initial location and zero velocity
        ekf_.x_ << measurement_pack.raw_measurements_[0],
                measurement_pack.raw_measurements_[1],
                0,
                0;
    }

    previous_timestamp_ = measurement_pack.timestamp_;
    // done initializing, no need to predict or update
    is_initialized_ = true;
    return;
  }

  /**
   * Prediction
   */

  /**
   * TODO: Update the state transition matrix F according to the new elapsed time.
   * Time is measured in seconds.
   * TODO: Update the process noise covariance matrix.
   * Use noise_ax = 9 and noise_ay = 9 for your Q matrix.
   */
    // compute the time elapsed between the current and previous measurements
    // dt - expressed in seconds
    double dt = (measurement_pack.timestamp_ - previous_timestamp_) / 1000000.0;
    previous_timestamp_ = measurement_pack.timestamp_;

    ekf_.ResetF(dt);
    ekf_.ResetQ(dt);

    ekf_.Predict();

    /**
    * Update
    */

    /**
    * TODO:
    * - Use the sensor type to perform the update step.
    * - Update the state and covariance matrices.
    */

    if (measurement_pack.sensor_type_ == MeasurementPackage::LASER) {
    // TODO: Laser updates
//      ekf_.Update(measurement_pack.raw_measurements_);

    } else {
    // TODO: Radar updates
      ekf_.Hj_ = tools.CalculateJacobian(ekf_.x_);
      ekf_.UpdateEKF(measurement_pack.raw_measurements_);

    }

    // print the output
    cout << "x_ = " << ekf_.x_ << endl;
    cout << "P_ = " << ekf_.P_ << endl;
}
