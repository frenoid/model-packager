import os
import mlflow


if __name__ == "__main__": 
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

    print(f"Preparing to package model from uri")

    mlflow.artifacts.download_artifacts(artifact_uri=os.environ["MODEL_PATH"], dst_path="/app")