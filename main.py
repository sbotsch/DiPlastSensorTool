

import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.

import numpy as np
import pandas as pd
from PIL import Image
import os
import base64



#set page icon,title and layout
st.set_page_config(page_title="Di-Plast Sensor Selection ",layout="wide", page_icon = "favicon.png")

# one could specify the burger menu
#menu_items={"About":"Made by SKZ","Report a Bug":None,"Get help":None })



#for image rendering with link, magic from https://discuss.streamlit.io/t/href-on-image/9693/4
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
@st.cache(allow_output_mutation=True)

#use this in code to display image
def get_img_with_href(local_img_path, target_url,width="1"):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img style="width: {width}%" src="data:image/{img_format};base64,{bin_str} " />
        </a>'''
    return html_code

#remove colored bar and menu
#header {visibility: hidden;}
#MainMenu {visibility: hidden;} #hides Menu in Style
hide_streamlit_style = """
            <style>           
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#remove padding of widgets
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}4em;
        padding-left: {padding}4em;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

#-------------------------------------------------------------------------------------------------------

#Initialize Session state------------------------------------------------------------------------------
if 'choose_process' not in st.session_state:
    st.session_state['choose_process'] = False

if 'choose_problem' not in st.session_state:
    st.session_state['choose_problem'] = False

if 'choose_cause' not in st.session_state:
    st.session_state['choose_cause'] = False    

if 'choose_parameter' not in st.session_state:
    st.session_state['choose_parameter'] = False   




#-------------------------callbacks from selectboxes-------------------------------------------------------------------
def on_change_process():
    st.session_state['choose_process'] = True   
    st.session_state['choose_problem'] = False
    st.session_state['choose_cause'] = False
    st.session_state['choose_parameter'] = False


    print("CHANGE_process")

def on_change_problem():
    st.session_state['choose_problem'] = True

    st.session_state['choose_cause'] = False
    st.session_state['choose_parameter'] = False
    print("CHANGE_problem")

def on_change_cause():
    st.session_state['choose_cause'] = True
    
    print("CHANGE_problem")

def on_click_parameter():
    st.session_state['choose_parameter']=True
#----------------------------------------------------------------------------------------------------


st.markdown('<style>body{background-color: Blue;}</style>',unsafe_allow_html=True)

with st.sidebar:
#image = Image.open('Logo.png')
    #display project logo in sidebar
    Logo_html = get_img_with_href('Logo.PNG', 'https://www.nweurope.eu/projects/project-search/di-plast-digital-circular-economy-for-the-plastics-industry/',width="80")
    st.markdown(Logo_html, unsafe_allow_html=True)

#st.sidebar.image(image, width=250)
    st.title('Di-Plast Sensor Selection')
    df=pd.read_excel("Di_Plast_Database.xlsx", index_col=None,engine='openpyxl') 
    list_process=df.Process.unique()

    #if(st.session_state["choose_process"]!=True):
    
    list_process=np.insert(list_process,0,"Please select")
    process=st.selectbox("What is your production process?",list_process,help="Please select your production process!​",on_change=on_change_process)
    problem_df = df[df['Process'] ==process ]

    list_problem=problem_df.Problem.unique()
    
    
    #if(st.session_state['choose_problem']!=True):
        #list_problem=sorted(problem_df.Problem.unique())

    if (st.session_state['choose_process']==True and process!= "Please select"):
        print(list_problem)
        list_problem=np.insert(list_problem,0,"Please select")
        problem=st.sidebar.selectbox("What is your process problem?​",list_problem,help="Please select your production problem!​",on_change=on_change_problem)
        cause_df=df[(df["Process"]==process) & (df["Problem"]==problem)]  
        list_cause=sorted(cause_df.Causerankfirstorder.unique())
        

    if (st.session_state['choose_problem']==True and problem!="Please select"):
        
        list_cause=np.insert(list_cause,0,"Please select")
        second_box_var=1
        #if(st.session_state['choose_cause']!=True):
        
        #second_box_var=2
        
        cause=st.selectbox("What could be the cause for the problem?​",list_cause,help="Please select what is causing the problem in your opinion!​",on_change=on_change_cause)
    
        cause_df=df[(df["Process"]==process) & (df["Problem"]==problem)& (df["Causerankfirstorder"]==cause)]
        list_cause_snd=sorted(cause_df.Causeranksecondorder.unique())
        cause_snd=""
        print(len(list_cause_snd))

        if len(list_cause_snd)>second_box_var:
            cause_snd =st.sidebar.selectbox("Please specify the cause!",list_cause_snd,help="Please specify the cause according to your experience!")

        if cause_snd!="":
            result_df=df[(df["Process"]==process) & (df["Problem"]==problem)& (df["Causerankfirstorder"]==cause)& (df["Causeranksecondorder"]==cause_snd)]
        else:
            result_df=cause_df

            st.write("")
            st.write("")




    SKZ_Logo_html = get_img_with_href('SKZ-Logo.png', 'https://www.skz.de',width="70")
    st.markdown(SKZ_Logo_html, unsafe_allow_html=True)
    st.markdown('<a href="mailto:c.kugler@skz.de?subject= Feedback Di-Plast Sensor Tool">Bug reports and suggestions welcome</a>', unsafe_allow_html=True)
    st.caption("Christoph Kugler (c.kugler@skz.de)")
    st.write("[Back to the Di-Plast Knowledge Hub](https://di-plast.sis.cs.uos.de/)")
    if(st.session_state['choose_problem']!=True):
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.text('')
            st.subheader('')
    
            


    #---------------------------------------------columns---------------------------------------------------------------------
if(st.session_state['choose_cause']==False):
    st.header('About')
    st.write('''This is the Di-Plast Sensor Selection Tool. The tool is meant to be used for process troubleshooting in plastics conversion. It supports in narrowing down the problem causes and finding a suitable monitoring strategy.
    You can start instantly by following the selections one by one starting on the top left side with the process. A dropdown shows all available selections. (More alternatives to be added in the future.)
    While answering what is the process and what is the problem is usually not complicated it can be complicated to define the cause for the problem. Since all the previously made selections stay active you can change any selection at any time during the process, but it may alter the selections that are based on the previous ones if the case is not available (i.e. sagging in injection moulding).
    After making the selections in the left side area the suitable surveillance parameters are displayed in the upper centre. Clicking on one of the parameters shows suitable sensors, manufacturers for those sensors (direct link) and an advice whether consulting for implementation is necessary.''')
    st.write('''The Sensor Selection tool is funded by the [Interreg North-West Europe program (Interreg NWE, NWE729)](https://www.nweurope.eu/projects/project-search/di-plast-digital-circular-economy-for-the-plastics-industry/), project Di-Plast - Digital Circular Economy for the Plastics Industry''')

    st.header('Disclaimer of Warranty')
    st.write('''There is no warranty for the program, to the extent permitted by applicable law. Except when otherwise stated in writing the copyright holders and/or other parties provide the program “as is” without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the program is with you. should the program prove defective, you assume the cost of all necessary servicing, repair or correction.''')
    st.header('Limitation of Liability')
    st.write('''In no event unless required by applicable law or agreed to in writing will any copyright holder, or any other party who modifies and/or conveys the program as permitted above, be liable to you for damages, including any general, special, incidental or consequential damages arising out of the use or inability to use the program (including but not limited to loss of data or data being rendered inaccurate or losses sustained by you or third parties or a failure of the program to operate with any other programs), even if such holder or other party has been advised of the possibility of such damages.''')



if(st.session_state['choose_cause']==True):
#st.write(result_df)
    parameter=""
    engineering_flag=""
  
    st.subheader('Suitable surveillance parameters:​') 
    #if (st.session_state["choose_parameter"]!=True):
    text_please="<p style='color:Blue;font-size: 1 em;'>Please click on parameter to monitor</p>"
    st.markdown(text_please, unsafe_allow_html=True)
   


    
    parameters=result_df['Valuetobemonitored'].tolist()
    for item in parameters:
        if st.button(item, key=item,on_click=on_click_parameter):
            parameter=item
            sensor_df=result_df[result_df["Valuetobemonitored"]==item]
            engineering_flag=sensor_df["additionalengineeringoradaptionadvised"].iloc[0]
    
    text_line="<hr/>"
    st.markdown(text_line, unsafe_allow_html=True)    

    
    if parameter!="":
    
        
        st.subheader('Suitable sensor type:​')   
       
        text_sensor=f"<p style='color:Black;font-size: 1.5em;'> {sensor_df['SuitableSensoring'].iloc[0]}</p>"
        st.markdown(text_sensor, unsafe_allow_html=True)
        text_line="<hr/>"
        st.markdown(text_line, unsafe_allow_html=True)  
        
    
     
    if parameter!="" and st:
       
        st.subheader(' Examples of manufacturers of the shown type of sensors:')
      
        st.write(f"- [{sensor_df['Manufacturerone'].iloc[0]}]({sensor_df['Manufactureronelink'].iloc[0]})")
        st.write(f"- [{sensor_df['Manufacturertwo'].iloc[0]}]({sensor_df['Manufacturertwolink'].iloc[0]})")
        st.write(f"- [{sensor_df['Manufacturerthree'].iloc[0]}]({sensor_df['Manufacturerthreelink'].iloc[0]})")
    if engineering_flag !="" and engineering_flag=="yes" and st.session_state["choose_parameter"]==True:
        st.write("")
        
        
        text_recommend="<p style='color:red;font-size: 1.2em;'>We strongly recommend consultation for the right implementation of the sensor</p>"
        st.markdown(text_recommend, unsafe_allow_html=True)
        
