# Capstone-Project
> "You cannot escape the responsibility of tomorrow by evading it today." -Abraham Lincoln

### ML Landscape:
```
ML- Scikit Learn, XGBoost
Data Source - Consumer CFPB inquires and complaints DB, Reddit Finance Posts, Debt inquires
Programming and Pre-processing - Python, Flask, Pandas, Numpy, spaCy, Jypter Notebook
Model Versioning - MLFlow
Backend Relational DB - MySQL and CloudSQL
Monitoring and Visualization - Prometheus and Grafana
Kubernetes for Distributed Computing
AI Ethics - We do not calculate personal data in our recommendation engine to guard against bias
Education - FourthBrain AI MLOps Class
GCP Deployment/Hosting/Endpoints
Kubeflow to manage distributed env 
Dockerize & GCP container registry
```
### Flask app QA, front-end and container: [Sarah]
```
-1st page that accepts user input and POSTs info to SQLite database 
-2nd page that GETs output of ML and provides recommendations (min 2) to user
-Unit testing of code with [Ponicode](https://www.ponicode.com) AI tool and [standards](https://madewithml.com/courses/mlops/testing/) 
-Containerization and registry
```

### Backend DBs trigger events to synchronize workflow events [Modsquad Team]
```
-1st user info
-2nd store look up table 
-store the output for continious training
```

### ML pipeline in storage bucket for recommendation engine [Mani]
```
-topic tracking lightweight NLP model & continuous training
-MLflow for model versioning
```   

### Monitoring [Daisy]
```
GCP Metrics for VM instance resource management displayed on Prometheus & Grafana 
Continious experimenting protocol - how to guard against data drift?
```

### Final Presentation: [Modsquad Team/Sarah]
```
Plug into PPT a mapping of [MLOps Stack Template](https://ml-ops.org/content/state-of-mlops) to our Credit Invincible Capstone Project
```

