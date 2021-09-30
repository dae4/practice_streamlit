import streamlit as st
import pandas as pd
import os

worker = ['user1']

if os.path.isfile('test_csv_file.csv'):
    workload = pd.read_csv('test_csv_file.csv')
else:
    workload = pd.DataFrame(columns=worker,data=None)

user = st.selectbox("worker",worker)
daily_work=st.number_input('Enter a number')
complete = st.button("Enter")


if complete:
    insert_data = {user:[daily_work]}
    df_to_insert = pd.DataFrame(data=insert_data)
    workload = workload.append(df_to_insert, ignore_index=True)
    table = st.table(workload)
    workload.to_csv('test_csv_file.csv')