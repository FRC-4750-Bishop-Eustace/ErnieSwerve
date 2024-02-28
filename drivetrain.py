#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math
import navx
import wpilib
import wpimath.geometry
import wpimath.kinematics
import swervemodule
import variables

'''
kMaxSpeed = 1.5  # meters per second
kRMaxSpeed = 0.1
kTMaxSpeed = 1.0
kMaxAngularSpeed = math.pi  # 1/2 rotation per second
frontLeftZero = 0
frontRightZero = 0
backLeftZero = 0
backRightZero = 0
zeroThreshold = wpimath.geometry.Rotation2d(0.3)
'''

class Drivetrain:
    """
    Represents a swerve drive style drivetrain.
    """

    def __init__(self) -> None:
        # NOTE: May need to tweak the center measurements 44.5mm rough measurement
        # NOTE: EVERYTHING IS MEASURE IN METERS! 
        # NOTE: Update center measure distance from each module
        # Wheel to Wheel = 63.4 cm
        # Chassis = 76cm
        '''
        self.frontLeftLocation = wpimath.geometry.Translation2d(0.32, 0.32)
        self.frontRightLocation = wpimath.geometry.Translation2d(0.32, -0.32)
        self.backRightLocation = wpimath.geometry.Translation2d(-0.32, -0.32)
        self.backLeftLocation = wpimath.geometry.Translation2d(-0.32, 0.32)
        '''
        self.frontLeftLocation = wpimath.geometry.Translation2d(-variables.chassisHalfLength, variables.chassisHalfLength)
        self.frontRightLocation = wpimath.geometry.Translation2d(-variables.chassisHalfLength, -variables.chassisHalfLength)
        self.backRightLocation = wpimath.geometry.Translation2d(variables.chassisHalfLength, -variables.chassisHalfLength)
        self.backLeftLocation = wpimath.geometry.Translation2d(variables.chassisHalfLength, variables.chassisHalfLength)

        self.frontLeft = swervemodule.SwerveModule(variables.frontLeftDriveController, variables.frontLeftTurnController, variables.frontLeftDriveEncoder, variables.frontLeftTurnEncoder)
        self.frontRight = swervemodule.SwerveModule(variables.frontRightDriveController, variables.frontRightTurnController, variables.frontRightDriveEncoder, variables.frontRightTurnEncoder)
        self.backRight = swervemodule.SwerveModule(variables.backRightDriveController, variables.backRightTurnController, variables.backRightDriveEncoder, variables.backRightTurnEncoder)
        self.backLeft = swervemodule.SwerveModule(variables.backLeftDriveController, variables.backLeftTurnController, variables.backLeftDriveEncoder, variables.backLeftTurnEncoder)


        '''
        BERT NOTES:
        
        driveMotorID: int,
        turningMotorID: int,
        driveEncoderID: int,
        turningEncoderID: int,

        Front Left (+,+) 
            - Drive Motor: 4
            - Rotation Motor: 3
            - Drive Encoder: 4
            - Rotation Encoder: 13 
        
        Front Right (+,-) 
            - Drive Motor: 7
            - Rotation Motor: 8
            - Drive Encoder: 7
            - Rotation Encoder: 10

        Rear Left (-,+) 
            - Drive Motor: 2
            - Rotation Motor: 1
            - Drive Encoder: 2
            - Rotation Encoder: 11

        Rear Right (-,-) 
            - Drive Motor: 5
            - Rotation Motor: 6
            - Drive Encoder: 5
            - Rotation Encoder: 12

        '''

        #self.gyro = wpilib.AnalogGyro(0)
        self.angler = navx.AHRS.create_spi()
        #print("gyroscope = ", self.angler)
        self.gyroinit = self.angler.getAngle()
        self.gyroradiansinit = wpimath.units.degreesToRadians(self.gyroinit)
        # print("gyro", self.gyro)

        #NOTE: Just defining the fixed kinematics of the bot
        self.kinematics = wpimath.kinematics.SwerveDrive4Kinematics(
            self.frontLeftLocation,
            self.frontRightLocation,
            self.backRightLocation,
            self.backLeftLocation,
        )

        #NOTE: getPosition - need to determine position value - velocity and angle -
        #NOTE: Need to understand expected units/values returned - is it meters & radians?
        self.odometry = wpimath.kinematics.SwerveDrive4Odometry(
            self.kinematics,
            wpimath.geometry.Rotation2d(self.gyroradiansinit),
            #self.angler.getAngle(),
            #self.angler.getRotation2d(),
            #self.gyro.Translation2d(),
            #self.gyro.getRotation2d(),
            (
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.backRight.getPosition(),
                self.backLeft.getPosition(),
            ),
        )

        #print(self.frontLeft.getPosition(), self.frontRight.getPosition(), self.backLeft.getPosition(), self.backRight.getPosition())

        self.angler.reset()

    def drive(
        self,
        xSpeed: float,
        ySpeed: float,
        rot: float,
        fieldRelative: bool,
        periodSeconds: float,
    ) -> None:
        """
        Method to drive the robot using joystick info.
        :param xSpeed: Speed of the robot in the x direction (forward).
        :param ySpeed: Speed of the robot in the y direction (sideways).
        :param rot: Angular rate of the robot.
        :param fieldRelative: Whether the provided x and y speeds are relative to the field.
        :param periodSeconds: Time
        """

        #if fieldRelative:
        #    self.updateOdometry()

        self.gyro = self.angler.getAngle()
        self.gyroradians = wpimath.units.degreesToRadians(self.gyro)

        #print("gyro", self.gyroradians)

        swerveModuleStates = self.kinematics.toSwerveModuleStates(
            wpimath.kinematics.ChassisSpeeds.discretize(
                wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(
                    xSpeed, ySpeed, rot, wpimath.geometry.Rotation2d(self.gyroradians)
                )
                if fieldRelative
                else wpimath.kinematics.ChassisSpeeds(xSpeed, ySpeed, rot),
                periodSeconds,
            )
        )
        wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerveModuleStates, variables.kMaxSpeed
        )
        
        #NOTE: Should we desaturate for Turning speed motors? 
        
        self.frontLeft.setDesiredState(swerveModuleStates[0])
        self.frontRight.setDesiredState(swerveModuleStates[1])
        self.backRight.setDesiredState(swerveModuleStates[2])
        self.backLeft.setDesiredState(swerveModuleStates[3])

        

        #print(wpimath.kinematics.ChassisSpeeds(0, 0, rot))
        #print(wpimath.kinematics.ChassisSpeeds(xSpeed, ySpeed, rot))
        #print(swerveModuleStates[0], swerveModuleStates[1], swerveModuleStates[2], swerveModuleStates[3])

    # CURRENLY NOT BEING USED
    def updateOdometry(self) -> None:
        """Updates the field relative position of the robot."""
        self.odometry.update(
            wpimath.geometry.Rotation2d(self.gyroradiansinit),
            (
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.backRight.getPosition(),
                self.backLeft.getPosition(),
            ),
        )
        # print(wpimath.geometry.Rotation2d(self.gyroradians))
        
    '''
    def alignment(self) -> None:
        #Updates the wheel alignment for robot to zer0
        #Leverage Network Tables to report out each wheel position
        if self.frontLeft.getPosition().angle > variables.zeroThreshold:
            self.frontLeft.turningMotor.setVoltage(0.1)
            print("Front Left Position = ", self.frontLeft.getPosition())
        if self.backRight.getPosition().angle > variables.zeroThreshold:
            self.frontRight.turningMotor.setVoltage(0.1)
            print("Front Right Position = ", self.frontRight.getPosition())
        if self.backLeft.getPosition().angle > variables.zeroThreshold:
            self.backLeft.turningMotor.setVoltage(0.1)
            print("Back Left Position = ", self.backLeft.getPosition())
        if self.backRight.getPosition().angle > variables.zeroThreshold:
            self.backRight.turningMotor.setVoltage(0.1)
            print("Back Right Position = ", self.backRight.getPosition())
    '''
    def alignment(self) -> None:
        self.frontLeft.setDesiredState(wpimath.kinematics.SwerveModuleState(0, wpimath.geometry.Rotation2d(0)))
        self.frontRight.setDesiredState(wpimath.kinematics.SwerveModuleState(0, wpimath.geometry.Rotation2d(0)))
        self.backRight.setDesiredState(wpimath.kinematics.SwerveModuleState(0, wpimath.geometry.Rotation2d(0)))
        self.backLeft.setDesiredState(wpimath.kinematics.SwerveModuleState(0, wpimath.geometry.Rotation2d(0)))
        # print("aligning")


