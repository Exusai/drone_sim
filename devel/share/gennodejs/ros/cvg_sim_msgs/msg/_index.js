
"use strict";

let MotorCommand = require('./MotorCommand.js');
let MotorPWM = require('./MotorPWM.js');
let Compass = require('./Compass.js');
let MotorStatus = require('./MotorStatus.js');
let RawRC = require('./RawRC.js');
let VelocityZCommand = require('./VelocityZCommand.js');
let HeadingCommand = require('./HeadingCommand.js');
let PositionXYCommand = require('./PositionXYCommand.js');
let Supply = require('./Supply.js');
let YawrateCommand = require('./YawrateCommand.js');
let RC = require('./RC.js');
let ServoCommand = require('./ServoCommand.js');
let Altitude = require('./Altitude.js');
let RawImu = require('./RawImu.js');
let VelocityXYCommand = require('./VelocityXYCommand.js');
let Altimeter = require('./Altimeter.js');
let AttitudeCommand = require('./AttitudeCommand.js');
let ControllerState = require('./ControllerState.js');
let HeightCommand = require('./HeightCommand.js');
let ThrustCommand = require('./ThrustCommand.js');
let RawMagnetic = require('./RawMagnetic.js');
let RuddersCommand = require('./RuddersCommand.js');

module.exports = {
  MotorCommand: MotorCommand,
  MotorPWM: MotorPWM,
  Compass: Compass,
  MotorStatus: MotorStatus,
  RawRC: RawRC,
  VelocityZCommand: VelocityZCommand,
  HeadingCommand: HeadingCommand,
  PositionXYCommand: PositionXYCommand,
  Supply: Supply,
  YawrateCommand: YawrateCommand,
  RC: RC,
  ServoCommand: ServoCommand,
  Altitude: Altitude,
  RawImu: RawImu,
  VelocityXYCommand: VelocityXYCommand,
  Altimeter: Altimeter,
  AttitudeCommand: AttitudeCommand,
  ControllerState: ControllerState,
  HeightCommand: HeightCommand,
  ThrustCommand: ThrustCommand,
  RawMagnetic: RawMagnetic,
  RuddersCommand: RuddersCommand,
};
