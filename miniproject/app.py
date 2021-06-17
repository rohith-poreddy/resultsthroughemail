# from types import MethodType
from flask import Flask,render_template,request
# ,redirect, url_for
from flask_mail import Mail
import csv,smtplib, ssl
import pandas as pd

app=Flask(__name__)
mail=Mail(app)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username=request.form["username"]
        password=request.form["password"]
        if  username!= 'admin' or password != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return render_template('home.html', error=error)  
        else:    
            return render_template('login.html',username=username)  

@app.route('/sendmail',methods=['GET', 'POST'])
def getcsv():
    if request.method == 'POST':
       message = """Subject: Your Marks Hi {name}, your marks  are {total}"""
       from_address = 'resultsthroughemail@gmail.com'
       password = '6305077750'
       context = ssl.create_default_context()
       with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
          server.login(from_address, password)
          datacsv=request.form['datacsv']
          with open(datacsv) as file:
              reader = csv.reader(file)
              next(reader)  # Skip header row
              for ID,NAME,BRANCH,SECTION,S1,S2,S3,S4,S5,TOTAL,STATUS,EMAIL in reader:
                   server.sendmail(from_address,EMAIL,message.format(name=NAME,total=TOTAL),)
       datacsv=request.form['datacsv']
       results=[]
       with open(datacsv) as file:
           csvfile=csv.reader(file)
           for row in csvfile:
               results.append(row)
       results=pd.DataFrame(results)
       return render_template('details.html',results=results.to_html(header=False,index=False))
     
@app.route('/logout',methods=['GET', 'POST'])
def logout():
    return render_template("home.html") 


if __name__=="__main__":
    app.run(debug=True)
