from django.shortcuts import render
import pandas as pd
import joblib

# Home page
def home(request):
    return render(request, "home.html")


# Predict page
def predict(request):
    # Fetch data from the frontend
    mr_delay = int(request.POST["MR Delay"])
    gender = int(request.POST["M/F"])
    age = int(request.POST["Age"])
    educ = int(request.POST["EDUC"])
    ses = float(request.POST["SES"])
    mmse = float(request.POST["MMSE"])
    etiv = int(request.POST["eTIV"])
    nwbv = float(request.POST["nWBV"])

    # Store data in a dictionary
    data = {
    "MR Delay" : mr_delay,
    "M/F" : gender,
    "Age" : age,
    "EDUC" : educ,
    "SES" : ses,
    "MMSE" : mmse,
    "eTIV" : etiv,
    "nWBV" : nwbv}

    # Features for scaling
    numerical_scale = ['MR Delay','Age','EDUC','SES','MMSE','eTIV','nWBV']

    # Import tools for preprocessing
    scaler = joblib.load("tools/scaler_joblib")

    # Import model
    model = joblib.load("tools/model_joblib")    

    # Function to predict dementia
    def predict_dementia(data):
        test = pd.DataFrame([data])
        test[numerical_scale] = scaler.transform(test[numerical_scale])

        return model.predict(test)[0]

    # Getting prediction 
    prediction = predict_dementia(data)

    context = {
        "prediction" : prediction}
    return render(request, "home.html", context=context)