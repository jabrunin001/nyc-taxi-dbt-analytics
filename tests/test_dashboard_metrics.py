import pandas as pd

from dashboard.metrics import (
    build_kpi_summary,
    build_route_leaderboard,
    build_tipping_by_distance,
)


def test_build_kpi_summary_rolls_up_business_metrics():
    trips = pd.DataFrame(
        [
            {"trip_id": 1, "total_amount": 20.0, "tip_share": 0.15},
            {"trip_id": 2, "total_amount": 40.0, "tip_share": 0.20},
        ]
    )

    assert build_kpi_summary(trips) == {
        "total_trips": 2,
        "gross_revenue": 60.0,
        "avg_total_amount": 30.0,
        "avg_tip_share": 0.175,
    }


def test_build_route_leaderboard_adds_route_label_and_sorts_by_revenue():
    routes = pd.DataFrame(
        [
            {
                "pickup_borough": "Brooklyn",
                "dropoff_borough": "Queens",
                "distance_band": "medium",
                "trip_count": 3,
                "gross_revenue": 90.0,
                "avg_total_amount": 30.0,
                "avg_tip_share": 0.10,
            },
            {
                "pickup_borough": "Queens",
                "dropoff_borough": "Manhattan",
                "distance_band": "long",
                "trip_count": 2,
                "gross_revenue": 140.0,
                "avg_total_amount": 70.0,
                "avg_tip_share": 0.18,
            },
        ]
    )

    leaderboard = build_route_leaderboard(routes)

    assert leaderboard[["route", "gross_revenue"]].to_dict("records") == [
        {"route": "Queens -> Manhattan", "gross_revenue": 140.0},
        {"route": "Brooklyn -> Queens", "gross_revenue": 90.0},
    ]


def test_build_tipping_by_distance_groups_fact_rows():
    trips = pd.DataFrame(
        [
            {"distance_band": "short", "tip_share": 0.10},
            {"distance_band": "short", "tip_share": 0.20},
            {"distance_band": "long", "tip_share": 0.30},
        ]
    )

    summary = build_tipping_by_distance(trips)

    assert summary.to_dict("records") == [
        {"distance_band": "short", "avg_tip_share": 0.15, "trip_count": 2},
        {"distance_band": "long", "avg_tip_share": 0.30, "trip_count": 1},
    ]
