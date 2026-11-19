
import sys
import flask
import sklearn
import pandas
import joblib

print("SupportPilot Environment Check")
print("--------------------------------")

print("Python Version:", sys.version)
print("Python Location:", sys.executable)

print("Flask:", flask.__version__)
print("Scikit-learn:", sklearn.__version__)
print("Pandas:", pandas.__version__)
print("Joblib:", joblib.__version__)

print("--------------------------------")
print("Environment configured successfully!")
