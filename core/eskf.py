import numpy as np


class ESKF:

    """
    Lightweight 2D prototype of an
    error-state inertial propagation track.

    State used for this prototype:

        position = [x, y]
        velocity = [vx, vy]
        yaw

    This is intentionally simplified for
    visualization and architecture demonstration.
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

        # Yaw propagation
        self.yaw += gyro_z * dt

        cos_yaw = np.cos(self.yaw)
        sin_yaw = np.sin(self.yaw)

        rotation = np.array([
            [cos_yaw, -sin_yaw],
            [sin_yaw,  cos_yaw]
        ])

        # Body → local/world frame
        acceleration_world = (
            rotation @ acceleration_body
        )

        # Velocity propagation
        self.velocity += (
            acceleration_world * dt
        )

        # Position propagation
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