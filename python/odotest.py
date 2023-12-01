import time as time

from romi_interface.romi import Romi
romi = Romi()

from controller import Odometer
odo = Odometer(romi.read_encoders())

start = time.time()

while (time.time() - start < 3):
    romi.motors(255, 230)
    encoders = romi.read_encoders()
    odo.updateOdometry(encoders[0], encoders[1])
    print(time.time() - start, odo.x, odo.y)
romi.motors(0, 0)