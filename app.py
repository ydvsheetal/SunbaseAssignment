import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics
from flask import Flask, request, render_template
import pickle

app = Flask("__name__")

df_1=pd.read_csv("Churn_data_dummy.csv")
q = ""

@app.route("/")
def loadPage():
	return render_template('home.html', query="")


@app.route("/", methods=['POST'])
def predict():
    inputQuery1 = request.form['query1']
    inputQuery2 = request.form['query2']
    inputQuery3 = request.form['query3']
    inputQuery4 = request.form['query4']
    inputQuery5 = request.form['query5']
    inputQuery6 = request.form['query6']

    model = pickle.load(open("model.sav", "rb"))
    
    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6]]
    
    new_df = pd.DataFrame(data, columns = ['Age','Gender','Location','Subscription_Length_Months',
                                           'Monthly_Bill','Total_Usage_GB'])
    df_2 = pd.concat([df_1, new_df], ignore_index = True) 
    
    df_2['Age'] = pd.to_numeric(df_2['Age'],errors='coerce')
    df_2['Subscription_Length_Months'] = pd.to_numeric(df_2['Subscription_Length_Months'],errors='coerce')
    df_2['Monthly_Bill'] = pd.to_numeric(df_2['Monthly_Bill'],errors='coerce')
    df_2['Total_Usage_GB'] = pd.to_numeric(df_2['Total_Usage_GB'],errors='coerce')
    
    
    
    new_df__dummies = pd.get_dummies(df_2)
   # final_df=pd.concat([new_df__dummies, new_dummy], axis=1)
    #new_df__dummies=new_df__dummies.drop('Unnamed: 0',axis=1)
    
    single = model.predict(new_df__dummies.tail(1))
    probablity = model.predict_proba(new_df__dummies.tail(1))[:,1]
    
    if single==1:
        o1 = "This customer is likely to be churned!!"
        o2 = "Confidence: {}".format(probablity*100)
    else:
        o1 = "This customer is likely to continue!!"
        o2 = "Confidence: {}".format(probablity*100)
        
    return render_template('home.html', output1=o1, output2=o2, 
                           query1 = request.form['query1'], 
                           query2 = request.form['query2'],
                           query3 = request.form['query3'],
                           query4 = request.form['query4'],
                           query5 = request.form['query5'], 
                           query6 = request.form['query6'])
    
app.run()