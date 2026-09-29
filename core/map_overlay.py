import numpy as np
import folium


def local_to_latlon(
    x_m,
    y_m,
    center
):

    lat0, lon0 = center

    latitude = (
        lat0
        +
        y_m / 111320.0
    )

    longitude = (
        lon0
        +
        x_m
        /
        (
            111320.0
            *
            np.cos(
                np.radians(lat0)
            )
        )
    )

    return latitude, longitude


def create_map(
    trajectory,
    center
):

    points = []


    for _, row in trajectory.iterrows():

        lat, lon = local_to_latlon(
            row["x_m"],
            row["y_m"],
            center
        )

        points.append(
            [lat, lon]
        )


    if not points:

        points = [
            [
                center[0],
                center[1]
            ]
        ]


    # -----------------------------------------------------
    # Map
    # -----------------------------------------------------

    fmap = folium.Map(
        location=center,
        zoom_start=16,
        tiles="OpenStreetMap"
    )


    # -----------------------------------------------------
    # Full trajectory
    # -----------------------------------------------------

    folium.PolyLine(
        points,
        color="blue",
        weight=6,
        opacity=0.85,
        tooltip="Fused Dead Reckoning"
    ).add_to(fmap)


    # -----------------------------------------------------
    # Start
    # -----------------------------------------------------

    folium.Marker(
        points[0],
        tooltip="Start",
        popup="Dead Reckoning Start",
        icon=folium.Icon(
            color="green"
        )
    ).add_to(fmap)


    # -----------------------------------------------------
    # Current / End
    # -----------------------------------------------------

    folium.Marker(
        points[-1],
        tooltip="Current Position",
        popup="Current Dead Reckoning Position",
        icon=folium.Icon(
            color="red"
        )
    ).add_to(fmap)


    # -----------------------------------------------------
    # Right-turn marker
    # -----------------------------------------------------

    if len(points) > 300:

        turn_index = min(
            300,
            len(points) - 1
        )

        folium.Marker(
            points[turn_index],
            tooltip="Right Turn",
            popup="Approx. 300 m → Right Turn",
            icon=folium.Icon(
                color="orange",
                icon="arrow-right"
            )
        ).add_to(fmap)


    # -----------------------------------------------------
    # Fit trajectory
    # -----------------------------------------------------

    fmap.fit_bounds(
        points
    )


    return fmap