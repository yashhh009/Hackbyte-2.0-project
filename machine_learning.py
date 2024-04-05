import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def train_arima_model(data):
    train_size = int(len(data) * 0.8)
    train_data, test_data = data[:train_size], data[train_size:]
    model = ARIMA(train_data['CO'], order=(5,1,0))
    model_fit = model.fit()
    return model_fit

def make_predictions(model, test_data):
    predictions = model.forecast(steps=len(test_data))
    return predictions

def predict_increase(data_file_path):
    sensor_data = pd.read_csv(data_file_path)
    model = train_arima_model(sensor_data)
    test_data = sensor_data[train_size:]
    predictions = make_predictions(model, test_data)
    
    if not predictions.empty:
        if not test_data.empty:
            last_observed_value = test_data['CO'].iloc[-1]
            predicted_value = predictions.iloc[-1]

            if predicted_value > last_observed_value:
                return "There is a possibility of increase in CO"
            else:
                return "No significant increase in CO predicted"
        else:
            return "No testing data available. Unable to make predictions."
    else:
        return "No predictions available. Unable to make predictions."
