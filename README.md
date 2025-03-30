# Model packager designed for MLflow
Downloads model artifacts from MLflow and prepares a container images with artifacts and the python packages installed

# Images
Images can be found [hub.docker.com](https://hub.docker.com/r/frenoid/model-packager/tags)

# Run a local Ray Serve deployment

### Start a local Ray Cluster
```bash
ray start --head --port=6379
```

### Deploy the RayServe app
```bash
serve deploy serve_config.yaml
```

### Stop the Ray Cluster
```bash
ray stop
```