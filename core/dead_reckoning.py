import numpy as np
import pandas as pd

from .butterworth import butterworth_filter
from .eskf import ESKF
from .iekf import IEKF
from .fusion import fuse_tracks


def run_dead_reckoning(df):

    df = df.copy()

    df = df.reset_index(drop=True)

    timestamps = (
        df["timestamp_ns"]
        .to_numpy(dtype=np.int64)
    )

    time_s = (
        timestamps - timestamps[0]
    ) / 1e9

    # -----------------------------------------------------
    # Estimate sampling rate
    # -----------------------------------------------------

    if len(time_s) > 2:

        median_dt = np.median(
            np.diff(time_s)
        )

        if median_dt > 0:

            sample_hz = np.clip(
                1.0 / median_dt,
                1.0,
                100.0
            )

        else:

            sample_hz = 10.0

    else:

        sample_hz = 10.0


    # -----------------------------------------------------
    # Extract IMU
    # -----------------------------------------------------

    acceleration = df[
        [
            "accel_x",
            "accel_y",
            "accel_z"
        ]
    ].to_numpy(float)

    gyro = df[
        [
            "gyro_x",
            "gyro_y",
            "gyro_z"
        ]
    ].to_numpy(float)


    # -----------------------------------------------------
    # Butterworth
    # -----------------------------------------------------

    acceleration_filtered = butterworth_filter(
        acceleration,
        sample_hz=sample_hz
    )

    gyro_filtered = butterworth_filter(
        gyro,
        sample_hz=sample_hz
    )


    # -----------------------------------------------------
    # Filters
    # -----------------------------------------------------

    dt = 1.0 / sample_hz

    eskf = ESKF(dt)
    iekf = IEKF(dt)


    rows = []


    # -----------------------------------------------------
    # Propagation
    # -----------------------------------------------------

    for i in range(len(df)):

        acc_xy = acceleration_filtered[i, :2]

        gyro_z = gyro_filtered[i, 2]


        eskf_state = eskf.update(
            acc_xy,
            gyro_z
        )

        iekf_state = iekf.update(
            acc_xy,
            gyro_z
        )


        # -------------------------------------------------
        # Fusion
        # -------------------------------------------------

        fused = fuse_tracks(
            eskf_state,
            iekf_state
        )


        position = fused["position"]

        velocity = fused["velocity"]

        yaw = fused["yaw"]


        rows.append({

            "time_s": time_s[i],

            "x_m": position[0],

            "y_m": position[1],

            "heading_deg": (
                np.degrees(yaw) % 360
            ),

            "velocity_x_mps": velocity[0],

            "velocity_y_mps": velocity[1],

            "velocity_mps": np.linalg.norm(
                velocity
            ),

            "eskf_x_m":
                eskf_state["position"][0],

            "eskf_y_m":
                eskf_state["position"][1],

            "iekf_x_m":
                iekf_state["position"][0],

            "iekf_y_m":
                iekf_state["position"][1],
        })


    trajectory = pd.DataFrame(rows)


    # -----------------------------------------------------
    # Path length
    # -----------------------------------------------------

    dx = np.diff(
        trajectory["x_m"],
        prepend=trajectory["x_m"].iloc[0]
    )

    dy = np.diff(
        trajectory["y_m"],
        prepend=trajectory["y_m"].iloc[0]
    )

    path_length = np.sum(
        np.sqrt(dx**2 + dy**2)
    )


    return {

        "trajectory": trajectory,

        "duration_s": float(
            time_s[-1]
        ),

        "path_length_m": float(
            path_length
        ),

        # Demo map center
        # Replace with selected real map origin later.
        "map_center": (
            21.1458,
            79.0882
        )
    }