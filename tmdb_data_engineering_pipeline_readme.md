# TMDB Data Engineering Pipeline 🎬📊

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg)
![Seaborn](https://img.shields.io/badge/Seaborn-Data_Visualization-3776ab.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## Project Overview
This repository contains an end-to-end Data Engineering and Analytics pipeline built for the **AmaliTech Apprenticeship Programme (DEM02)**. The project demonstrates the extraction of movie telemetry from the TMDB REST API, extensive data cleaning, relational data enrichment, KPI generation, and statistical visualization.

**Author:** Dushimimana Prince  
**Role:** Data Engineering Apprentice, AmaliTech (Rwanda)

---

## 🏗️ Pipeline Architecture (ETL)

The project is broken down into four primary phases, mirroring a professional Medallion architecture (Bronze -> Silver -> Gold).

### Phase 1: Data Extraction
* Iterated through a curated list of movie IDs (including specific Bruce Willis and Quentin Tarantino titles) to query the `api.themoviedb.org/3/movie/{id}` endpoint.
* **Relational Enrichment:** Implemented a secondary fetch to the `/credits` endpoint to extract nested cast and director dictionaries, seamlessly merging them into the primary dataset via a Pandas Left Join.

### Phase 2: Cleaning & Preprocessing
* Flattened nested JSON objects into pipe-delimited (`|`) strings.
* Resolved `TypeError: unhashable type: 'list'` during deduplication by enforcing subset validation (`subset=['id']`).
* Cast financial strings to floats and scaled metrics to Millions USD (MUSD) for analytical readability.

### Phase 3: KPI Engineering & Analytics
* Engineered new performance metrics: **Profit (MUSD)** and **Return on Investment (ROI)**.
* Built a reusable User-Defined Function (UDF) to dynamically rank movies based on customizable parameters (e.g., minimum budget, minimum vote count).
* Solved complex multi-conditional boolean masking challenges (resolving `InvalidIndexError`) to execute advanced string searches for specific actors and directors.
* Categorized data using `np.where()` to compare "Franchise" vs. "Standalone" business models.

### Phase 4: Export & Visualization
* Exported the finalized, clean "Gold Layer" dataset to `data/tmdb_movies_clean.csv` for state persistence and downstream BI usage.
* Utilized **Matplotlib** and **Seaborn** to generate five core visual insights:
  1. Revenue vs. Budget Regression Trends
  2. ROI Distribution by Genre (utilizing Pandas `.explode()` to map one-to-many movie-to-genre relationships)
  3. 4-Dimensional Popularity vs. Rating Scatter Plots
  4. Yearly Box Office Performance Time-Series
  5. Franchise vs. Standalone Grouped Bar Charts

---

## 🛠️ Tech Stack
* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn
* **Requests:** `requests` (REST API Integration)
* **Environment:** Jupyter Notebook / VS Code
* **Version Control:** Git (Feature-Branch Workflow)

---

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Dushimimanaprince/TMDB-Movie-Data-Analysis.git
cd TMDB-Movie-Data-Analysis
```

**2. Install dependencies**
Ensure you have Python installed, then run:
```bash
pip install pandas numpy matplotlib seaborn requests
```

**3. Configure API Key**
You will need a free API Key from [The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api). 
* Open the Jupyter Notebook.
* Replace the `API_KEY` variable at the top of the extraction cell with your personal key.

**4. Execute the Pipeline**
Run the Jupyter Notebook cells sequentially from top to bottom. The final cell will automatically generate the clean `.csv` artifact and render the visual dashboard.

---

## 📈 Key Engineering Highlights
* **Data Enrichment:** Successfully handled "Missing by Design" API architecture by stitching together separate endpoint payloads.
* **One-to-Many Transformation:** Utilized `.assign()` and `.explode()` to accurately chart boxplots for movies belonging to multiple genres without dropping or duplicating financial realities.
* **Feature Branching:** Maintained clean version history by utilizing standard Git workflows (`feature/extraction`, `feature/data-cleaning`, `feature/data-visualization`).