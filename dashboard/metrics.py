from __future__ import annotations

import pandas as pd


def build_kpi_summary(trips: pd.DataFrame) -> dict[str, float | int]:
    if trips.empty:
        return {
            "total_trips": 0,
            "gross_revenue": 0.0,
            "avg_total_amount": 0.0,
            "avg_tip_share": 0.0,
        }

    return {
        "total_trips": int(trips["trip_id"].nunique()),
        "gross_revenue": round(float(trips["total_amount"].sum()), 2),
        "avg_total_amount": round(float(trips["total_amount"].mean()), 2),
        "avg_tip_share": round(float(trips["tip_share"].mean()), 4),
    }


def build_route_leaderboard(routes: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    if routes.empty:
        return pd.DataFrame(
            columns=[
                "route",
                "distance_band",
                "trip_count",
                "gross_revenue",
                "avg_total_amount",
                "avg_tip_share",
            ]
        )

    leaderboard = routes.copy()
    leaderboard["route"] = (
        leaderboard["pickup_borough"].astype(str)
        + " -> "
        + leaderboard["dropoff_borough"].astype(str)
    )
    return (
        leaderboard.sort_values(["gross_revenue", "avg_total_amount"], ascending=[False, False])
        .head(limit)
        .reset_index(drop=True)
    )


def build_tipping_by_distance(trips: pd.DataFrame) -> pd.DataFrame:
    if trips.empty:
        return pd.DataFrame(columns=["distance_band", "avg_tip_share", "trip_count"])

    order = {"short": 0, "medium": 1, "long": 2}
    summary = (
        trips.groupby("distance_band", as_index=False)
        .agg(avg_tip_share=("tip_share", "mean"), trip_count=("tip_share", "count"))
        .assign(
            avg_tip_share=lambda frame: frame["avg_tip_share"].round(4),
            _sort=lambda frame: frame["distance_band"].map(order).fillna(99),
        )
        .sort_values(["_sort", "distance_band"])
        .drop(columns=["_sort"])
        .reset_index(drop=True)
    )
    return summary


def build_revenue_by_borough(daily_metrics: pd.DataFrame) -> pd.DataFrame:
    if daily_metrics.empty:
        return pd.DataFrame(columns=["pickup_borough", "gross_revenue", "trip_count"])

    return (
        daily_metrics.groupby("pickup_borough", as_index=False)
        .agg(gross_revenue=("gross_revenue", "sum"), trip_count=("trip_count", "sum"))
        .sort_values("gross_revenue", ascending=False)
        .reset_index(drop=True)
    )
