import numpy as np

from scipy.signal import butter, filtfilt


def butterworth_filter(
    data,
    sample_hz=10.0,
    cutoff_hz=2.0,
    order=3
):
    """
    Low-pass Butterworth filter.

    Used here as a prototype noise-reduction stage
    before inertial state propagation.
    """

    data = np.asarray(data, dtype=float)

    if len(data) < 15:
        return data.copy()

    nyquist = sample_hz / 2.0

    cutoff = min(
        cutoff_hz,
        nyquist * 0.8
    )

    normal_cutoff = cutoff / nyquist

    b, a = butter(
        order,
        normal_cutoff,
        btype="low"
    )

    filtered = filtfilt(
        b,
        a,
        data,
        axis=0
    )

    return filtered