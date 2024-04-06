import os
from flask import Flask, render_template, request
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def train_arima_model(data):
    train_size = int(len(data) * 0.8)
    train_data, test_data = data[:train_size], data[train_size:]
    model = ARIMA(train_data['CO'], order=(5,1,0))
    model_fit = model.fit()
    return model_fit, train_size

def make_predictions(model, test_data):
    predictions = model.forecast(steps=len(test_data))
    return predictions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'data_file' not in request.files:
        return "No file part"
    
    uploaded_file = request.files['data_file']
    
    if uploaded_file.filename == '':
        return "No selected file"
    
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)
        
        sensor_data = pd.read_csv(file_path)
        model, train_size = train_arima_model(sensor_data)
        test_data = sensor_data[train_size:]
        predictions = make_predictions(model, test_data)
        
        if not predictions.empty and not test_data.empty:
            last_observed_value = test_data['CO'].iloc[-1]
            predicted_value = predictions.iloc[-1]

            if predicted_value > last_observed_value:
                prediction_result = "There is a possibility of increase in CO"
            else:
                prediction_result = "No significant increase in CO predicted"
        else:
            prediction_result = "Unable to make predictions."

        os.remove(file_path)  
        
        return render_template('result.html', prediction_result=prediction_result)
    else:
        return "Invalid file format or file not allowed"

if __name__ == '__main__':
    app.run(debug=True)
