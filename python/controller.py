

#values for getting joint velocities
oldLeftEncoder = 0#value for old left encoder (for velocity computation)
oldRightEncoder = 0 #old right encoder

#values to hold velocities
omega_left = 0
omega_right = 0

#variables to hold allocentric romi estimates
Xromi = 0
Yromi = 0
#variables to hold egocentric romi estimates
U = 0
psidot = 0
psi = 0

# romi parameters
r_romi = .07438
r_wheel = .035

def updateQdots():
    global oldRightEncoder,oldLeftEncoder,omega_right,omega_left
    omega_right = (romi.encRight-oldRightEncoder)/(timestep/1000.0) / (120 * 12) * (2 * 3.1415)
    omega_left = (romi.encRight - oldLeftEncoder)/(timestep/1000.0) / (120 * 12) * (2 * 3.1415)

def updateVelocities():
    global omega_left,omega_right,r_romi,psidot,U
    vLeft = omega_right*r_romi
    vRight = omega_right*r_romi
    U = (vLeft + vRight) / 2
    psidot = (vRight - vLeft) / (2 * r_romi)

def updateOdometry():
    global Xromi,Yromi,psi,psidot,timestep,U
    #use to get estimates of current romi X, and Y in allocentric frame
    #using odometry:
    Xromi = Xromi + U * np.cos(psi) * timestep/1000.0 #TODO implement this!
    Yromi = Yromi + U * np.sin(psi) * timestep/1000.0 #TODO implement this!
    psi = psi + timestep/1000.0*psidot