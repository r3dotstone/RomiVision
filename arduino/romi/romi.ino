#include <PololuRPiSlave.h>
#include <Romi32U4.h>

struct Data
{
  int16_t leftMotor, rightMotor;
  int16_t leftEncoder, rightEncoder;
};

PololuRPiSlave<struct Data,20> slave;
Romi32U4Motors motors;
Romi32U4Encoders encoders;

void setup() {
  slave.init(20);
}

void loop() {
  slave.updateBuffer();
  
  motors.setSpeeds(slave.buffer.leftMotor, slave.buffer.rightMotor);

  slave.buffer.leftEncoder = encoders.getCountsLeft();
  slave.buffer.rightEncoder = encoders.getCountsRight();

  slave.finalizeWrites();
}
