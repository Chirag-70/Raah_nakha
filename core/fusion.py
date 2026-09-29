import numpy as np


def fuse_tracks(
    eskf_state,
    iekf_state
):

    """
    Prototype consistency/fusion layer.

    Current implementation uses the mean of the
    ESKF and IEKF state estimates.
    """

    position = (
        eskf_state["position"]
        +
        iekf_state["position"]
    ) / 2.0

    velocity = (
        eskf_state["velocity"]
        +
        iekf_state["velocity"]
    ) / 2.0

    # Circular mean for yaw
    sin_sum = (
        np.sin(eskf_state["yaw"])
        +
        np.sin(iekf_state["yaw"])
    )

    cos_sum = (
        np.cos(eskf_state["yaw"])
        +
        np.cos(iekf_state["yaw"])
    )

    yaw = np.arctan2(
        sin_sum,
        cos_sum
    )

    return {
        "position": position,
        "velocity": velocity,
        "yaw": yaw
    }