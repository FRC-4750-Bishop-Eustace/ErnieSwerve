#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math
import wpilib
import wpimath
import wpilib.drive
import wpimath.filter
import wpimath.controller
import drivetrain
import variables
import shooter
import navxGyro
#import camera
#import auto
from cscore import CameraServer


class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        """Robot initialization function"""
        self.controller = wpilib.Joystick(variables.joystickPort1)
        self.controller2 = wpilib.Joystick(variables.joystickPort2)
        self.swerve = drivetrain.Drivetrain()
        self.shooter = shooter.ShootModule()
        #self.swerveAuto = auto.SwerveSubsystem()
        #self.camera = camera.Camera()
        # navxGyro is a file to test the navx Gyro. This can be ignored/commented out.
        self.navxGyro = navxGyro.Gyro()

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        # Speed limiters

        self.xspeedLimiter = wpimath.filter.SlewRateLimiter(variables.x_slewrate)
        self.yspeedLimiter = wpimath.filter.SlewRateLimiter(variables.y_slewrate)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(variables.rot_slewrate)

        self.fieldDrive = 1
        self.shooter_toggle = 0

        #CameraServer.startAutomaticCapture()
        

    #FUTURE
    def autonomousPeriodic(self) -> None:
        #self.driveWithJoystick(False)
        self.swerve.updateOdometry()


    def teleopPeriodic(self) -> None:
        if self.controller.getRawButton(variables.crossButton) == 1:
            self.fieldDrive = 2
        if self.controller.getRawButton(variables.circleButton) == 1:
            self.fieldDrive = 1

        if self.fieldDrive == 2:
            self.driveWithJoystick(True)
        else:
            self.driveWithJoystick(False)
    
        self.navxGyro.getGyro()
        #self.shootWithJoystick(False)
        #self.shooter.stopSensor()
        if self.controller.getRawButton(variables.squareButton) == 1:
            self.swerve.alignment()
        #print(self.fieldDrive)

        if self.controller.getRawButton(variables.triangleButton) == 1 and self.shooter_toggle == 0:
            self.shooter.speakershootmotor()
            self.shooter_toggle = 1
        else:
            self.shooter.stopmotor()
            self.shooter_toggle = 0
         
    
        # if self.controller.getRawButton(4) == 1:
        # self.swerve.drive(0,0,0,0,self.getPeriod())
        # self.swerve.alignment()

    def driveWithJoystick(self, fieldRelative: bool) -> None:
        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        # NOTE: Check if we need inversion here
        if fieldRelative:
            self.swerve.updateOdometry()

        xSpeed = (
            self.xspeedLimiter.calculate(
                wpimath.applyDeadband(self.controller.getRawAxis(1), variables.x_deadband)
            )
            * variables.kMaxSpeed
        )

        # Get the y speed or sideways/strafe speed. We are inverting this because
        # we want a positive value when we pull to the left. Xbox controllers
        # return positive values when you pull to the right by default.
        # NOTE: Check if we need inversion here
        ySpeed = (
            -self.yspeedLimiter.calculate(
                wpimath.applyDeadband(self.controller.getRawAxis(2), variables.y_deadband)
            )
            * variables.kTMaxSpeed
        )

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            (-self.rotLimiter.calculate(
                wpimath.applyDeadband(self.controller.getRawAxis(3), variables.rot_deadband)
            )
            * variables.kRMaxSpeed) +
            (self.rotLimiter.calculate(
                wpimath.applyDeadband(self.controller.getRawAxis(4), variables.rot_deadband)
            )
            * variables.kRMaxSpeed)
        )

        variables.setTurnState(rot)

        #self.swerve.drive(xSpeed, ySpeed, rot, fieldRelative, self.getPeriod())
        self.swerve.drive(xSpeed, ySpeed, rot, fieldRelative, self.getPeriod())

        
