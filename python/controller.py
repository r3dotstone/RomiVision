import numpy as np

r_romi = .07438
r_wheel = .035

class Odometer:
    def __init__(self, encoders, t):
        self.enc_old = encoders

        self.wl = 0
        self.wr = 0

        self.x = 0
        self.y = 0

        self.u = 0
        self.psidot = 0
        self.psi = 0

        self.prev_t = t

    def _updateQdots(self, encoders, dt):
        self.wl = (encoders[0] - self.enc_old[0]) / dt / (120 * 12) * (2 * 3.1415)
        self.wr = (encoders[1] - self.enc_old[1]) / dt / (120 * 12) * (2 * 3.1415)

    def _updateVelocities(self):
        vl = self.wl*r_romi
        vr = self.wr*r_romi
        self.u = (vl + vr) / 2
        self.psidot = (vr - vl) / (2 * r_romi)

    def updateOdometry(self, encoders, t):
        dt = t - self.prev_t
        self._updateQdots(encoders, dt)
        self._updateVelocities()
        self.x = self.x + self.u * np.cos(self.psi) * dt
        self.y  = self.y + self.u * np.sin(self.psi) * dt
        self.psi = self.psi + dt*self.psidot
        self.prev_t = t
        self.enc_old = encoders