<div align="center">

# 🏆 Athlete Training Analysis

### End-to-End Data Analytics Project | Python · SQL · PostgreSQL · Streamlit

*A comprehensive, portfolio-grade analytics project demonstrating the full data analyst workflow — from raw data ingestion and cleaning to advanced SQL querying and interactive dashboard development.*

---

**Python** · **Pandas** · **PostgreSQL** · **SQL** · **Streamlit** · **Plotly** · **Jupyter Notebook**

</div>

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Business Problem](#-business-problem)
3. [Dataset Details](#-dataset-details)
4. [Project Architecture](#-project-architecture)
5. [Data Cleaning & Preprocessing](#-data-cleaning--preprocessing)
6. [Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
7. [SQL Analysis (PostgreSQL)](#-sql-analysis-postgresql)
8. [KPI Metrics & Business Insights](#-kpi-metrics--business-insights)
9. [Streamlit Dashboard](#-streamlit-dashboard)
10. [Key Findings & Recommendations](#-key-findings--recommendations)
11. [Technologies Used](#-technologies-used)
12. [How to Run This Project](#-how-to-run-this-project)
13. [Future Scope](#-future-scope)

---

## 🎯 Project Overview

This project performs a **deep, multi-layered analysis** of athlete training data to extract actionable insights about workout performance, physiological health, and demographic trends. The workflow mirrors a real-world data analytics pipeline used in sports science, health-tech, and fitness industry analytics.

### What makes this project stand out:
- **Not just EDA** — includes engineered KPIs like *Consistency Score* and *Burn Efficiency*
- **Real database integration** — data is stored and queried from a live PostgreSQL instance
- **Interactive reporting** — a production-quality Streamlit dashboard with dynamic filters, insight cards, and recommendation engines
- **Business thinking** — every chart answers a specific business question, not just "what does the data look like"

---

## 💼 Business Problem

> *"A fitness organization wants to understand how different demographic groups (age, gender) respond to various workout types. They need to identify which training programs yield the highest calorie burn efficiency, detect health risk segments, and generate data-driven recommendations for personalized coaching."*

### Specific Questions Addressed:
| # | Business Question | Analysis Type |
|---|---|---|
| 1 | Which workout types burn the most calories per hour? | Efficiency Analysis |
| 2 | Does higher experience lead to better training consistency? | Trend Analysis |
| 3 | What is the BMI distribution across different age cohorts? | Health Risk Segmentation |
| 4 | Which athlete segments train at the highest intensity? | Heatmap Cross-Analysis |
| 5 | Is BMI a reliable proxy for body fat percentage? | Correlation Analysis |
| 6 | Which sports create the most cardiovascular stress? | Heart Rate Profiling |
| 7 | Who are the top 5% "elite" athletes by consistency? | KPI Engineering & Ranking |

---

## 📊 Dataset Details

### Source
The raw dataset (`gym_members_exercise_tracking.csv`) contains exercise tracking records for gym members. After cleaning, the final dataset (`cleaned_athlete_data.csv`) consists of **973 records** across **18 columns**.

### Schema

| Column | Data Type | Description |
|---|---|---|
| `age` | Integer | Athlete's age in years |
| `gender` | String | Male / Female |
| `weight_kg` | Float | Body weight in kilograms |
| `height_m` | Float | Height in meters |
| `max_bpm` | Integer | Maximum heart rate during workout |
| `avg_bpm` | Integer | Average heart rate during workout |
| `resting_bpm` | Integer | Resting heart rate |
| `session_duration_hours` | Float | Duration of single workout session |
| `calories_burned` | Float | Total calories burned per session |
| `workout_type` | String | Yoga / HIIT / Cardio / Strength |
| `fat_percentage` | Float | Body fat percentage |
| `water_intake_liters` | Float | Daily water consumption |
| `workout_frequency_days/week` | Integer | Training days per week |
| `experience_level` | Integer | 1 (Beginner) to 3 (Advanced) |
| `bmi` | Float | Body Mass Index (weight/height²) |
| `age_group` | String | Derived: 18-24, 25-34, 35-44, 45+ |
| `workout_intensity` | Float | Derived: avg_bpm / max_bpm |
| `bmi_category` | String | Derived: Underweight / Normal / Overweight / Obese |

---

## 🏗️ Project Architecture

```
Athlete Training Analysis/
│
├── 📓 Notebook/
│   └── AthleteTrainingAnalysis.ipynb    # Data cleaning, EDA, visualizations
│
├── 📁 datasets/
│   ├── gym_members_exercise_tracking.csv  # Raw dataset
│   └── cleaned_athlete_data.csv           # Cleaned & feature-engineered dataset
│
├── 📁 sql_queries/
│   └── deep_analysis.sql                  # 25+ PostgreSQL analytical queries
│
├── 📁 scripts/
│   └── load_to_postgres.py                # Python → PostgreSQL data migration
│
├── 📁 images/
│   ├── correlation_heatmap.png            # EDA visualizations
│   ├── calories_by_workout.png
│   ├── bmi_vs_calories.png
│   └── ...
│
├── 📊 dashboard.py                        # Streamlit interactive dashboard
└── 📄 README.md                           # Project documentation
```

### Data Pipeline Flow

```
Raw CSV → Jupyter (Clean + EDA) → Cleaned CSV → Python Script → PostgreSQL → SQL Queries → Streamlit Dashboard
```

---

## 🧹 Data Cleaning & Preprocessing

All preprocessing was performed in `Notebook/AthleteTrainingAnalysis.ipynb`.

### Steps Performed:

1. **Column Standardization**
   - Renamed all columns to lowercase `snake_case` for SQL compatibility
   - Example: `Workout_Type` → `workout_type`

2. **Missing Value Treatment**
   - Numerical columns: Imputed with **median** (robust against outliers)
   - Categorical columns: Imputed with **mode** (most frequent value)

3. **Feature Engineering** (3 new columns created)

   | New Column | Formula | Purpose |
   |---|---|---|
   | `age_group` | Binned from `age` | Demographic segmentation |
   | `workout_intensity` | `avg_bpm / max_bpm` | Normalized effort metric |
   | `bmi_category` | WHO thresholds on `bmi` | Health risk classification |

4. **Data Validation**
   - Confirmed no duplicate rows
   - Verified all numerical ranges are physiologically plausible
   - Exported clean data to `cleaned_athlete_data.csv`

---

## 📈 Exploratory Data Analysis (EDA)

EDA was conducted using **Matplotlib** and **Seaborn** within the Jupyter Notebook.

### Key Visualizations Generated:

| Visualization | Insight |
|---|---|
| **Correlation Heatmap** | Identified strong positive correlation between BMI and fat percentage |
| **Calories by Workout Type** | HIIT and Strength training burn the most calories on average |
| **BMI vs. Calories Scatter** | Higher BMI does not necessarily lead to higher calorie burn |
| **Workout Frequency Distribution** | Most athletes train 3-4 days per week |
| **Gender-wise Calorie Comparison** | Minimal performance gap between genders |
| **Experience Level Analysis** | Advanced athletes show higher consistency but not proportionally higher burn |

---

## 🗄️ SQL Analysis (PostgreSQL)

The cleaned dataset was loaded into a **PostgreSQL database** (`Athlete`) using SQLAlchemy via `scripts/load_to_postgres.py`. A total of **25+ analytical queries** were written across multiple complexity levels.

### Query Categories:

#### 🟢 Beginner — Quick Aggregations
```sql
-- Total athletes and average calorie burn
SELECT COUNT(*) AS total_athletes, AVG(calories_burned) AS avg_calories
FROM athlete_training;
```

#### 🟡 Intermediate — Segmentation & Ranking
```sql
-- Rank athletes within each workout type by calories
SELECT gender, workout_type, calories_burned,
       RANK() OVER(PARTITION BY workout_type ORDER BY calories_burned DESC) AS rank
FROM athlete_training;
```

#### 🔴 Advanced — CTEs, Subqueries & KPI Engineering
```sql
-- Top 5% "Elite" Athletes by Consistency Score
SELECT gender, age, workout_type,
       ROUND(((workout_frequency * workout_intensity) / NULLIF(bmi, 0))::numeric, 3) AS score
FROM athlete_training
ORDER BY score DESC
LIMIT (SELECT COUNT(*) * 0.05 FROM athlete_training);
```

### Full Query Coverage:
- Conditional aggregation (`CASE WHEN`)
- Window functions (`RANK`, `ROW_NUMBER`)
- Common Table Expressions (CTEs)
- Subqueries (scalar and correlated)
- `HAVING` clause for filtered aggregations
- Cross-tabulation and pivot-style analysis

---

## 📐 KPI Metrics & Business Insights

### Engineered KPIs

| KPI | Formula | Business Value |
|---|---|---|
| **Burn Efficiency** | `calories_burned / session_duration_hours` | Measures calorie ROI per hour of training |
| **Consistency Score** | `(frequency × intensity) / BMI` | Identifies athletes who are consistent AND intense relative to body mass |
| **Heart Rate Reserve** | `max_bpm - avg_bpm` | Measures cardiovascular headroom — how close athletes train to their limit |
| **Body Composition Correlation** | `Pearson(BMI, fat_percentage)` | Validates whether BMI is a reliable health indicator for this population |
| **Cardiovascular Stress Gap** | `max_bpm - resting_bpm` | Identifies which sports create the most cardiac load |

### Dashboard-Level KPIs (Real-Time)

| Metric | Description |
|---|---|
| Total Participants | Count of athletes matching current filter |
| Avg Calorie Burn | Mean calories burned per session |
| Body Mass Index | Population average BMI |
| Training Intensity | Average workout intensity ratio |
| Peak Heart Rate | Average maximum BPM |
| Body Fat Ratio | Average fat percentage |

---

## 📊 Streamlit Dashboard

The interactive dashboard (`dashboard.py`) connects **directly to PostgreSQL** and renders real-time analytical views using **Plotly**.

### Dashboard Architecture

```
Sidebar Filters (Activity, Gender, Age)
    ↓
SQL WHERE clause dynamically constructed
    ↓
PostgreSQL queries executed via SQLAlchemy
    ↓
Results rendered as Plotly charts + Insight Cards
```

### Dashboard Sections (Visual Hierarchy)

| Level | Section | Components |
|---|---|---|
| **L0** | Header | Title, project description |
| **L1** | Executive KPIs | 6 metric cards (participants, calories, BMI, intensity, HR, fat) |
| **L2** | Training Intensity Overview | Heatmap: Age Cohort × Activity Category |
| **L3** | Population Segmentation | Donut chart (activity share), Sunburst (age→BMI), Radar (HR profile) |
| **L4** | Deep-Dive Tabs | Performance efficiency, body composition, raw data explorer |

### Interactive Features

- **Dynamic Filtering**: Sidebar filters update all charts and insight cards in real-time
- **Insight Cards** (💡): Auto-generated analytical observations based on live data
- **Recommendation Cards** (🎯): Actionable business suggestions derived from patterns
- **Data Export**: Download any filtered view as a CSV file
- **Search**: Full-text search across the raw dataset

### Chart Types Used

| Chart | Library | Purpose |
|---|---|---|
| Density Heatmap | Plotly Express | Intensity cross-analysis |
| Donut Chart | Plotly Express | Activity share distribution |
| Sunburst Chart | Plotly Express | Hierarchical age-BMI breakdown |
| Polar/Radar Chart | Plotly Express | Multi-zone heart rate profiling |
| Horizontal Bar | Plotly Express | Burn efficiency ranking |
| Scatter + OLS Trendline | Plotly Express | BMI vs. Fat correlation |
| Overlaid Histogram | Plotly Graph Objects | HR distribution comparison |

---

## 🔍 Key Findings & Recommendations

### Key Findings

1. **HIIT and Strength training** deliver the highest calorie burn per hour, making them the most time-efficient activities
2. **BMI and Fat Percentage** show a moderate-to-strong positive correlation, confirming BMI as a useful (but imperfect) health screening metric
3. **Experience level does not linearly increase calorie burn** — advanced athletes are more consistent but not always burning more
4. **The 45+ age group** maintains competitive training intensity, challenging assumptions about age-related performance decline
5. **Certain workout types** create significantly higher cardiovascular stress (resting-to-peak HR gap), warranting structured recovery protocols

### Business Recommendations

| Finding | Recommendation |
|---|---|
| HIIT has highest burn efficiency | Promote HIIT programs for time-constrained members |
| Low-intensity segments exist in specific age groups | Design progressive overload programs for underperforming cohorts |
| High cardiovascular stress in certain activities | Implement mandatory cool-down and recovery tracking |
| BMI is a limited fat proxy | Invest in direct body composition measurement tools |
| Top 5% athletes have distinct patterns | Create an "Elite Performance" membership tier with personalized coaching |

---

## 🛠️ Technologies Used

| Category | Technology | Usage |
|---|---|---|
| **Language** | Python 3.13 | Core programming language |
| **Data Processing** | Pandas, NumPy | Cleaning, transformation, feature engineering |
| **Visualization (EDA)** | Matplotlib, Seaborn | Static charts in Jupyter |
| **Database** | PostgreSQL 15 | Production data storage and querying |
| **ORM** | SQLAlchemy | Python-PostgreSQL bridge |
| **Dashboard** | Streamlit | Interactive web application |
| **Dashboard Charts** | Plotly Express, Plotly Graph Objects | Dynamic, interactive visualizations |
| **Notebook** | Jupyter Notebook | Exploratory analysis environment |
| **Statistics** | Statsmodels | OLS trendline regression |

---

## 🚀 How to Run This Project

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- Git (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/athlete-training-analysis.git
cd athlete-training-analysis
```

### Step 2: Install Dependencies
```bash
pip install pandas sqlalchemy psycopg2 streamlit plotly statsmodels
```

### Step 3: Set Up PostgreSQL
1. Create a database named `Athlete` in PostgreSQL
2. Update the connection credentials in `scripts/load_to_postgres.py` and `dashboard.py`

### Step 4: Load Data into PostgreSQL
```bash
python scripts/load_to_postgres.py
```

### Step 5: Run SQL Analysis (Optional)
Open `sql_queries/deep_analysis.sql` in pgAdmin or any SQL client and execute the queries.

### Step 6: Launch the Dashboard
```bash
streamlit run dashboard.py
```
The dashboard will open at `http://localhost:8501`

---

## 🔮 Future Scope

| Enhancement | Description |
|---|---|
| **Predictive Modeling** | Build ML models to predict calorie burn based on athlete profile |
| **Time-Series Analysis** | Track individual athlete progress over multiple sessions |
| **Clustering** | Use K-Means to discover natural athlete segments |
| **A/B Testing Framework** | Compare effectiveness of different training programs |
| **Cloud Deployment** | Deploy the Streamlit dashboard on Streamlit Cloud or AWS |
| **Real-Time Data Ingestion** | Connect to wearable APIs (Fitbit, Apple Health) for live data |
| **Power BI / Tableau Version** | Create an alternative dashboard for enterprise stakeholders |

---

<div align="center">

### 📬 Connect

If you found this project useful, feel free to ⭐ star the repository!

**Built with analytical rigor and a passion for data-driven decision making.**

</div>
