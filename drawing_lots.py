import streamlit as st

import random


st.title("랜덤점심")

members= [str(x) for x in range(0,5,1)]

empty = st.empty()
target = {}
st.sidebar.title("휴가자는 체크해제")
col1, col2 = st.beta_columns(2)

for meber in members:
    target[meber]=st.sidebar.checkbox(meber,True)
temp=[]
for i in target:
    if target[i]==False:
        temp.append(target[i])

mebers = temp
try :
    person=int(st.text_input("배정인원을 넣어주세요"))

    groups=len(members)//person
    even = len(members)%person
    if even==0:
        st.write("총 {}조".format(groups))
        for i in range(groups):
            st.write('{}조'.format(i+1))
            group=random.sample(members,person)
            for j in group:
                members.remove(j)
            st.write(group)

    else:
        st.write("총 {}조".format(groups+1))
        for i in range(groups):
            st.write('{}조'.format(i+1))
            group=random.sample(members,person)
            for j in group:
                members.remove(j)
            st.write(group)
        st.write('{}조'.format(groups+1))    
        st.write(members)
except:
    None