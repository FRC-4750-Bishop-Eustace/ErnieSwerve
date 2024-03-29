#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math
import wpilib
import wpimath.kinematics
import wpimath.controller
from phoenix5 import WPI_TalonSRX

# Variables



class ShootModule:
    def __init__(
        self,
    ) -> None:

        # NOTE: need to confirm output from SparkMaxAbsoluteEncoder - may shift to Relative Encoder
        ## No longer required 
        self.shootMotor1ID = WPI_TalonSRX(14)
        self.shootMotor2ID = WPI_TalonSRX(15)
        
        # NOTE: can we use the wpilib.encoder library for these encoders - may need to review

        # NOTE: Need to determine if this is the right distance per pulse value (from user guide it shows 42 counts per revolution)


       

    
    def shootingmotor(self):
        print("motor moving")
        self.shootMotor1ID.set(1.2)
        self.shootMotor2ID.set(1.2) 

    def stopmotor(self):
        print("motor stopped")
        self.shootMotor1ID.set(0)
        self.shootMotor2ID.set(0)
