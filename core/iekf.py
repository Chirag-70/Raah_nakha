import numpy as np


class IEKF:

    """
    Lightweight invariant-style prototype track.

    The production PS168 architecture can later replace
    this implementation with a complete Lie-group IEKF.

    For the Streamlit prototype we maintain a separate
    inertial propagation track so that IEKF and ESKF
    outputs can be compared and fused.
    """

    def __init__(self, dt):

        self.dt = float(dt)

        self.position = np.zeros(2)
        self.velocity = np.zeros(2)

        self.yaw = 0.0


    def update(
        self,
        acceleration_body,
        gyro_z
    ):

        dt = self.dt

        self.yaw += gyro_z * dt

        c = np.cos(self.yaw)
        s = np.sin(self.yaw)

        rotation = np.array([
            [c, -s],
            [s,  c]
        ])

        acceleration_world = (
            rotation @ acceleration_body
        )

        self.velocity += (
            acceleration_world * dt
        )

        self.position += (
            self.velocity * dt
            +
            0.5 * acceleration_world * dt * dt
        )

        return {
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "yaw": self.yaw
        }