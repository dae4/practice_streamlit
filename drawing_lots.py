import streamlit as st

import random


st.title("랜덤점심")

members= [str(x) for x in range(0,30)]

target = {}
st.sidebar.title("휴가자는 체크해제")

for member in members:
    target[member]=st.sidebar.checkbox(member,True)

for k,value in list(target.items()):
    if value==False:
        del target[k]

members = list(target.keys())

try :
    person=int(st.text_input("배정인원을 넣어주세요"))
    groups=len(members)//person ## 총 생성된 조
    even = len(members)%person  ## 마지막조 인원

    col1,col2 = st.columns(2)

    for i in range(groups):

        if i==groups-1 and len(members) > person-1 and even!=0:
            if person!=1:
                person-=1

        group=random.sample(members,person)
        
        for j in group:
            members.remove(j)
        

        group = " ".join(group)

        if i%2==0:
            with col1:
                st.header('{}조'.format(i+1))
                st.write('{}'.format(group))
        else:
            with col2:
                st.header('{}조'.format(i+1))
                st.write('{}'.format(group))
          
    if even!=0:
        with col2:
            members = " ".join(members)
            st.header('{}조'.format(groups+1))
            st.write('{}'.format(members))

except:
    None