import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


health_data = pd.read_csv('apple_health_data_clean.csv')
health_data['creationDate'] = pd.to_datetime(health_data['creationDate'])
health_data['startDate'] = pd.to_datetime(health_data['startDate'])
health_data['endDate'] = pd.to_datetime(health_data['endDate'])

# Filter for relevant metrics
metrics = ['VO2Max', 'HeartRateVariabilitySDNN', 'RestingHeartRate', 'HeartRate']
health_metrics = health_data[health_data['type'].isin(metrics)]
health_data_daily = health_metrics.groupby(['type', pd.Grouper(key='startDate', freq='D')])['value'].sum().unstack(level=0).reset_index()
correlation_matrix = health_data_daily[metrics].corr()

# Extract relevant correlations
vo2max_correlations = correlation_matrix['VO2Max']
hrv_correlations = correlation_matrix['HeartRateVariabilitySDNN']
resting_heart_rate_correlations = correlation_matrix['RestingHeartRate']
heart_rate_correlations = correlation_matrix['HeartRate']

# Create a dashboard
st.title('Health Metrics Dashboard')

# Scatter plot of VO2Max and HRV
st.header('VO2Max and HRV Relationship')
plt.scatter(health_data_daily['VO2Max'], health_data_daily['HeartRateVariabilitySDNN'])
plt.xlabel('VO2Max')
plt.ylabel('HRV')
st.pyplot()

# Correlation table
st.header('Correlations between Health Metrics')
st.write(correlation_matrix)

# Correlation bar charts
st.subheader('VO2Max Correlations')
plt.figure(figsize=(12, 6))
vo2max_correlations.abs().sort_values(ascending=False)[1:].plot(kind='bar')
st.pyplot()

st.subheader('HRV Correlations')
plt.figure(figsize=(12, 6))
hrv_correlations.abs().sort_values(ascending=False)[1:].plot(kind='bar')
st.pyplot()

st.subheader('Resting Heart Rate Correlations')
plt.figure(figsize=(12, 6))
resting_heart_rate_correlations.abs().sort_values(ascending=False)[1:].plot(kind='bar')
st.pyplot()

st.subheader('Heart Rate Correlations')
plt.figure(figsize=(12, 6))
heart_rate_correlations.abs().sort_values(ascending=False)[1:].plot(kind='bar')
st.pyplot()