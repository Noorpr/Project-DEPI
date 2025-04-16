from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


async def lifespan(app: FastAPI):
    app.state.model = joblib.load("random_forest.pkl")
    print("Model Loaded")
    yield

app = FastAPI(lifespan = lifespan)


class InputData(BaseModel):
    features : list[float]



@app.post("/predict")
def get_result(data : InputData):
    model = app.state.model
    prediction = model.predict([data.features])
    return {"prediction": prediction[0]}