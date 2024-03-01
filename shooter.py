#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math
import wpilib
import wpimath.kinematics
import wpimath.controller
import variables
from phoenix5 import WPI_TalonSRX

# Variables



class ShootModule:
    def __init__(
        self,
    ) -> None:
    def __init__(
   
        # NOTE: need to confirm output from SparkMaxAbsoluteEncoder - may shift to Relative Encoder
        ## No longer required 
        self.shootMotor1ID = WPI_TalonSRX(14)
        self.shootMotor2ID = WPI_TalonSRX(15)
            self.stopSensor = wpilib.AnalogInput(0)
)
        # NOTE: can we use the wpilib.encoder library for these encoders - may need to review

        # NOTE: Need to determine if this is the right distance per pulse value (from user guide it shows 42 counts per revolution)


    def vacummotor(self):
        self.shootMotor1ID(variables.intakeSpeedMotor1)
        self.shootMotor2ID(variables.intakeSpeedMotor2)

    def ampshootmotor(self):
        self.shootMotor1ID(variables.ampSpeedMotor1)
        self.shootMotor2ID(variables.ampSpeedMotor2)

    def speakershootmotor(self):
        self.shootMotor1ID.set(variables.Motor1Speed)
        self.shootMotor2ID.set(variables.Motor2Speed) 

    def stopmotor(self):
        self.shootMotor1ID.set(0)
        self.shootMotor2ID.set(0)



    def stopSensor(self):
        if self.stopSensor.getValue() < 1000:
            self.shootMotor1ID.set(0)
            self.shootMotor2ID.set(0)
            
