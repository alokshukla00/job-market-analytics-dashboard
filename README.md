# 📊 Job Market Analytics Dashboard

An interactive data analytics project that explores data science job salaries, experience levels, job titles, company locations, and remote-work patterns using Python and Streamlit.

The dashboard helps users explore salary data through interactive filters, visualizations, summary metrics, and SQL-based analysis.

## 🚀 Live Demo

**Live Dashboard:** Add your Streamlit deployment URL here

## 📸 Dashboard Preview

Add a screenshot of your running dashboard below.

![Job Market Analytics Dashboard](screenshots/your-screenshot.png)

> Replace `your-screenshot.png` with the actual screenshot filename inside the `screenshots` folder.

## 🎯 Project Objectives

- Explore salary patterns across data science roles.
- Compare compensation by experience level and job title.
- Analyze company locations and remote-work arrangements.
- Use SQL to summarize salary data.
- Build an interactive dashboard for exploratory data analysis.

## ✨ Features

- Interactive filters for work year, experience level, job title, company location, and remote-work ratio.
- Average and median salary metrics.
- Salary distribution analysis.
- Job-title and company-location exploration.
- Remote-work arrangement comparison.
- SQL summary grouped by experience level.
- Download filtered records as a CSV file.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data cleaning and analysis |
| SQLite | SQL-based data analysis |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard interface |

## 📂 Project Structure

```text
job-market-analytics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── screenshots/
└── data/
    └── ds_salaries.csv
```

The dataset is downloaded separately and placed inside the `data` directory.

## 📊 Dataset

**Dataset:** Data Science Job Salaries

**Source:** [Kaggle – Data Science Job Salaries](https://www.kaggle.com/datasets/rushi1990/data-science-job-salaries)

The dataset contains job-related information such as salary, experience level, employment type, job title, company location, and remote-work ratio.

Please review the dataset's license and attribution requirements before redistributing the data.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/alokshukla00/job-market-analytics-dashboard.git
cd job-market-analytics-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Download the dataset

Download the CSV file from the Kaggle dataset page and place it at:

```text
data/ds_salaries.csv
```

### 6. Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## 🔍 Key Analytical Areas

### Salary Analysis
Explore salary distributions and compare average and median compensation.

### Experience-Level Analysis
Understand how salary patterns vary across experience levels.

### Job-Title Analysis
Explore salary records across different data science job titles.

### Location Analysis
Compare job records and salary patterns across company locations.

### Remote-Work Analysis
Examine how remote-work ratios vary across roles and locations.

### SQL Analysis
Use SQLite queries to summarize salary data by experience level.

## 📌 Skills Demonstrated

- Data cleaning and exploratory data analysis
- Data manipulation using Pandas
- SQL querying with SQLite
- Interactive data visualization using Plotly
- Dashboard development using Streamlit
- Python project organization
- Data-driven analysis and presentation

## 👨‍💻 Author

**Alok Shukla**

- GitHub: [alokshukla00](https://github.com/alokshukla00)
- LinkedIn: [alok shukla](https://www.linkedin.com/in/alok-shukla-561915448/)

If you find this project useful, feel free to ⭐ the repository.
