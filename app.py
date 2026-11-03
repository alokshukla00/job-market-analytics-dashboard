from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "ds_salaries.csv"


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load the CSV dataset and perform basic cleaning."""
    df = pd.read_csv(file_path)

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Convert numeric columns when available
    numeric_columns = [
        "work_year",
        "salary",
        "salary_in_usd",
        "remote_ratio",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows without salary in USD if that column exists
    if "salary_in_usd" in df.columns:
        df = df.dropna(subset=["salary_in_usd"])

    return df


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def get_available_values(df: pd.DataFrame, column: str) -> list:
    """Return sorted, non-null unique values from a column."""
    if column not in df.columns:
        return []

    return sorted(df[column].dropna().unique().tolist())


def format_salary(value) -> str:
    """Format salary values for display."""
    if pd.isna(value):
        return "N/A"

    return f"${value:,.0f}"


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 Job Market Analytics Dashboard")

st.markdown(
    """
    Explore data-science job salaries, experience levels, job titles,
    company locations, and remote-work patterns.
    """
)

st.caption(
    "Dataset: Data Science Job Salaries | "
    "This dashboard analyzes the dataset provided locally."
)


# ---------------------------------------------------------
# CHECK DATASET
# ---------------------------------------------------------
if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Please place the CSV file here:"
    )

    st.code("data/ds_salaries.csv")

    st.markdown(
        """
        **Expected folder structure:**

        ```text
        job-market-analytics-dashboard/
        ├── app.py
        └── data/
            └── ds_salaries.csv
        ```
        """
    )

    st.stop()


df = load_data(str(DATA_PATH))


# ---------------------------------------------------------
# VALIDATE EXPECTED COLUMNS
# ---------------------------------------------------------
required_columns = [
    "job_title",
    "experience_level",
    "company_location",
    "salary_in_usd",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing expected columns: "
        + ", ".join(missing_columns)
    )

    st.write("Columns found:", list(df.columns))
    st.stop()


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Filter the Data")

filtered_df = df.copy()

if "work_year" in filtered_df.columns:
    years = get_available_values(filtered_df, "work_year")

    selected_years = st.sidebar.multiselect(
        "Work Year",
        options=years,
        default=years,
    )

    filtered_df = filtered_df[
        filtered_df["work_year"].isin(selected_years)
    ]


experience_levels = get_available_values(
    filtered_df,
    "experience_level",
)

selected_experience = st.sidebar.multiselect(
    "Experience Level",
    options=experience_levels,
    default=experience_levels,
)

filtered_df = filtered_df[
    filtered_df["experience_level"].isin(selected_experience)
]


job_titles = get_available_values(filtered_df, "job_title")

selected_jobs = st.sidebar.multiselect(
    "Job Title",
    options=job_titles,
    default=job_titles,
)

filtered_df = filtered_df[
    filtered_df["job_title"].isin(selected_jobs)
]


locations = get_available_values(
    filtered_df,
    "company_location",
)

selected_locations = st.sidebar.multiselect(
    "Company Location",
    options=locations,
    default=locations,
)

filtered_df = filtered_df[
    filtered_df["company_location"].isin(selected_locations)
]


if "remote_ratio" in filtered_df.columns:
    remote_values = get_available_values(
        filtered_df,
        "remote_ratio",
    )

    selected_remote = st.sidebar.multiselect(
        "Remote Ratio",
        options=remote_values,
        default=remote_values,
        help="0 = on-site, 50 = hybrid, 100 = fully remote",
    )

    filtered_df = filtered_df[
        filtered_df["remote_ratio"].isin(selected_remote)
    ]


# ---------------------------------------------------------
# HANDLE EMPTY FILTER RESULTS
# ---------------------------------------------------------
if filtered_df.empty:
    st.warning(
        "No records match the selected filters. "
        "Try changing or clearing some filters."
    )

    st.stop()


# ---------------------------------------------------------
# KPI METRICS
# ---------------------------------------------------------
total_records = len(filtered_df)

average_salary = filtered_df["salary_in_usd"].mean()

median_salary = filtered_df["salary_in_usd"].median()

unique_job_titles = filtered_df["job_title"].nunique()

unique_locations = filtered_df["company_location"].nunique()


metric1, metric2, metric3, metric4, metric5 = st.columns(5)

metric1.metric(
    "Job Records",
    f"{total_records:,}",
)

metric2.metric(
    "Average Salary",
    format_salary(average_salary),
)

metric3.metric(
    "Median Salary",
    format_salary(median_salary),
)

metric4.metric(
    "Unique Job Titles",
    f"{unique_job_titles:,}",
)

metric5.metric(
    "Company Locations",
    f"{unique_locations:,}",
)


st.divider()

# ---------------------------------------------------------
# YEARLY SALARY TREND
# ---------------------------------------------------------
if "work_year" in filtered_df.columns:
    st.subheader("📈 Salary Trend Over Time")

    yearly_salary = (
        filtered_df
        .groupby("work_year", as_index=False)
        .agg(
            median_salary=("salary_in_usd", "median"),
            job_records=("salary_in_usd", "count"),
        )
        .sort_values("work_year")
    )

    if not yearly_salary.empty:
        fig_yearly_salary = px.line(
            yearly_salary,
            x="work_year",
            y="median_salary",
            markers=True,
            title="Median Salary by Work Year",
            labels={
                "work_year": "Work Year",
                "median_salary": "Median Salary (USD)",
            },
            hover_data=["job_records"],
        )

        st.plotly_chart(
            fig_yearly_salary,
            use_container_width=True,
        )

        st.caption(
            "Salary trends are based on the records selected "
            "in the sidebar filters."
        )

# ---------------------------------------------------------
# SALARY ANALYSIS
# ---------------------------------------------------------
st.subheader("💰 Salary Analysis")

salary_col1, salary_col2 = st.columns(2)


with salary_col1:
    salary_by_experience = (
        filtered_df
        .groupby("experience_level", as_index=False)["salary_in_usd"]
        .median()
        .sort_values("salary_in_usd", ascending=False)
    )

    fig_salary_experience = px.bar(
        salary_by_experience,
        x="experience_level",
        y="salary_in_usd",
        title="Median Salary by Experience Level",
        labels={
            "experience_level": "Experience Level",
            "salary_in_usd": "Median Salary (USD)",
        },
        text_auto=".2s",
    )

    st.plotly_chart(
        fig_salary_experience,
        use_container_width=True,
    )


with salary_col2:
    fig_salary_distribution = px.histogram(
        filtered_df,
        x="salary_in_usd",
        nbins=30,
        title="Salary Distribution",
        labels={
            "salary_in_usd": "Salary (USD)",
        },
    )

    st.plotly_chart(
        fig_salary_distribution,
        use_container_width=True,
    )


# ---------------------------------------------------------
# JOB TITLE ANALYSIS
# ---------------------------------------------------------
st.subheader("💼 Job Title Analysis")

top_job_titles = (
    filtered_df["job_title"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_job_titles.columns = [
    "job_title",
    "number_of_jobs",
]

fig_top_jobs = px.bar(
    top_job_titles.sort_values("number_of_jobs"),
    x="number_of_jobs",
    y="job_title",
    orientation="h",
    title="Top 10 Job Titles by Number of Records",
    labels={
        "job_title": "Job Title",
        "number_of_jobs": "Number of Records",
    },
)

st.plotly_chart(
    fig_top_jobs,
    use_container_width=True,
)


# ---------------------------------------------------------
# LOCATION ANALYSIS
# ---------------------------------------------------------
st.subheader("🌍 Company Location Analysis")

location_salary = (
    filtered_df
    .groupby("company_location", as_index=False)
    .agg(
        median_salary=("salary_in_usd", "median"),
        job_records=("job_title", "count"),
    )
    .sort_values("job_records", ascending=False)
    .head(15)
)

fig_location = px.bar(
    location_salary.sort_values("job_records"),
    x="job_records",
    y="company_location",
    orientation="h",
    title="Top 15 Company Locations by Job Records",
    labels={
        "company_location": "Company Location",
        "job_records": "Number of Records",
    },
    hover_data=["median_salary"],
)

st.plotly_chart(
    fig_location,
    use_container_width=True,
)


# ---------------------------------------------------------
# REMOTE WORK ANALYSIS
# ---------------------------------------------------------
if "remote_ratio" in filtered_df.columns:
    st.subheader("🏠 Remote Work Analysis")

    remote_mapping = {
        0: "On-site",
        50: "Hybrid",
        100: "Fully Remote",
    }

    remote_df = filtered_df.copy()

    remote_df["remote_type"] = (
        remote_df["remote_ratio"]
        .map(remote_mapping)
        .fillna("Other")
    )

    remote_summary = (
        remote_df
        .groupby("remote_type", as_index=False)
        .agg(
            job_records=("job_title", "count"),
            median_salary=("salary_in_usd", "median"),
        )
    )

    remote_col1, remote_col2 = st.columns(2)

    with remote_col1:
        fig_remote_count = px.pie(
            remote_summary,
            names="remote_type",
            values="job_records",
            title="Job Records by Work Arrangement",
        )

        st.plotly_chart(
            fig_remote_count,
            use_container_width=True,
        )

    with remote_col2:
        fig_remote_salary = px.bar(
            remote_summary,
            x="remote_type",
            y="median_salary",
            title="Median Salary by Work Arrangement",
            labels={
                "remote_type": "Work Arrangement",
                "median_salary": "Median Salary (USD)",
            },
            text_auto=".2s",
        )

        st.plotly_chart(
            fig_remote_salary,
            use_container_width=True,
        )


# ---------------------------------------------------------
# SQL ANALYSIS
# ---------------------------------------------------------
st.subheader("🧮 SQL Summary")

# Create an in-memory SQLite database
connection = sqlite3.connect(":memory:")

filtered_df.to_sql(
    "job_salaries",
    connection,
    index=False,
    if_exists="replace",
)

sql_query = """
SELECT
    experience_level,
    COUNT(*) AS job_records,
    ROUND(AVG(salary_in_usd), 2) AS average_salary_usd,
    ROUND(
        (SELECT salary_in_usd
         FROM job_salaries AS inner_table
         WHERE inner_table.experience_level = outer_table.experience_level
         ORDER BY salary_in_usd
         LIMIT 1 OFFSET (
             SELECT COUNT(*) / 2
             FROM job_salaries AS median_table
             WHERE median_table.experience_level =
                   outer_table.experience_level
         )),
        2
    ) AS middle_salary_record
FROM job_salaries AS outer_table
GROUP BY experience_level
ORDER BY average_salary_usd DESC;
"""

# Simpler SQL summary for display
sql_summary_query = """
SELECT
    experience_level,
    COUNT(*) AS job_records,
    ROUND(AVG(salary_in_usd), 2) AS average_salary_usd,
    ROUND(MIN(salary_in_usd), 2) AS minimum_salary_usd,
    ROUND(MAX(salary_in_usd), 2) AS maximum_salary_usd
FROM job_salaries
GROUP BY experience_level
ORDER BY average_salary_usd DESC;
"""

sql_summary = pd.read_sql_query(
    sql_summary_query,
    connection,
)

st.dataframe(
    sql_summary,
    use_container_width=True,
    hide_index=True,
)

connection.close()

# ---------------------------------------------------------
# AUTOMATIC DATA INSIGHTS
# ---------------------------------------------------------
st.subheader("🔍 Key Insights")

insight_col1, insight_col2 = st.columns(2)

# Highest median salary by experience level
salary_experience_insights = (
    filtered_df
    .groupby("experience_level")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
)

with insight_col1:
    if not salary_experience_insights.empty:
        highest_experience = salary_experience_insights.index[0]
        highest_experience_salary = salary_experience_insights.iloc[0]

        st.info(
            f"**Highest median salary by experience level:** "
            f"{highest_experience} — "
            f"${highest_experience_salary:,.0f}"
        )

# Most frequent job title
job_title_counts = filtered_df["job_title"].value_counts()

with insight_col2:
    if not job_title_counts.empty:
        most_common_job = job_title_counts.index[0]
        most_common_count = job_title_counts.iloc[0]

        st.info(
            f"**Most frequent job title in this selection:** "
            f"{most_common_job} "
            f"({most_common_count} records)"
        )

# ---------------------------------------------------------
# FILTERED DATA TABLE
# ---------------------------------------------------------
with st.expander("View Filtered Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_job_market_data.csv",
    mime="text/csv",
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "Built with Python, Pandas, SQLite, Plotly, and Streamlit."
)