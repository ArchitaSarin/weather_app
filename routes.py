from flask import render_template, request
from app import app
from app.weather import get_info, ai_assist, clean

@app.route('/', methods=['GET', 'POST'])
def index():

    # defining the variables
    weather = None
    current = None
    forecast = None
    ai = None
    clean_ai = None
    location = None
    
    # sending backend information to frontend to display to user
    if request.method == 'POST':
        location = request.form['location']
        weather = get_info(location)
        current = weather[0]
        forecast = weather[1]
        ai = ai_assist(forecast)
        clean_ai = clean(ai)
    
    return render_template('index.html', location=location, current=current, forecast=forecast, ai=clean_ai)

@app.route('/info')
def info():
    return render_template('info.html')