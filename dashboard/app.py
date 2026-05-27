from __future__ import annotations

import streamlit as st
import plotly.express as px

from dashboard.data_access import DEFAULT_DUCKDB_PATH, database_exists, load_dashboard_tables
from dashboard.metrics import (
    build_kpi_summary,
    build_revenue_by_borough,
    build_route_leaderboard,
    build_tipping_by_distance,
)


st.set_page_config(
    page_title="NYC Taxi Metrics Command Center",
    page_icon="T",
    layout="wide",
)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #070b12;
            --panel: #0d1524;
            --panel-2: #111b2d;
            --line: rgba(140, 167, 214, 0.22);
            --text: #e7edf8;
            --muted: #8ea3c3;
            --gold: #f4c76b;
            --cyan: #57d8ff;
            --green: #6ee7a8;
        }
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(87, 216, 255, 0.16), transparent 32rem),
                radial-gradient(circle at top right, rgba(244, 199, 107, 0.11), transparent 28rem),
                var(--bg);
            color: var(--text);
        }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(17, 27, 45, 0.94), rgba(9, 15, 27, 0.96));
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 18px 18px 14px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28);
        }
        .hero {
            border: 1px solid var(--line);
            border-radius: 28px;
            padding: 30px;
            margin-bottom: 18px;
            background:
                linear-gradient(135deg, rgba(13, 21, 36, 0.96), rgba(11, 18, 31, 0.78)),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.035) 0 1px, transparent 1px 72px);
        }
        .eyebrow {
            color: var(--gold);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .hero h1 {
            color: var(--text);
            font-size: 3rem;
            letter-spacing: -0.06em;
            margin: 0 0 8px;
        }
        .hero p, .insight-card p {
            color: var(--muted);
            font-size: 1rem;
            margin: 0;
        }
        .insight-card {
            background: rgba(17, 27, 45, 0.82);
            border: 1px solid var(--line);
            border-left: 4px solid var(--cyan);
            border-radius: 18px;
            padding: 18px 20px;
            margin: 12px 0 18px;
        }
        .section-title {
            color: var(--text);
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-top: 24px;
        }
        .small-note {
            color: var(--muted);
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def money(value: float) -> str:
    return f"${value:,.2f}"


def percent(value: float) -> str:
    return f"{value:.1%}"


def main() -> None:
    apply_theme()

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Analytics Engineering Portfolio Demo</div>
            <h1>NYC Taxi Metrics Command Center</h1>
            <p>Canonical dbt metrics translated into executive-ready answers: where demand concentrates, which routes create value, and whether the metrics can be trusted.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not database_exists():
        st.error(f"DuckDB database not found at `{DEFAULT_DUCKDB_PATH}`.")
        st.info("Run `dbt build --profiles-dir .` from the repo root, then restart this dashboard.")
        return

    tables = load_dashboard_tables()
    trips = tables["trips"]
    daily_metrics = tables["daily_metrics"]
    route_revenue = tables["route_revenue"]

    kpis = build_kpi_summary(trips)
    revenue_by_borough = build_revenue_by_borough(daily_metrics)
    route_leaderboard = build_route_leaderboard(route_revenue)
    tipping_by_distance = build_tipping_by_distance(trips)

    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Trips Modeled", f"{kpis['total_trips']:,}")
    kpi_cols[1].metric("Gross Revenue", money(float(kpis["gross_revenue"])))
    kpi_cols[2].metric("Avg Fare", money(float(kpis["avg_total_amount"])))
    kpi_cols[3].metric("Avg Tip Share", percent(float(kpis["avg_tip_share"])))

    st.markdown(
        """
        <div class="insight-card">
            <div class="eyebrow">Business Readout</div>
            <p>This dashboard sits on top of the dbt mart layer, so every chart is traceable to a tested model instead of an ad hoc notebook query.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.1, 0.9])
    with left:
        st.markdown('<div class="section-title">Where is revenue concentrated?</div>', unsafe_allow_html=True)
        fig = px.bar(
            revenue_by_borough,
            x="pickup_borough",
            y="gross_revenue",
            color="pickup_borough",
            text_auto=".2s",
            template="plotly_dark",
            color_discrete_sequence=["#57d8ff", "#f4c76b", "#6ee7a8", "#b389ff"],
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Which routes are highest value?</div>', unsafe_allow_html=True)
        display_routes = route_leaderboard[
            ["route", "distance_band", "trip_count", "gross_revenue", "avg_total_amount", "avg_tip_share"]
        ].copy()
        display_routes["gross_revenue"] = display_routes["gross_revenue"].map(money)
        display_routes["avg_total_amount"] = display_routes["avg_total_amount"].map(money)
        display_routes["avg_tip_share"] = display_routes["avg_tip_share"].map(percent)
        st.dataframe(display_routes, hide_index=True, use_container_width=True)

    st.markdown('<div class="section-title">How does trip distance change tipping behavior?</div>', unsafe_allow_html=True)
    tip_fig = px.bar(
        tipping_by_distance,
        x="distance_band",
        y="avg_tip_share",
        color="distance_band",
        text_auto=".1%",
        template="plotly_dark",
        color_discrete_sequence=["#6ee7a8", "#57d8ff", "#f4c76b"],
    )
    tip_fig.update_layout(showlegend=False, yaxis_tickformat=".0%", margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(tip_fig, use_container_width=True)

    catalog, quality = st.columns([1, 1])
    with catalog:
        st.markdown('<div class="section-title">Metric Catalog</div>', unsafe_allow_html=True)
        st.dataframe(
            [
                {"Metric": "Gross Revenue", "Definition": "Sum of total_amount", "Source": "fct_taxi_trips"},
                {"Metric": "Trip", "Definition": "One completed pickup-to-dropoff record", "Source": "fct_taxi_trips"},
                {"Metric": "Route", "Definition": "Pickup borough to dropoff borough by distance band", "Source": "mart_route_revenue"},
                {"Metric": "Tip Share", "Definition": "tip_amount divided by total_amount", "Source": "int_taxi_trip_metrics"},
            ],
            hide_index=True,
            use_container_width=True,
        )

    with quality:
        st.markdown('<div class="section-title">Trust And Freshness</div>', unsafe_allow_html=True)
        max_service_date = trips["service_date"].max()
        st.markdown(
            f"""
            <div class="insight-card">
                <p><strong>Latest service date:</strong> {max_service_date}</p>
                <p><strong>Validated models:</strong> staging, intermediate, fact, daily mart, route mart</p>
                <p><strong>Quality gates:</strong> 23 dbt data tests covering keys, accepted values, and non-negative measures.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("Portfolio note: the included seed is intentionally small for fast CI. The same dashboard pattern can point at full NYC TLC trip files.")


if __name__ == "__main__":
    main()
