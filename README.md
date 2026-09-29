# SIH 2026 PS168 — Streamlit Dead Reckoning Prototype

## Prototype

This project demonstrates a simplified PS168 dead-reckoning pipeline:

IMU
↓
Butterworth Filter
↓
ESKF + IEKF
↓
Consistency Fusion
↓
Dead Reckoning Trajectory
↓
OpenStreetMap Overlay

The AI/ML/TFLite speed model is intentionally disabled.

---

## Demo Route

The built-in demo runs for approximately 60 seconds:

0–30 seconds:
300 m straight

30–31 seconds:
approximately 90° right turn

31–60 seconds:
300 m straight

The demo uses synthetic IMU-like data so that it can run without a phone.

---

## Real IMU Input

The current prototype accepts a CSV with:

timestamp_ns
accel_x
accel_y
accel_z
gyro_x
gyro_y
gyro_z

Example:

timestamp_ns,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z

---

## Installation

Create environment:

python -m venv .venv

Windows:

.venv\Scripts\activate

Install:

pip install -r requirements.txt

Run:

streamlit run app.py

---



## ESKF / IEKF Scope

The included ESKF and IEKF are lightweight prototype propagation tracks.

They are intended to demonstrate:

- parallel state propagation
- trajectory generation
- ESKF/IEKF comparison
- fusion
- map visualization

They are not yet a production-grade 3D inertial navigation implementation.

---

## Map

The prototype converts local XY displacement into latitude/longitude around a
demo map center and displays the trajectory on OpenStreetMap tiles.

The next implementation stage can add:

- real road snapping
- heading-aware map matching
- road segment selection
- turn constraints
- GNSS initialization
- offline OSM data
- 3D quaternion state
- accelerometer gravity compensation
- bias estimation
