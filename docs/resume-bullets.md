# Resume Bullets

- Built a public dbt analytics project on NYC taxi trip data with staged, intermediate, and mart models, schema tests, auto-generated documentation, and GitHub Actions CI to demonstrate production analytics engineering practices.
- Modeled taxi demand, route revenue, trip duration, and tipping behavior in DuckDB-backed dbt marts, with documented business questions and reproducible local setup for reviewers.

## Interview Explanation

I built this project to make my analytics engineering work publicly reviewable. It shows how I structure a dbt project from raw inputs through reusable transformations and stakeholder-facing marts, then enforce data quality with tests and CI. The implementation is intentionally local-first with DuckDB so a recruiter or interviewer can clone it and run the full build without cloud credentials.
