from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np

# Create FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input data model
class ProjectInput(BaseModel):
    project_type: str
    # Add other features your model expects
    # For example:
    budget: float
    duration: int
    # Add all other features your model needs

# Load the saved model and encoder
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    print("Model and encoder loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.get("/")
def read_root():
    return {"message": "Win Prediction API is running"}

@app.post("/predict")
def predict_win(data: ProjectInput):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # One-hot encode project type
        type_encoded = encoder.transform(input_df[['project_type']])
        type_cols = encoder.get_feature_names_out(['project_type'])
        type_df = pd.DataFrame(type_encoded, columns=type_cols)
        
        # Combine features (adjust according to your model's requirements)
        X = pd.concat([input_df.drop(['project_type'], axis=1), type_df], axis=1)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]
        
        return {
            "prediction": bool(prediction),
            "win_probability": float(probability),
            "message": "Win" if prediction == 1 else "Loss"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
