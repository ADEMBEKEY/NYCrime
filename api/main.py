import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "lgbm.joblib")

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model from {MODEL_PATH}: {e}")
    model = None

class PredictionRequest(BaseModel):
    date: str
    hour: int
    latitude: float
    longitude: float
    place: str
    age: int
    race: str
    gender: str
    precinct: int
    borough: str

def create_df(date_str, hour, latitude, longitude, place, age, race, gender, precinct, borough):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        date = datetime.now()
        
    hour = int(hour) if int(hour) < 24 else 0
    day = date.day
    month = date.month
    year = date.year
    in_park = 1 if place == "In park" else 0
    in_public = 1 if place == "In public housing" else 0
    in_station = 1 if place == "In station" else 0
    boro = borough.upper()
    completed = 1
    ADDR_PCT_CD = float(precinct)
    age = int(age)

    columns = np.array(['year', 'month', 'day', 'hour', 'Latitude', 'Longitude','COMPLETED','ADDR_PCT_CD', 'IN_PARK', 'IN_PUBLIC_HOUSING',
                        'IN_STATION', 'BORO_NM_BRONX', 'BORO_NM_BROOKLYN', 'BORO_NM_MANHATTAN', 'BORO_NM_QUEENS',
                        'BORO_NM_STATEN ISLAND', 'BORO_NM_UNKNOWN', 'VIC_AGE_GROUP_18-24', 'VIC_AGE_GROUP_25-44',
                        'VIC_AGE_GROUP_45-64', 'VIC_AGE_GROUP_65+', 'VIC_AGE_GROUP_-18', 'VIC_AGE_GROUP_UNKNOWN',
                        'VIC_RACE_AMERICAN INDIAN/ALASKAN NATIVE', 'VIC_RACE_ASIAN / PACIFIC ISLANDER', 'VIC_RACE_BLACK',
                        'VIC_RACE_BLACK HISPANIC', 'VIC_RACE_OTHER', 'VIC_RACE_UNKNOWN', 'VIC_RACE_WHITE',
                        'VIC_RACE_WHITE HISPANIC', 'VIC_SEX_D', 'VIC_SEX_E', 'VIC_SEX_F', 'VIC_SEX_M', 'VIC_SEX_U'])

    data = [[year, month, day, hour, latitude, longitude,completed,ADDR_PCT_CD, in_park, in_public, in_station,
             1 if boro == "BRONX" else 0, 1 if boro == "BROOKLYN" else 0, 1 if boro == "MANHATTAN" else 0,
             1 if boro == "QUEENS" else 0, 1 if boro == "STATEN ISLAND" else 0, 1 if boro not in (
             "BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND") else 0,
             1 if age in range(18, 25) else 0, 1 if age in range(25, 45) else 0, 1 if age in range(45, 65) else 0,
             1 if age >= 65 else 0, 1 if age < 18 else 0, 0,
             1 if race == "AMERICAN INDIAN/ALASKAN NATIVE" else 0, 1 if race == "ASIAN / PACIFIC ISLANDER" else 0,
             1 if race == "BLACK" else 0, 1 if race == "BLACK HISPANIC" else 0, 1 if race == "OTHER" else 0,
             1 if race == "UNKNOWN" else 0, 1 if race == "WHITE" else 0, 1 if race == "WHITE HISPANIC" else 0,
             0, 0, 1 if gender == "Female" else 0, 1 if gender == "Male" else 0, 0]]

    df = pd.DataFrame(data, columns=columns)
    return df.values

@app.post("/api/predict")
async def predict_crime(req: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        data = create_df(req.date, req.hour, req.latitude, req.longitude, req.place, 
                         req.age, req.race, req.gender, req.precinct, req.borough)
        
        # Get class probabilities
        probs = model.predict_proba(data)[0]
        
        categories_map = {
            0: {
                "name": 'DRUGS/ALCOHOL',
                "subcategories": ['DANGEROUS DRUGS', 'INTOXICATED & IMPAIRED DRIVING', 'ALCOHOLIC BEVERAGE CONTROL LAW', 'INTOXICATED/IMPAIRED DRIVING', 'UNDER THE INFLUENCE OF DRUGS', 'LOITERING FOR DRUG PURPOSES']
            },
            1: {
                "name": 'PERSONAL',
                "subcategories": ['ASSAULT 3 & RELATED OFFENSES', 'FELONY ASSAULT', 'OFFENSES AGAINST THE PERSON', 'HOMICIDE-NEGLIGENT,UNCLASSIFIE', 'HOMICIDE-NEGLIGENT-VEHICLE', 'KIDNAPPING & RELATED OFFENSES', 'ENDAN WELFARE INCOMP', 'OFFENSES RELATED TO CHILDREN', 'CHILD ABANDONMENT/NON SUPPORT', 'KIDNAPPING', 'DANGEROUS WEAPONS', 'UNLAWFUL POSS. WEAP. ON SCHOOL']
            },
            2: {
                "name": 'PROPERTY',
                "subcategories": ['BURGLARY', 'PETIT LARCENY', 'GRAND LARCENY', 'ROBBERY', 'THEFT-FRAUD', 'GRAND LARCENY OF MOTOR VEHICLE', 'FORGERY', 'JOSTLING', 'ARSON', 'PETIT LARCENY OF MOTOR VEHICLE', 'OTHER OFFENSES RELATED TO THEF', "BURGLAR'S TOOLS", 'FRAUDS', 'POSSESSION OF STOLEN PROPERTY', 'CRIMINAL MISCHIEF & RELATED OF', 'OFFENSES INVOLVING FRAUD', 'FRAUDS', 'THEFT OF SERVICES']
            },
            3: {
                "name": 'SEXUAL',
                "subcategories": ['SEX CRIMES', 'HARRASSMENT 2', 'RAPE', 'PROSTITUTION & RELATED OFFENSES', 'FELONY SEX CRIMES', 'LOITERING/DEVIATE SEX']
            }
        }
        
        all_predictions = []
        for i, prob in enumerate(probs):
            cat_info = categories_map.get(i, {"name": "UNKNOWN", "subcategories": []})
            all_predictions.append({
                "id": i,
                "category": cat_info["name"],
                "subcategories": cat_info["subcategories"],
                "confidence": float(prob)
            })
            
        # Sort predictions by confidence (highest first)
        all_predictions.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "top_prediction": all_predictions[0],
            "all_predictions": all_predictions
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}

# Mount static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
