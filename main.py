

import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.

import numpy as np
import pandas as pd
from PIL import Image
import os
import base64
st.set_page_config(page_title="Di-Plast Sensor Selection ",layout="wide", page_icon = "favicon.png",)
#for image rendering with link, magic from https://discuss.streamlit.io/t/href-on-image/9693/4
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url,width="1"):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img style="width: {width}%" src="data:image/{img_format};base64,{bin_str} " />
        </a>'''
    return html_code
#-------------------------------------------------------------------------------------------------------





col1, col2= st.columns(2)




#image = Image.open('Logo.png')
Logo_html = get_img_with_href('Logo.PNG', 'https://www.nweurope.eu/projects/project-search/di-plast-digital-circular-economy-for-the-plastics-industry/',width="100")
st.sidebar.markdown(Logo_html, unsafe_allow_html=True)

#st.sidebar.image(image, width=250)
st.sidebar.title('Di-Plast Sensor Selection')
df=pd.read_excel("Di_Plast_Database.xlsx", index_col=None,engine='openpyxl') 

list_process=df.Process.unique()
process=st.sidebar.selectbox("What is your production process?",list_process,help="Please select your production process!​")


problem_df = df[df['Process'] ==process ]

list_problem=sorted(problem_df.Problem.unique())

problem=st.sidebar.selectbox("What is your process problem?​",list_problem,help="Please select your production problem!​")


cause_df=df[(df["Process"]==process) & (df["Problem"]==problem)]
for col in cause_df.columns:
    print(col)


list_cause=sorted(cause_df.Causerankfirstorder.unique())
cause=st.sidebar.selectbox("What could be the cause for the problem?​",list_cause,help="Please select what is causing the problem in your opinion!​")


cause_df=df[(df["Process"]==process) & (df["Problem"]==problem)& (df["Causerankfirstorder"]==cause)]

list_cause_snd=sorted(cause_df.Causeranksecondorder.unique())
cause_snd=""
print(len(list_cause_snd))

if len(list_cause_snd)>1:
    cause_snd =st.sidebar.selectbox("Please specify the cause!",list_cause_snd,help="Please specify the cause according to your experience!")

if cause_snd!="":
    result_df=df[(df["Process"]==process) & (df["Problem"]==problem)& (df["Causerankfirstorder"]==cause)& (df["Causeranksecondorder"]==cause_snd)]
else:
    result_df=cause_df

st.sidebar.write("")
st.sidebar.write("")




SKZ_Logo_html = get_img_with_href('SKZ-Logo.png', 'https://www.skz.de',width="100")
st.sidebar.markdown(SKZ_Logo_html, unsafe_allow_html=True)

st.sidebar.caption("[Bug reports and suggestions welcome ](mailto:c.kugler@skz.de)")

#---------------------------------------------columns---------------------------------------------------------------------


#st.write(result_df)
parameter=""
engineering_flag=""
with col1:
    st.title('Suitable surveillance parameters:​') 
    parameters=result_df['Valuetobemonitored'].tolist()
    for item in parameters:
        if st.button(item, key=item):
           parameter=item
           sensor_df=result_df[result_df["Valuetobemonitored"]==item]
           engineering_flag=sensor_df["additionalengineeringoradaptionadvised"].iloc[0]
    if engineering_flag !="" and engineering_flag=="yes":
        st.write("")
        st.write("")
        st.write("")
        st.markdown("__We strongly recommend consultation for the right implementation of the sensor__")
    if (parameter==""):
        st.write("Please choose a Parameter for Monitoring")
        

with col2:
    st.title('Suitable Sensor Type:​')
    if parameter!="":       
        st.write(sensor_df["SuitableSensoring"].iloc[0])
         
    st.title('Manufacturers for the shown type of sensors')

    if parameter!="":
        
        st.write(f"[{sensor_df['Manufacturerone'].iloc[0]}]({sensor_df['Manufactureronelink'].iloc[0]})")
        st.write(f"[{sensor_df['Manufacturertwo'].iloc[0]}]({sensor_df['Manufacturertwolink'].iloc[0]})")
        st.write(f"[{sensor_df['Manufacturerthree'].iloc[0]}]({sensor_df['Manufacturerthreelink'].iloc[0]})")
       
