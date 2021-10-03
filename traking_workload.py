import streamlit as st
import pandas as pd
import os

worker = []

user=st.text_input('Add user')

worker.append(user)

if os.path.isfile('test_csv_file.csv'):
    workload = pd.read_csv('test_csv_file.csv')
else:
    workload = pd.DataFrame(columns=worker,data=None)

user = st.selectbox("worker",worker)
daily_work=st.number_input('Enter a number')
complete = st.button("Enter")

workload=workload.append({user: daily_work}, ignore_index=True)

if complete:
    table = st.table(workload)
    workload.to_csv('test_csv_file.csv')