FROM docker.io/python:3.11.11-bookworm

ARG MLFLOW_TRACKING_URI=http://mlflow.mlnow.frenoid.com:30080/
ARG MLFLOW_TRACKING_USERNAME=mlflow
ARG MLFLOW_TRACKING_PASSWORD=mlflow
ARG MODEL_PATH="mlflow-artifacts:/1/57b3cc2aa1b743ecbf998c59bd575d8c/artifacts/model"

WORKDIR /app

COPY . .

# Install mlflow for downloading artifacts
RUN pip3 install -r requirements.txt

# Download model artifacts from mlflow
RUN python3 mlflow-packager.py

# Install the model requirements
RUN pip3 install -r /app/model/requirements.txt