#!/usr/bin/env python3
"""
gps_manage.py

Script to control donkey car with GPS navigation. Waypoints are set with GPS coordinates in degrees.

Call: gps_manage.py -drive
"""

# import GPS Planner and other DK parts
import donkeycar as dk
from donkeycar.parts.gps import GPS
from donkeycar.parts.planner import Planner
from donkeycar.vehicle import Vehicle
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle

# other important modules
import serial
import pynmea2
import time
import threading


def drive(cfg, goalLocation):
    """
    drive(cfg, goalLocation)

    Add GPS, Planner, and actuator parts and call DK Vehicle.py to run car.
    @param: cfg - configuration file from dk calibration
            goalLocation - list of GPS coordinates in degrees
    @return: None
    """
    # initialize vehicle
    V = Vehicle()

    # GPS is a DK part that will poll GPS data from serial port
    # and output current location in radians.
    gps = GPS()

    # Planner is a DK part that calculates control signals to actuators based on current location
    # from GPS
    planner = Planner(goalLocation=goalLocation, steer_gain=0.5, throttle_gain=1)

    # Actuators: steering and throttle 
    steering_controller = PCA9685(cfg.STEERING_CHANNEL)
    steering = PWMSteering(controller=steering_controller,
                                    left_pulse=cfg.STEERING_LEFT_PWM,
                                    right_pulse=cfg.STEERING_RIGHT_PWM)

    throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL)
    throttle = PWMThrottle(controller=throttle_controller,
                                    max_pulse=cfg.THROTTLE_FORWARD_PWM,
                                    zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                                    min_pulse=cfg.THROTTLE_REVERSE_PWM)

    # add threaded part for gps controller
    V.add(gps, outputs=["currLocation", "prevLocation"], threaded=True)

    # add planner, actuator parts
    V.add(planner, inputs=["currLocation", "prevLocation"], outputs=["steer_cmd", "throttle_cmd"])
    V.add(steering, inputs=['steer_cmd'])
    V.add(throttle, inputs=['throttle_cmd'])

    V.start()

if __name__ == '__main__':
    # goalLocation = [0.5738778838, -2.0461111027] # bioengineering building
    goalLocation = [0.5738857378, -2.0461065736] # bioengineering building

    cfg = dk.load_config()
    drive(cfg, goalLocation)
