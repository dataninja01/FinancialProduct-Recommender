# ML Financial Advisor: Transforming Credit Invisible to Invincible (Capstone Project)

### Design & Feature Selection:
```
Education - FourthBrain MLOps Class November 21 cohort
Data Source - Consumer CFPB inquiries and complaints DB, Reddit Finance Posts, Debt inquires, publically available hacked data from breaches 
Programming and Pre-processing - Python, Flask, Pandas, Numpy, spaCy, Jypter Notebook
ML- Scikit Learn, XGBoost
```

### Integration & Implementation:
```
Backend Relational DB - MySQL and CloudSQL for user info and store look up table
Dockerize & GCP container registry
GCP Deployment/Hosting/Endpoints
Kubeflow to manage distributed env 
```
### Operations and Monitoring
```
Monitoring and Visualization - Prometheus and Grafana, Pusher? []
Kubernetes for Distributed Computing
Kubeflow to manage distributed env 
AI Ethics - We do not calculate personal data in our recommendation engine to guard against bias
```
### Front-end: [Sarah]
```
-1st page that accepts user input and POSTs info to SQLite database 
-GETs output of ML and provides recommendations (min 3) to user
-Unit testing of code with [Ponicode](https://www.ponicode.com) AI tool and [standards](https://madewithml.com/courses/mlops/testing/) 
```

### ML pipeline in storage bucket for recommendation engine [Mani]
```
-Machine learning algorithms take numbers as inputs. This means that we will need to convert the texts into numerical vectors. There are two steps to creating the Document-Term Matrix:
Tokenization - with NLTK library (remove the punctuations, stopwords and normalize the corpus) basically divide texts into words or smaller sub-texts.
Vectorization - Tfidf vectorization increases proportionally to the number of times a word appears in the document and is offset by the number of documents in the corpus that contain the word…in other words penalizes very frequently occurring words that provide less contextual meaning.
-topic tracking lightweight NLP model & continuous training
- Competitive classification models were explored 
Multiclass Logistic Regression
XGBoost
Linear Support Vector Classifier  
The Metrics for model evaluation -ROC_AUC, test accuracy, model run time, precision, recall for the 7 categories: credit card, digital card, credit repair, debt settlement, rewards credit card, secured credit card
-MLflow for model versioning
```   

### Monitoring [Daisy]
```
-Containerization and registry
-GCP Metrics for VM instance resource management displayed on Prometheus & Grafana 
-Web traffic monitoring
```

### Final Presentation: [Modsquad Team]
```
Credit Invincible Capstone Project PPT and Demo

```

