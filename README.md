Formula 1 Race Position Prediction

OVERVIEW
- Predict Formula 1 drivers’ race finishing positions using historical race data
- Apply extensive EDA, feature engineering, and ML model building
- Models used: **XGBoost** and **scikit-learn**
- Dataset compiled from multiple CSV files (circuits, drivers, constructors, races, results)


---

PROJECT STRUCTURE
- **data/** – Contains all dataset CSV files used in the project
  - `circuits.csv` – Circuit details (location, country, etc.)
  - `constructors.csv` – Constructor information
  - `drivers.csv` – Driver information
  - `results.csv` – Race result records
  - *(and other supporting datasets)*
- **F1_EDA.ipynb** – Notebook for data cleaning, preprocessing, and visualizations
- **F1_model.ipynb** – Notebook for feature engineering, model training, and evaluation
- **README.md** – Project documentation

 
DATASETS USED
The `data/` folder contains:
- **circuits.csv** — Circuit details (location, country, etc.)
- **constructors.csv** — Constructor information
- **drivers.csv** — Driver information
- **results.csv** — Race result records
- **lap_times.csv** — Lap-by-lap timings
- **qualifying.csv** — Qualifying session results
- **pit_stops.csv** — Pit stop data
- *(and other supporting datasets)*

Source: [Kaggle Formula 1 Dataset](https://www.kaggle.com/datasets) (originally fetched from the [Ergast API](https://ergast.com/mrd/)).

---

TECH STACK
- **Languages:** Python
- **Libraries:** Pandas, NumPy, Scikit-learn, XGBoost, Matplotlib, Seaborn, Jupyter
- **Techniques:** EDA, Feature Engineering, Regression Models, Model Evaluation

---

HOW TO RUN
1. **Clone the repository**
   ```bash
   git clone https://github.com/pranavdubey1725/F1-Race-Prediction.git
   cd F1-Race-Prediction
