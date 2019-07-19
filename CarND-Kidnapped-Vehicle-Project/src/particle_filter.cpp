/**
 * particle_filter.cpp
 *
 * Created on: Dec 12, 2016
 * Author: Tiffany Huang
 */

#include "particle_filter.h"

#include <math.h>
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <random>
#include <string>
#include <vector>

#include "helper_functions.h"

using std::string;
using std::vector;

void ParticleFilter::init(double x, double y, double theta, double std[]) {
  /**
   * Set the number of particles. Initialize all particles to 
   *   first position (based on estimates of x, y, theta and their uncertainties
   *   from GPS) and all weights to 1. 
   *  Add random Gaussian noise to each particle.
   * NOTE: Consult particle_filter.h for more information about this method 
   *   (and others in this file).
   */
  num_particles = 101;  // Set the number of particles
  double init_weight = 1.0 / static_cast<double>(num_particles);
  std::normal_distribution<double> x_init(x, std[0]);
  std::normal_distribution<double> y_init(y, std[1]);
  std::normal_distribution<double> theta_init(theta, std[2]);

  particles.resize(num_particles);

  for(auto& p : particles) {
    p.x = x_init(gen);
    p.y = y_init(gen);
    p.theta = theta_init(gen);
    p.weight = init_weight;
  }

  is_initialized = true;

}

void ParticleFilter::prediction(double delta_t, double std_pos[], 
                                double velocity, double yaw_rate) {
  /**
   * Add measurements to each particle and add random Gaussian noise.
   * NOTE: When adding noise you may find std::normal_distribution 
   *   and std::default_random_engine useful.
   *  http://en.cppreference.com/w/cpp/numeric/random/normal_distribution
   *  http://www.cplusplus.com/reference/random/default_random_engine/
   */
  const double eps = 0.0000001;
  std::normal_distribution<double> x_noise(0.0, std_pos[0]);
  std::normal_distribution<double> y_noise(0.0, std_pos[1]);
  std::normal_distribution<double> theta_noise(0.0, std_pos[2]);

  for(auto& p : particles) {
    if (fabs(yaw_rate) < eps) {
      p.x += velocity * delta_t * cos(p.theta);
      p.y += velocity * delta_t * sin(p.theta);
    } else {
      p.x += (velocity / yaw_rate) * (sin(p.theta + yaw_rate * delta_t) - sin(p.theta));
      p.y += (velocity / yaw_rate) * (cos(p.theta) - cos(p.theta + yaw_rate * delta_t));
      p.theta += yaw_rate * delta_t;
    }

    p.x += x_noise(gen);
    p.y += y_noise(gen);
    p.theta += theta_noise(gen);
  }
}

void ParticleFilter::dataAssociation(vector<LandmarkObs> predicted, 
                                     vector<LandmarkObs>& observations) {
  /**
   * Find the predicted measurement that is closest to each 
   *   observed measurement and assign the observed measurement to this 
   *   particular landmark.
   * NOTE: this method will NOT be called by the grading code. But you will 
   *   probably find it useful to implement this method and use it as a helper 
   *   during the updateWeights phase.
   */

  // Find min distance landmark pair between prediction and observation, assign id to observation
  for (auto& obs : observations) {
    double min_dist = std::numeric_limits<double>::max();
    int32_t min_idx = std::numeric_limits<int32_t>::min();
    int32_t num_prediction = static_cast<int32_t >(predicted.size());
    for (int32_t i = 0; i < num_prediction; ++i) {
      double dis = dist(obs.x, obs.y, predicted[i].x, predicted[i].y);

      if (dis < min_dist) {
        min_dist = dis;
        min_idx = i;
      }
    }
    obs.id = min_idx;
  }


}

static double inline MultiGaussian(double x, double ux, double y, double uy, double sx, double sy) {
  double factor = 1 / (2 * M_PI * sx * sy);
  double power = - ((x - ux) * (x - ux) / (2 * sx * sx) + (y - uy) * (y - uy) / (2 * sy * sy));
  return factor * exp(power);
}

void ParticleFilter::updateWeights(double sensor_range, double std_landmark[], 
                                   const vector<LandmarkObs> &observations, 
                                   const Map &map_landmarks) {
  /**
   * Update the weights of each particle using a mult-variate Gaussian 
   *   distribution. You can read more about this distribution here: 
   *   https://en.wikipedia.org/wiki/Multivariate_normal_distribution
   * NOTE: The observations are given in the VEHICLE'S coordinate system. 
   *   Your particles are located according to the MAP'S coordinate system. 
   *   You will need to transform between the two systems. Keep in mind that
   *   this transformation requires both rotation AND translation (but no scaling).
   *   The following is a good resource for the theory:
   *   https://www.willamette.edu/~gorr/classes/GeneralGraphics/Transforms/transforms2d.htm
   *   and the following is a good resource for the actual equation to implement
   *   (look at equation 3.33) http://planning.cs.uiuc.edu/node99.html
   */

  for (auto& p : particles) {
    vector<LandmarkObs> candidate_landmarks;
    // Collect landmark for current particle within observation range
    for (const auto& lm : map_landmarks.landmark_list) {
      if (fabs(p.x - lm.x_f) < sensor_range and fabs(p.y - lm.y_f)) {
        candidate_landmarks.emplace_back(lm.id_i, lm.x_f, lm.y_f);
      }
    }
    // Convert all observation landmark to map frame
    std::vector<LandmarkObs> sense_markers;
    for (const auto& obs : observations) {
      LandmarkObs transformed_observation_marker;
      transformed_observation_marker.x = p.x + obs.x * cos(p.theta) - obs.y * sin(p.theta);
      transformed_observation_marker.y = p.y + obs.x * sin(p.theta) + obs.y * cos(p.theta);
      transformed_observation_marker.id = 0; // Used to record associate with candidate_landmarks
      sense_markers.emplace_back(transformed_observation_marker);
    }

    // Id of sense marker is index of matched item in candidate_landmarks
    dataAssociation(candidate_landmarks, sense_markers);

    // Calculate product of gaussian model
    p.weight = 1.0;

    for (const auto& sense_mark : sense_markers) {
      LandmarkObs& ref_mark = candidate_landmarks[sense_mark.id];
      double prob = MultiGaussian(sense_mark.x, ref_mark.x, sense_mark.y, ref_mark.y, std_landmark[0], std_landmark[1]);
      p.weight *= prob;
    }
  }

}

void ParticleFilter::resample() {
  /**
   * Resample particles with replacement with probability proportional 
   *   to their weight. 
   * NOTE: You may find std::discrete_distribution helpful here.
   *   http://en.cppreference.com/w/cpp/numeric/random/discrete_distribution
   */
  // Collect all weights, easy to use it
  weights.clear();
  for (const auto& p : particles) {
    weights.emplace_back(p.weight);
  }

  // generate random starting index for resampling wheel
  std::uniform_int_distribution<int32_t > uniintdist(0, num_particles-1);
  int32_t index = uniintdist(gen);

  double max_weight = *max_element(weights.cbegin(), weights.cend());

  std::uniform_real_distribution<double> weight_random(0.0, max_weight);

  double beta = 0.0;

  vector<Particle> resample_particles;
  // Resample specific quantity of particles
  for (int32_t i = 0; i < num_particles; ++i) {
    beta += weight_random(gen) * 2.0;
    while (beta > weights[index]) {
      beta -= weights[index];
      index = (index + 1) % num_particles;
    }

    resample_particles.emplace_back(particles[index]);
  }

  particles = std::move(resample_particles);
}

void ParticleFilter::SetAssociations(Particle& particle, 
                                     const vector<int>& associations, 
                                     const vector<double>& sense_x, 
                                     const vector<double>& sense_y) {
  // particle: the particle to which assign each listed association, 
  //   and association's (x,y) world coordinates mapping
  // associations: The landmark id that goes along with each listed association
  // sense_x: the associations x mapping already converted to world coordinates
  // sense_y: the associations y mapping already converted to world coordinates
  particle.associations= associations;
  particle.sense_x = sense_x;
  particle.sense_y = sense_y;
}

string ParticleFilter::getAssociations(Particle best) {
  vector<int> v = best.associations;
  std::stringstream ss;
  copy(v.begin(), v.end(), std::ostream_iterator<int>(ss, " "));
  string s = ss.str();
  s = s.substr(0, s.length()-1);  // get rid of the trailing space
  return s;
}

string ParticleFilter::getSenseCoord(Particle best, string coord) {
  vector<double> v;

  if (coord == "X") {
    v = best.sense_x;
  } else {
    v = best.sense_y;
  }

  std::stringstream ss;
  copy(v.begin(), v.end(), std::ostream_iterator<float>(ss, " "));
  string s = ss.str();
  s = s.substr(0, s.length()-1);  // get rid of the trailing space
  return s;
}
