import os

# Update the model loading paths
MODEL_PATH = os.path.join('models', 'model.pkl')
ENCODER_PATH = os.path.join('models', 'encoder.pkl') 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add your Vercel deployment URL here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your API routes...