import streamlit as st
import pandas as pd

worker = ['user1']

workload = pd.DataFrame(columns=worker,data=None)
user = st.selectbox("worker",worker)
daily_work=st.number_input('Enter a number')
complete = st.button("Enter")


table = st.table(workload)

if complete:
    temp = pd.DataFrame(columns=[user],data=[daily_work])
    table.add_rows(temp)
    