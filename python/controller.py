import time as time
import numpy as np

r_romi = .07438
r_wheel = .035

class Odometer:
    def __init__(self):
        self.enc_l_old = 0
        self.enc_r_old = 0

        self.wl = 0
        self.wr = 0

        self.x = 0
        self.y = 0

        self.u = 0
        self.psidot = 0
        self.psi = 0

        self.prev_t = 0

    def _updateQdots(self, enc_r, enc_l, dt):
        self.wr = (enc_r - self.enc_r_old)/ dt / (120 * 12) * (2 * 3.1415)
        self.wl = (enc_l - self.enc_r_old)/ dt / (120 * 12) * (2 * 3.1415)

    def _updateVelocities(self):
        vl = self.wr*r_romi
        vr = self.wl*r_romi
        U = (vl + vr) / 2
        psidot = (vr - vl) / (2 * r_romi)

    def updateOdometry(self, enc_r, enc_l):
        t = time.process_time()
        dt = t - self.prev_t
        self._updateQdots(enc_r, enc_l, dt)
        self._updateVelocities()
        self.x = self.x + self.u * np.cos(self.psi) * dt
        self.y  = self.y + self.u * np.sin(self.psi) * dt
        self.psi = self.psi + dt*self.psidot
        self.prev_t = t