from ray import serve
from ray.serve.handle import DeploymentHandle
from starlette.requests import Request
import mlflow
import xgboost as xgb
import pandas as pd
import numpy as np

MODEL_URI = "mlflow-artifacts:/1/57b3cc2aa1b743ecbf998c59bd575d8c/artifacts/model"

@serve.deployment(
    ray_actor_options={"num_cpus": 1.0, "num_gpus": 0},
    autoscaling_config={
        "target_num_ongoing_requests_per_replica": 4,
        "min_replicas": 1,
        "initial_replicas": 1,
        "max_replicas": 5
    },
)
class PredictApplesDemand:
    def __init__(self):
        print(f"Load mlflow model {MODEL_URI}")
        self.model = mlflow.xgboost.load_model(MODEL_URI)
        
        print("PredictApplesDemand is ready to serve")
    
    def predict(self, input_df) -> float:
        print(input_df)
        batch_dmatrix = xgb.DMatrix(input_df)

        inference = self.model.predict(batch_dmatrix)
        
        print(float(inference[0]))

        # Make a copy of the original dataframe
        #infer_df = df.copy()

        # Add the perdictions as a new column to the dataframe
        #infer_df["predicted_demand"] = inference
    
        return float(inference[0])

    async def __call__(self, request: Request) -> list[str]:
        average_temperature = float((await request.json())["average_temperature"])
        rainfall = float((await request.json())["rainfall"])
        weekend = int((await request.json())["weekend"])
        holiday = int((await request.json())["holiday"])
        price_per_kg = float((await request.json())["price_per_kg"])
        promo = int((await request.json())["promo"])
        previous_days_demand = float((await request.json())["previous_days_demand"])
        competitor_price_per_kg = float((await request.json())["competitor_price_per_kg"])
        marketing_intensity = float((await request.json())["marketing_intensity"])
        print(f"PredictApplesDemand called")
        
        d = {"average_temperature": [average_temperature],
              "rainfall": [rainfall],
              "weekend": [weekend],
              "holiday": [holiday],
              "price_per_kg": [price_per_kg],
              "promo": [promo],
              "previous_days_demand": [previous_days_demand],
              "competitor_price_per_kg": [competitor_price_per_kg],
              "marketing_intensity": [marketing_intensity],
             }
        print(f"Predict demand with: {d}")
        df = pd.DataFrame(data=d)
        predicted_demand = self.predict(df)
        
        return predicted_demand
    
app = PredictApplesDemand.bind()