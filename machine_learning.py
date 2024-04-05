#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error


# In[13]:


sensor_data = pd.read_csv('D:\da iot practicals\CO(ppm).csv')


# In[14]:


train_size = int(len(sensor_data) * 0.8)
train_data, test_data = sensor_data[:train_size], sensor_data[train_size:]


# In[15]:


model = ARIMA(train_data['CO'], order=(5,1,0))
model_fit = model.fit()


# In[16]:


predictions = model_fit.forecast(steps=len(test_data))


# In[17]:


if not predictions.empty:
    if not test_data.empty:
        last_observed_value = test_data['CO'].iloc[-1]
        predicted_value = predictions.iloc[-1]

        if predicted_value > last_observed_value:
            print("There is a possibility of increase in CO")
        else:
            print("No significant increase in CO predicted")
    else:
        print("No testing data available. Unable to make predictions.")
else:
    print("No predictions available. Unable to make predictions.")


# In[ ]:
