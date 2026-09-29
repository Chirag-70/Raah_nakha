import pandas as pd


REQUIRED_COLUMNS = [
    "timestamp_ns",
    "accel_x",
    "accel_y",
    "accel_z",
    "gyro_x",
    "gyro_y",
    "gyro_z"
]


COLUMN_ALIASES = {

    "timestamp":
        "timestamp_ns",

    "timestamp_ns":
        "timestamp_ns",

    "acc_x":
        "accel_x",

    "accel_x":
        "accel_x",

    "acc_y":
        "accel_y",

    "accel_y":
        "accel_y",

    "acc_z":
        "accel_z",

    "accel_z":
        "accel_z",

    "gyro_x":
        "gyro_x",

    "gyro_y":
        "gyro_y",

    "gyro_z":
        "gyro_z"
}


def validate_imu_csv(
    dataframe
):

    df = dataframe.copy()


    # Normalize column names

    rename_map = {}

    for column in df.columns:

        normalized = (
            column
            .strip()
            .lower()
            .replace(" ", "_")
        )

        if normalized in COLUMN_ALIASES:

            rename_map[column] = (
                COLUMN_ALIASES[
                    normalized
                ]
            )


    df = df.rename(
        columns=rename_map
    )


    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]


    if missing:

        raise ValueError(
            "Missing required IMU columns: "
            +
            ", ".join(missing)
        )


    df = df[
        REQUIRED_COLUMNS
    ]


    # Numeric conversion

    for column in REQUIRED_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    df = df.dropna()


    if len(df) < 20:

        raise ValueError(
            "At least 20 valid IMU samples are required."
        )


    df = df.sort_values(
        "timestamp_ns"
    )


    df = df.drop_duplicates(
        "timestamp_ns"
    )


    df = df.reset_index(
        drop=True
    )


    return df