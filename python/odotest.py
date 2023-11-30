import time as time

from romi_interface.romi import Romi
romi = Romi()

from controller import Odometer
odo = Odometer()

start = time.time()

while (time.time() - start < 3):
    romi.motors(100, 100)
    encoders = romi.read_encoders()
    odo.updateOdometry(encoders[0], encoders[1])
    print(odo.x, ", ", odo.y)
romi.motors(0, 0)