#include "kalman_filter.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;

#include <iostream>

/* 
 * Please note that the Eigen library does not initialize 
 *   VectorXd or MatrixXd objects with zeros upon creation.
 */

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

//void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
//                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
//  x_ = x_in;
//  P_ = P_in;
//  F_ = F_in;
//  H_ = H_in;
//  R_ = R_in;
//  Q_ = Q_in;
//}

void KalmanFilter::Predict() {
  /**
   * predict the state
   */
    x_ = F_ * x_;
    MatrixXd Ft = F_.transpose();
    P_ = F_ * P_ * Ft + Q_;
}

void KalmanFilter::Update(const VectorXd &z) {
  /**
   * update the state by using Kalman Filter equations
   */
    VectorXd z_pred = H_laser_ * x_;
    VectorXd y = z - z_pred;
    MatrixXd Ht = H_laser_.transpose();
    MatrixXd S = H_laser_ * P_ * Ht + R_laser_;
    MatrixXd Si = S.inverse();
    MatrixXd PHt = P_ * Ht;
    MatrixXd K = PHt * Si;

    //new estimate
    x_ = x_ + (K * y);
    long x_size = x_.size();
    MatrixXd I = MatrixXd::Identity(x_size, x_size);
    P_ = (I - K * H_laser_) * P_;
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  /**
   * update the state by using Extended Kalman Filter equations
   */
    double rho = sqrt(x_(0) * x_(0) + x_(1) * x_(1));
    double phi = atan2(x_(1), x_(0));
    double rhodot = 0;
    if (fabs(rho) > 0.001) {
        rhodot = (x_(0) * x_(2) + x_(1) * x_(3)) / rho;
    }

    // To deal with angle express at border
    double half_pi = M_PI / 2;
    if (phi < 0. and z(1) > 0. and fabs(phi) > half_pi and fabs(z(1)) > half_pi) {
        phi += 2 * M_PI;
    }

    if (phi > 0. and z(1) < 0. and fabs(phi) > half_pi and fabs(z(1)) > half_pi) {
        phi -= 2 * M_PI;
    }


    VectorXd z_pred = VectorXd(3);
    z_pred << rho, phi, rhodot;
    VectorXd y = z - z_pred;
    MatrixXd Ht = Hj_.transpose();
    MatrixXd S = Hj_ * P_ * Ht + R_radar_;
    MatrixXd Si = S.inverse();
    MatrixXd PHt = P_ * Ht;
    MatrixXd K = PHt * Si;

    //new estimate
    x_ = x_ + (K * y);
    long x_size = x_.size();
    MatrixXd I = MatrixXd::Identity(x_size, x_size);
    P_ = (I - K * Hj_) * P_;
}

void KalmanFilter::ResetF(double dt) {
    F_ << 1, 0, dt, 0,
            0, 1, 0, dt,
            0, 0, 1, 0,
            0, 0, 0, 1;

}

void KalmanFilter::ResetQ(double dt) {
    double power3dt = dt * dt * dt / 2;
    double power4dt = dt * dt * dt * dt / 4;
    double power2dt = dt * dt;
    Q_ = MatrixXd(4, 4);
    Q_ << power4dt * noise_ax_, 0, power3dt * noise_ax_, 0,
            0, power4dt * noise_ay_, 0, power3dt * noise_ay_,
            power3dt * noise_ax_, 0, power2dt * noise_ax_, 0,
            0, power3dt * noise_ay_, 0, power2dt* noise_ay_;
}
