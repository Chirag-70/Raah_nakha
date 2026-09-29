import numpy as np
import pandas as pd


def generate_sample_route(
    duration_s=60,
    sample_hz=10
):

    """
    Generates a deterministic 1-minute IMU demo.

    Route concept:

        300 m straight
               |
               |
               +-------- 300 m

    Approx:
        0-30 sec  : 300 m straight
        30-31 sec : right turn
        31-60 sec : 300 m straight

    Vehicle speed:
        10 m/s = 36 km/h
    """

    n = int(
        duration_s * sample_hz
    )

    time = (
        np.arange(n)
        / sample_hz
    )


    # -----------------------------------------------------
    # Vehicle speed
    # -----------------------------------------------------

    speed = np.full(
        n,
        10.0
    )


    # -----------------------------------------------------
    # Heading
    # -----------------------------------------------------

    heading = np.zeros(n)

    turn_start = 30.0
    turn_end = 31.0


    turn_mask = (
        (time >= turn_start)
        &
        (time < turn_end)
    )


    heading[turn_mask] = np.linspace(
        0,
        np.pi / 2,
        turn_mask.sum(),
        endpoint=False
    )


    heading[
        time >= turn_end
    ] = np.pi / 2


    # -----------------------------------------------------
    # Yaw rate
    # -----------------------------------------------------

    yaw_rate = np.gradient(
        heading,
        1.0 / sample_hz
    )


    # -----------------------------------------------------
    # Forward acceleration
    # -----------------------------------------------------

    forward_acceleration = np.gradient(
        speed,
        1.0 / sample_hz
    )


    # -----------------------------------------------------
    # Small deterministic noise
    # -----------------------------------------------------

    rng = np.random.default_rng(168)


    noise_acc_x = rng.normal(
        0,
        0.03,
        n
    )

    noise_acc_y = rng.normal(
        0,
        0.03,
        n
    )

    noise_acc_z = rng.normal(
        0,
        0.04,
        n
    )


    noise_gyro = rng.normal(
        0,
        0.003,
        n
    )


    # -----------------------------------------------------
    # Synthetic accelerometer
    # -----------------------------------------------------

    accel_x = (
        forward_acceleration
        +
        noise_acc_x
    )

    accel_y = noise_acc_y

    accel_z = (
        9.81
        +
        noise_acc_z
    )


    # -----------------------------------------------------
    # Synthetic gyroscope
    # -----------------------------------------------------

    gyro_x = rng.normal(
        0,
        0.002,
        n
    )

    gyro_y = rng.normal(
        0,
        0.002,
        n
    )

    gyro_z = (
        yaw_rate
        +
        noise_gyro
    )


    return pd.DataFrame({

        "timestamp_ns":
            (
                time * 1e9
            ).astype(np.int64),

        "accel_x":
            accel_x,

        "accel_y":
            accel_y,

        "accel_z":
            accel_z,

        "gyro_x":
            gyro_x,

        "gyro_y":
            gyro_y,

        "gyro_z":
            gyro_z
    })