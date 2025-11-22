# 📌 SafeLA – Crime Analytics & Forecasting (2020–2025)

A complete end-to-end crime analytics project built as part of the **DEPI – Data Analyst Track (2025)**.
The project analyzes crime patterns in **Los Angeles from 2020 until mid-2025 (January 2020 → May 2025)** using multiple tools and dashboards.

This repository includes **cleaning scripts, dashboards, forecasting models, documentation**, and final insights.

---

## 🎯 Project Objective

To identify **high-risk crime zones, peak times, weapon trends, and victim demographics**, and to build a **2-year forecasting model** to support public safety decision-making.

---

## 🧩 Project Workflow

### **1. Data Collection**

* Source: Los Angeles Open Data Portal (2020 → May 2025)
* Raw dataset included 1M+ crime incidents

### **2. Data Cleaning & Preparation**

Performed across multiple tools:

#### ✔ Power Query (Excel) — by Nariman

* Removed nulls, normalized dates
* Extracted Year / Month / Weekday
* Created Time Period bucket
* Cleaned victim gender & premise types
* Cleaned coordinates (LAT/LON)
* Created `Victim_Age_Group`
* **Grouped 300+ Weapon Types into 10 categories**
* **Grouped 140+ Crime Types into 12 categories**

#### ✔ Python Cleaning Script — by Moataz

* Automated cleaning pipeline for the full dataset
* Data type correction
* Outlier handling
* Encoding & preprocessing
  🔗 **Python Cleaning File:**
  `/cleaning/cleaning_script_moataz.py`
  (Upload first → then copy the link here)

---

### **3. Exploratory Data Analysis (EDA) — Ziad**

* Crime distribution across areas
* Heatmaps: day × hour
* Correlation between weapon type & arrest outcome
* Victim gender/age patterns
* Insight generation for dashboards

---

### **4. Forecasting Model (Alaa)**

* Trained using **CatBoostRegressor**
* Predicts crime volume for **2025–2027**
* Accuracy: ~80%
* Output dataset exported and visualized in Tableau
* Forecasting dashboard summarizes:

  * Future hotspots
  * Expected crime trend
  * Risk zones over time

---

### **5. Visualization Dashboards**

Dashboards were created using **multiple tools**, each focusing on a specific angle:

#### 📊 **Tableau Dashboard (by Sara)**

* Overview KPIs
* Top Crime Types & Areas
* Victim demographics
* Weapons analysis
* Arrest vs No-Arrest patterns
* Geo-mapping
* Forecast interpretation

#### 📈 **Power BI Dashboard (by Moataz)**

* Time-series analysis
* Drill-downs by gender, crime type, weapon
* Map visualization
* Comparative trends year-over-year

#### 📉 **Excel Dashboard (by Nariman)**

* Pivot-based summary
* Slicers for Year/Area/Weapon
* KPI cards

#### 🐍 **Python Dashboard (Ziad)**

* Custom plots
* Statistical exploration
* Insight explanation

#### 📊 Forecast Tableau Dashboard (by Alaa)
 * Future hotspots
 * Expected crime trend
 * Risk zones over time
---

## 👥 Team Members

| Name               | Role                                                      |
| ------------------ | --------------------------------------------------------- |
| **Sara Farouk**    | Team Leader, Tableau, Documentation, PPT                  |
| **Nariman Yasser** | Excel Dashboard, Data Cleaning, Data Dictionary           |
| **Moataz Mostafa** | Python Cleaning, Power BI, QA                             |
| **Ziad Sayed**     | EDA, Python Dashboard, Insight Generation                 |
| **Alaa Ayman**     | Forecasting Model (CatBoost) + Tableau Forecast Dashboard |

---

## 🛠️ Tools & Technologies

* Python (Pandas, NumPy, Matplotlib, Seaborn, CatBoost, Scikit-learn)
* Tableau
* Power BI
* Excel (Power Query)
* GitHub
* Google Colab / Jupyter

---

## 📁 Repository Structure

```
📁 SafeLA-Data-Analytics
│
├── 📁 cleaning                 → PowerQuery output + Python cleaning scripts
├── 📁 dataset                  → Raw + cleaned datasets
├── 📁 dashboards
│      ├── tableau
│      ├── powerbi
│      ├── excel
│      └── python
│
├── 📁 forecasting              → Model notebook + forecasted datasets
│
├── 📁 documentation
│      └── Project Documentation.pdf
│
└── README.md
```

---

## 📄 Documentation

Full project documentation (problem statement, methodology, dashboards, insights, forecasting model):
📌 `/documentation/Project Documentation.pdf`

---

### 📁 Dataset Source
- Crime Data from 2020 to Present – [catalog.data.gov](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)

---

## 🏆 Final Outcome

This project demonstrates how multi-tool analytics (Python + Excel + Power BI + Tableau) can produce an evidence-based approach for predicting and reducing crime in Los Angeles.

---
