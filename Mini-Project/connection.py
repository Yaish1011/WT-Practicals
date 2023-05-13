from turtle import pd
from flask import Flask, render_template, request
# import mysql.connector
import csv
import matplotlib.pyplot as plt
import time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Registration.html')
# @app.route('/show')
# def show():
#     # Connect to the database
#     cnx = mysql.connector.connect(user='root', password='root',
#                               host='localhost',
#                               database='mydatabase')
#     cursor = cnx.cursor()

#     # Fetch data from the database
#     cursor.execute("SELECT * FROM customers")
#     data = cursor.fetchall()

#     # Render the HTML template with the data
#     return render_template('home.html', data=data)

@app.route('/Submit', methods=['POST'])
def save_data():
    data1 = request.form['name']
    data2 = request.form['email']
    data3 = request.form['game']
    data4 = request.form['username']
    data5 = request.form['age']
    data6 = request.form['country']
   
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data1, data2, data3, data4, data5, data6])
    return 'Data saved successfully'




@app.route('/chart')
def index():
    with open('data.csv') as f:
        reader = csv.reader(f)
        countries = [row[-1] for row in reader]
    counts = {}
    for country in countries:
        if country in counts:
            counts[country] += 1
        else:
            counts[country] = 1
    labels = list(counts.keys())
    values = list(counts.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    plt.savefig('static/chart.png')

    # Render the HTML template
    chart_url = '/static/chart.png'
    return render_template('chart.html', chart_url=chart_url)
    # Render HTML template and pass image URL to it



@app.route('/faq')
def faq():
    return render_template('faq.html')
def chatbot_response(message):
    var_time = time.ctime()
    qna = {
        "Hi" : "Hello",
        "hi" : "Hello",
        "Hello" : "Hi",
        "hello" : "Hi",
        "Hey" : "wassup",
        "hey" : "wassup",
        "what is your name" : "My name is ChatBot",
        "What is your name" : "My name is ChatBot",
        "how are you" : "I'am Fine, what about you",
        "How are you" : "I'am Fine, what about you",
        "I am fine" : "Ok",
        "i am fine" : "Ok",
        "Fine" : "Ok",
        "fine" : "Ok",
        "what is the time now" : var_time,
        "Bye" : "See you later",
        "bye" : "See you later",
        "ok" : "See you later",
        "Ok" : "See you later",
    }
    

    




    return qna.get(message, "I'm sorry, I didn't understand that.")
@app.route('/faq', methods=['POST'])
def get_bot_response():
    user_message = request.form['message']
    bot_response = chatbot_response(user_message)
    return render_template('faq.html', message=user_message, response=bot_response)


@app.route('/data')
def data():
    # Read the CSV file and convert it to a list of dictionaries
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        games = [dict(zip(['name', 'email', 'game', 'username', 'age', 'country'], row)) for row in reader]

    # Render the HTML template with the games data
    return render_template('data.html', games=games)
        

 

if __name__ == '__main__':
    app.run(debug=False)
    