# Global Vars

import wpimath.geometry
import math
import robot

# SPEED CONFIG
kMaxSpeed = 2.0  # meters per second
kRMaxSpeed = 10.0
kTMaxSpeed = 2.0
kMaxAngularSpeed = math.pi  # 1/2 rotation per second
frontLeftZero = 0
frontRightZero = 0
backLeftZero = 0
backRightZero = 0
zeroThreshold = wpimath.geometry.Rotation2d(0.3)

# PID and FeedForward
drivePID_P = 0.02
drivePID_I = 0
drivePID_D = 0
turnPID_P = 2 # 0.06
turnPID_I = 0
turnPID_D = 0.000053 #0.000053
driveFF_1 = 1.8
driveFF_2 = 3
turnFF_1 = 0.3 #0.05
turnFF_2 = 1 #0.45 

TurnState = 0

# MODULE/CHASSIS CONFIG
chassisHalfLength = 0.32 # Chassis should be square

frontLeftDriveController = 4
frontLeftTurnController = 3
frontLeftDriveEncoder = 4
frontLeftTurnEncoder = 13

frontRightDriveController = 7
frontRightTurnController = 8
frontRightDriveEncoder = 7
frontRightTurnEncoder = 10

backRightDriveController = 5
backRightTurnController = 6
backRightDriveEncoder = 5
backRightTurnEncoder = 12

backLeftDriveController = 2
backLeftTurnController = 1
backLeftDriveEncoder = 2
backLeftTurnEncoder = 11


# CONTROLLERS/DEADBAND/SLEW
joystickPort1 = 2
joystickPort2 = 0
x_slewrate = 3
y_slewrate = 3
rot_slewrate = 3
squareButton = 1
crossButton = 2
circleButton = 3
x_deadband = 0.1
y_deadband = 0.4
rot_deadband = 0.2

def setTurnState(rot) -> None:
    global TurnState
    if abs(rot) > 0:
        TurnState = 1
    else:
        TurnState = 0
    #print(TurnState)
    #return TurnState
