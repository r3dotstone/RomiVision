import time as time

from romi_interface.romi import Romi
romi = Romi()

from controller import Odometer
odo = Odometer(romi.read_encoders(), time.time())

start = odo.prev_t
t = start

while (t - start < 3):
    t = time.time()
    romi.motors(255, 255)
    encoders = romi.read_encoders()
    odo.updateOdometry(encoders, t)
    print(t - start, odo.x, odo.y)
romi.motors(0, 0)