Formula 1 Race Position Prediction

OVERVIEW
This project predicts Formula 1 drivers’ race finishing positions using historical race data and machine learning techniques.  
It involves extensive Exploratory Data Analysis (EDA), feature engineering, and model building with **XGBoost** and **scikit-learn**.  
The dataset is compiled from multiple CSV files containing information on circuits, drivers, constructors, races, and results.

---

PROJECT STRUCTURE
├── data/ # All dataset files
│ ├── circuits.csv
│ ├── constructors.csv
│ ├── drivers.csv
│ ├── results.csv
│ ├── lap_times.csv
│ ├── qualifying.csv
│ ├── pit_stops.csv
│ ├── ...
│
├── F1_EDA.ipynb # Data cleaning, preprocessing, visualizations
├── F1_model.ipynb # Feature engineering, model training & evaluation
├── README.md # Project documentation
 
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
