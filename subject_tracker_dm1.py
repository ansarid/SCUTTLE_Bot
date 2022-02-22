#  Copyright (C) 2022 Texas Instruments Incorporated - http://www.ti.com/
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#    Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#
#    Neither the name of Texas Instruments Incorporated nor the names of
#    its contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# The logic below imitates the logic in the L2 track_target / L3 follow combination, mostly.
# I tried to retain intentions of this code such as inputing minimum and target radii, rather than
# target radius & tolerance, to compute the pixel size of a target that results in approach/reverse.
# DM 2022.02.21

import numpy as np   # import for math functions

def clamp(val, minVal, maxVal):
    return max(min(val, maxVal), minVal)

class SubjectTracker:
    cruiseRate = 0.8            # fraction of max speed that the robot uses for chasing
    turnRate = 0.9              # fraction of max turning speed that robot uses for seeking
    minLinVel = -0.4            # linear velocity (m/s)
    maxLinVel = 0.4             # linear velocity (m/s)
    minAngVel = -2              # angular velocity (rad/s)
    maxAngVel = 2               # angular velocity (rad/s)
    tol_band  = 0.20            # fraction of field of view yielding no turning

    def __init__(self, input_width, input_height, min_radius, target_radius):
        self.target_radius = target_radius         # radius desired (pixels)
        self.min_radius    = min_radius            # the no-move radius = any radius between target and min
        self.input_width   = input_width
        self.input_height  = input_height
        self.tol           = tol_band * input_width  #tolerance of pixels for non-rotation
 
    def _turnAndGo(self, x, y, radius):
        
        if x is None or y is None or radius is None:
            return chassisTargets                                   # just recycle the previous values

        x_pos = self.input_width/2 - x                              # returns a pixel location [leftmost 120 to rightmost -120]
        x_offset = x_pos / self.input_width                         # returns the offset percent among Field of View [-1.0, 1.0]

        if abs(x_pos) > self.tol:                                   # x-location of target is outside the centerband
            angVel = self.maxAngVel * turnRate * np.sign(pos)       # left-hand target yields left-hand turn (positive)
            chassisTargets[0] = 0                                   # make x_dot zero
            chassisTargets[1] = self.maxAngVel * x_offset * x_offset * np.sign(x_offset) # max turn speed * ratio of offset
            return chassisTargets
        if radius < self.min_radius:                                # if the ball is too far
            linVel = self.maxLinVel * cruiseRate                    # back up at the cruise speed
            chassisTargets[0] = linVel                              # store the x_dot value
            chassisTargets[1] = 0                                   # theta_dot is zero
        if radius > self.target_radius:                             # if the ball is too near
            linVel = self.minLinVel * cruiseRate                    # use the reverse cruise speed
            chassisTargets[0] = linVel                              # store the x_dot value
            chassisTargets[1] = 0                                   # theta_dot is zero
        return chassisTargets                                       # return the x_dot targets

    @classmethod
    def _slope_intercept(self, x1, y1, x2, y2):
        a = (y2 - y1) / (x2 - x1)
        b = y1 - (a * x1)
        return a,b

    def getChassisTargets(self, x, y, radius):
        chassisTargets = self._turnAndGo(x, y, radius)
        return chassisTargets

# class SubjectTracker
