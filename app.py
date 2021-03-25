from flask import Flask,request,render_template
import pandas as pd 
import numpy as np 
import pickle
import os

webapp_root = "webapp"
template_dir = os.path.join(webapp_root,"templates")

app = Flask(__name__,template_folder=template_dir)
model= pickle.load(open("car_prediction_model.pkl","rb"))
@app.route("/",methods=["GET","POST"])
def Home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    Fuel_Type_Diesel = 0
    if request.form:
        print(request.form)
        year = int(request.form["Year"])
        present_price = float(request.form["Present_Price"])
        Kms_Driven = int(request.form["Kms_Driven"])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form["Owner"])
        Fuel_Type_Petrol = request.form["Fuel_Type_Petrol"]
        if (Fuel_Type_Petrol == "Petrol"):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Petrol == "Diesel"):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Year = 2021-year    
        Seller_Type_Individual = request.form["Seller_Type_Individual"]
        if(Seller_Type_Individual == "Individual"):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form["Transmission_Mannual"]
        if(Transmission_Mannual == "Mannual"):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
           
        
        input_df = pd.DataFrame([[present_price,Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Transmission_Mannual]])
        input_df.columns=['Present_Price', 'Kms_Driven', 'Owner', 'no_years',
       'Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Transmission_Manual']
        
        prediction=model.predict(input_df)
        output = np.round(prediction[0],2)
        if(output <0):
            print("Sorry !! You cannot sell your car!!")
            return render_template("index.html",prediction_texts = "Sorry!! You cannot sell your car")
        else:
            print("You can sell your car at {}".format(output))
            return render_template("index.html", prediction_text = "You can sell your car at {}".format(output))
        
    else:
        return render_template("index.html")

if __name__=="__main__":
	app.run(host="127.0.0.1",debug=True)