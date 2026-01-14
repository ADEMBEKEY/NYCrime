<h1 align="center">
  <br>
  New York City Crimes Detection using Machine Learning

</h1>

<div align="center">
  <h4>
    <a href="#overview">Overview</a> |
    <a href="#architecture">Architecture</a> |
    <a href="#dataset">Dataset</a> |
    <a href="#machine-learning-model">Machine Learning Model</a> |
    <a href="#installation">Installation</a> |
    <a href="#usage">Usage</a> |
    <a href="#notebooks">Notebooks</a> |
    <a href="#technologies">Technologies</a> |
    <a href="#user-interface">User Interface</a>
  </h4>
</div>

<br>

## Overview

Predicting crime probabilities is crucial for enhancing public safety measures. This machine learning-based web application leverages historical crime data in New York City to provide users with valuable insights into potential crime occurrences. By incorporating user-specific information, location, and time, the application assists individuals in making informed decisions and taking preventive actions. Whether planning a route, selecting a residential area, or simply staying aware of potential risks, this tool empowers users with a proactive approach to personal safety.

### Key Capabilities
- **Crime Type Prediction**: Predicts the most likely category of crime (Drugs/Alcohol, Personal, Property, Sexual)
- **Risk Assessment**: Provides confidence scores for all crime categories
- **Interactive Map**: Allows users to select locations by clicking on a map or typing an address
- **Personalized Analysis**: Considers victim demographics (age, gender, race) for more accurate predictions
- **Temporal Intelligence**: Factors in date and time for context-aware predictions
- **Location Intelligence**: Uses NYC borough and precinct data with shapefile integration

## Architecture

The project consists of three main components:

### 1. Streamlit Application (`application/`)
- **`main.py`**: Interactive web interface for crime prediction
  - Map-based location selection using Folium
  - Text-based address search using Nominatim geocoding API
  - Real-time user input collection (demographics, time, location)
  - Visualization of prediction results
  
- **`backend.py`**: Core prediction logic
  - Feature engineering and data preprocessing
  - Model loading and inference
  - Crime category mapping and result formatting

### 2. FastAPI REST API (`api/`)
- **`main.py`**: RESTful API for crime predictions
  - `/api/predict` endpoint for crime predictions with probability distributions
  - `/api/health` endpoint for service monitoring
  - CORS-enabled for frontend integration
  - Serves static frontend files

### 3. Frontend (`frontend/`)
- **Modern Web Dashboard**: Premium UI for crime analysis
  - `index.html`: Responsive dashboard layout
  - `script.js`: Interactive map, form handling, and API integration
  - `style.css`: Modern styling with animated backgrounds
  - Features Leaflet maps for location selection
  - Real-time risk breakdown visualization

## Dataset

This work relies on the [NYPD Complaint Data Historic Dataset](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i). This dataset includes all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department (NYPD) from 2006 to 2021.

**Dataset Statistics:**
- **Records**: 6,901,167 complaints
- **Columns**: 35 features
- **Time Period**: 2006-2021
- **Coverage**: All NYC boroughs (Manhattan, Brooklyn, Queens, Bronx, Staten Island)

**Key Features Used:**
- Temporal: Year, month, day, hour
- Spatial: Latitude, longitude, borough, precinct
- Victim Demographics: Age group, race, gender
- Location Type: Parks, public housing, stations
- Crime Completion Status

## Machine Learning Model

The application uses a **LightGBM (Light Gradient Boosting Machine)** classifier for multi-class crime category prediction.

### Crime Categories
The model classifies crimes into 4 main categories:

1. **DRUGS/ALCOHOL** (Class 0)
   - Dangerous drugs, intoxicated driving, DUI
   - Alcoholic beverage control law violations
   - Loitering for drug purposes

2. **PERSONAL** (Class 1)
   - Assault and felony assault
   - Homicide and kidnapping
   - Child endangerment and abandonment
   - Dangerous weapons possession

3. **PROPERTY** (Class 2)
   - Burglary, robbery, larceny (grand and petit)
   - Motor vehicle theft
   - Forgery and fraud
   - Arson and criminal mischief

4. **SEXUAL** (Class 3)
   - Sex crimes and rape
   - Harassment
   - Prostitution-related offenses

### Model Features (35 input features)
- **Temporal**: `year`, `month`, `day`, `hour`
- **Spatial**: `Latitude`, `Longitude`, `ADDR_PCT_CD` (precinct)
- **Status**: `COMPLETED` (crime completion indicator)
- **Location Type**: `IN_PARK`, `IN_PUBLIC_HOUSING`, `IN_STATION`
- **Borough**: One-hot encoded (Bronx, Brooklyn, Manhattan, Queens, Staten Island, Unknown)
- **Victim Age Groups**: One-hot encoded (<18, 18-24, 25-44, 45-64, 65+, Unknown)
- **Victim Race**: One-hot encoded (7 categories including White, Black, Hispanic variants, Asian/Pacific Islander, etc.)
- **Victim Sex**: One-hot encoded (D, E, F, M, U)

### Model Performance
The repository includes performance visualizations in the `images/` directory:
- Confusion matrices for LightGBM, XGBoost, and CatBoost
- ROC curves showing multi-class classification performance
- Feature importance analysis

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/ADEMBEKEY/NYCrime.git
cd NYCrime
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download required data files**

The following files are required but not included in the repository (due to size):
- Trained model: `models/lgbm.joblib`
- NYC precinct shapefile: `application/geo_export_84578745-538d-401a-9cb5-34022c705879.shp` (and associated .shx, .dbf, .prj files)
- NYC borough shapefile: `application/borough/nybb.shp` (and associated files)

Note: These files are excluded via `.gitignore` due to their size. You'll need to train the model using the provided notebooks or obtain pre-trained models separately.


## Notebooks

The repository includes Jupyter notebooks for data analysis and model development:

### 1. Data Cleaning & Exploratory Data Analysis
- **File**: `notebooks/ny-crimes-data-cleaning-eda.ipynb`
- **Contents**: 
  - Data loading and initial exploration
  - Missing value analysis and handling
  - Outlier detection
  - Feature distribution analysis
  - Temporal and spatial patterns visualization
  - Crime category distribution analysis

### 2. Data Preparation & Modeling
- **File**: `notebooks/data-preparation-modeling.ipynb`
- **Contents**:
  - Feature engineering
  - One-hot encoding for categorical variables
  - Train-test split
  - Model training (LightGBM, XGBoost, CatBoost)
  - Model evaluation and comparison
  - Hyperparameter tuning
  - Feature importance analysis
  - Model serialization

## Technologies

### Web Application Framework
- **Streamlit**: Interactive web application framework
- **FastAPI**: Modern, high-performance web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI

### Geospatial Libraries
- **Folium**: Interactive map visualization
- **streamlit-folium**: Streamlit component for Folium maps
- **geopy**: Geocoding and location services (Nominatim)
- **geopandas**: Geographic data manipulation
- **shapely**: Geometric operations
- **pyproj**: Cartographic projections and coordinate transformations

### Data Science & Machine Learning
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms and utilities
- **LightGBM**: Gradient boosting framework (primary model)
- **XGBoost**: Gradient boosting library
- **CatBoost**: Gradient boosting library

### Visualization
- **seaborn**: Statistical data visualization
- **matplotlib**: Plotting library
- **scikit-plot**: Visualization for machine learning metrics

### Additional Libraries
- **joblib**: Model serialization
- **requests**: HTTP library for API calls

### Installation
To install all required dependencies:
```sh
pip install -r requirements.txt
```

## User Interface

The application provides three different interfaces:

### 1. Streamlit Interface

Interactive web application with:
- Sidebar form for user input
- Dual input methods (map selection or address search)
- Real-time prediction display
- Crime category and subcategory information

### 2. Modern Web Dashboard
![Web Dashboard](Capture%20d%27écran%202026-01-12%20013010.png)

Premium dashboard featuring:
- Animated background with gradient blobs
- Interactive Leaflet map
- Comprehensive form for all parameters
- Risk breakdown with confidence scores
- Responsive design with modern aesthetics

### Key UI Components

**Input Forms:**
- Date and time selection
- Borough dropdown (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- Precinct ID input
- Place type selection (Public Housing, Park, Station)
- Victim demographics (Age, Gender, Race)

**Output Display:**
- Primary crime category prediction
- Confidence score with visual progress bar
- List of related crime subcategories
- Risk breakdown for all crime categories

## Project Structure

```
NYCrime/
├── api/
│   └── main.py                 # FastAPI REST API
├── application/
│   ├── main.py                 # Streamlit application
│   ├── backend.py              # Prediction logic
│   ├── geo_export_*.shp        # NYC precinct shapefiles (excluded)
│   └── borough/
│       └── nybb.shp            # NYC borough shapefiles (excluded)
├── frontend/
│   ├── index.html              # Modern web dashboard
│   ├── script.js               # Frontend JavaScript
│   └── style.css               # Styling
├── images/                     # Model performance visualizations
├── models/
│   └── lgbm.joblib             # Trained LightGBM model (excluded)
├── notebooks/
│   ├── ny-crimes-data-cleaning-eda.ipynb
│   └── data-preparation-modeling.ipynb
├── test_model.py               # Model testing script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## How It Works

### Prediction Pipeline

1. **User Input Collection**
   - Location: Either map click or address text input
   - Temporal: Date and hour
   - Demographics: Age, gender, race
   - Context: Place type (park, housing, station)

2. **Geocoding & Spatial Processing**
   - Convert address to coordinates using Nominatim API
   - Transform coordinates to UTM projection (EPSG:2263)
   - Match coordinates to NYC precinct using shapefile intersection
   - Match coordinates to borough using shapefile intersection

3. **Feature Engineering**
   - Extract temporal features (year, month, day, hour)
   - One-hot encode categorical variables:
     - Borough (6 categories)
     - Age groups (7 categories)
     - Race (8 categories)
     - Gender (5 categories)
   - Binary encode location types (park, public housing, station)
   - Combine all features into 35-dimensional input vector

4. **Model Prediction**
   - Load pre-trained LightGBM model
   - Pass feature vector through model
   - Get probability distribution across 4 crime categories
   - Identify highest probability category

5. **Result Presentation**
   - Display primary crime category
   - Show confidence score
   - List related crime subcategories
   - Visualize on map (Streamlit version)
   - Show risk breakdown (Web dashboard)

## Model Training Process

1. **Data Collection**: NYPD historical crime data (2006-2021)
2. **Data Cleaning**: Handle missing values, outliers, invalid entries
3. **Feature Engineering**: Create derived features and encode categoricals
4. **Data Splitting**: Train-test split with temporal consideration
5. **Model Training**: Train multiple gradient boosting models
6. **Model Selection**: Compare LightGBM, XGBoost, CatBoost performance
7. **Hyperparameter Tuning**: Optimize selected model
8. **Model Evaluation**: Assess using confusion matrix, ROC curves, F1-scores
9. **Model Serialization**: Save best model as `lgbm.joblib`

