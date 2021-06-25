import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from PIL import Image
col1, col2= st.beta_columns(2)




image = Image.open('Logo.png')
st.sidebar.image(image, width=250)
st.sidebar.title('Di-Cision')
df=pd.read_excel("Di_Plast_Database.xlsx", index_col=None)  

list_process=df.Process.unique()
process=st.sidebar.selectbox("What is your Process?",list_process,help="Please choose a Process to continue")


problem_df = df[df['Process'] ==process ]

list_problem=sorted(problem_df.Problem.unique())

problem=st.sidebar.selectbox("What is your Problem?",list_problem,help="Please choose a Problem to continue")

cause_df=df[(df["Process"]==process) & (df["Problem"]==problem)]
for col in cause_df.columns:
    print(col)


list_cause=sorted(cause_df.Causerankfirstorder.unique())
cause=st.sidebar.selectbox("Possible Cause?",list_cause)


cause_df=df[(df["Process"]==process) & (df["Problem"]==problem)& (df["Causerankfirstorder"]==cause)]

list_cause_snd=sorted(cause_df.Causeranksecondorder.unique())
cause_snd=""
print(len(list_cause_snd))

if len(list_cause_snd)>1:
    cause_snd =st.sidebar.selectbox("Narrow down error?",list_cause_snd)

if cause_snd!="":
    result_df=df[(df["Process"]==process) & (df["Problem"]==problem)& (df["Causerankfirstorder"]==cause)& (df["Causeranksecondorder"]==cause_snd)]
else:
    result_df=cause_df

#st.write(result_df)
parameter=""
engineering_flag=""
with col1:
    st.title('Check Parameter:') 
    parameters=result_df['Valuetobemonitored'].tolist()
    for item in parameters:
        if st.button(item, key=item, help=None):
           parameter=item
           sensor_df=result_df[result_df["Valuetobemonitored"]==item]
           engineering_flag=sensor_df["additionalengineeringoradaptionadvised"].iloc[0]
    if engineering_flag !="" and engineering_flag=="yes":
        st.write("")
        st.write("")
        st.write("")
        st.markdown("__Additional engineering adaption advised!__")


with col2:
    st.title('Sensor:')
    if parameter!="":       
        st.write(sensor_df["SuitableSensoring"].iloc[0])
         
    st.title('Manufacturers:')

    if parameter!="":
        
        st.write(sensor_df["Manufacturerone"].iloc[0])
        st.write(sensor_df["Manufacturertwo"].iloc[0])
        st.write(sensor_df["Manufacturerthree"].iloc[0])

