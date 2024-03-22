import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit_option_menu as sto
import psycopg2
import requests
import json

myconnection=psycopg2.connect(host='127.0.0.1',user='postgres',password='yusuff@12345',port='5432',database='phonepe')
cursor=myconnection.cursor()

cursor.execute("SELECT * FROM agg_transaction")
myconnection.commit()
table1=cursor.fetchall()
agg_trans=pd.DataFrame(table1,columns=["State","Quarter","Transaction Type","Transaction amount","Transaction count","Year"])

cursor.execute("SELECT * FROM agg_user")
myconnection.commit()
table1=cursor.fetchall()
agg_user=pd.DataFrame(table1,columns=["Mobile Brand","Total count","Percentage","Quarter","State","Year"])

cursor.execute("SELECT * FROM map_transaction")
myconnection.commit()
table1=cursor.fetchall()
map_trans=pd.DataFrame(table1,columns=["City","Transaction count","Transaction amount","Quarter","Year","State"])

cursor.execute("SELECT * FROM map_user")
myconnection.commit()
table1=cursor.fetchall()
map_user=pd.DataFrame(table1,columns=["District","Registered Users","App Opens","Quarter","Year","State"])

cursor.execute("SELECT * FROM top_transaction")
myconnection.commit()
table1=cursor.fetchall()
top_trans=pd.DataFrame(table1,columns=["State","Transaction Type","Transaction count","Transaction amount","Quarter","Year"])

cursor.execute("SELECT * FROM top_user")
myconnection.commit()
table1=cursor.fetchall()
top_user=pd.DataFrame(table1,columns=["District","Registered Users","Quarter","Year","State"])

def trans_amount_count(df,year):
    trans_y=df[df['Year']==year]
    trans_y.reset_index(drop=True,inplace=True)
    trans_g=trans_y.groupby("State")[['Transaction count','Transaction amount']].sum()
    trans_g.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        url='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for i in data1["features"]:
            state_name.append(i['properties']['ST_NM'])
        state_name.sort()
        fig_india=px.choropleth(trans_g,geojson=data1,locations=state_name,featureidkey='properties.ST_NM',color='Transaction amount',color_continuous_scale="twilight",range_color=(trans_g['Transaction amount'].min(),trans_g['Transaction amount'].max()),hover_name='State',
                                title=f"{year} Transaction Amount",fitbounds="locations",height=800,width=750)
        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)
        
    with col2:
        fig_india1=px.choropleth(trans_g,geojson=data1,locations=state_name,featureidkey='properties.ST_NM',color='Transaction count',color_continuous_scale="twilight",range_color=(trans_g['Transaction count'].min(),trans_g['Transaction count'].max()),hover_name='State',
                                title=f"{year} Transaction count",fitbounds="locations",height=800,width=800)
        fig_india1.update_geos(visible=False)
        st.plotly_chart(fig_india1)
    
    col1,col2=st.columns(2)
    with col1:
        #st.markdown(f'<style>div.row-widget.stHorizontal>{{"flex-wrap": "wrap";}}</style>', unsafe_allow_html=True)
        #st.markdown(f'<style>.reportview-container .main .block-container{{max-width: 50px;}}</style>', unsafe_allow_html=True)

        figure_trans_count=px.bar(trans_g, x="State" , y="Transaction count",title=f"{year} Transaction count",height=600,width=750,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(figure_trans_count)
    with col2:
        #st.markdown(f'<style>div.row-widget.stHorizontal>{{"flex-wrap": "wrap";}}</style>', unsafe_allow_html=True)
        #st.markdown(f'<style>.reportview-container .main .block-container{{max-width: 100px;}}</style>', unsafe_allow_html=True)
        figure_trans_amount=px.bar(trans_g,x='State',y="Transaction amount",title=f"{year} Transaction amount",height=600,width=750,color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(figure_trans_amount)
    return trans_y

def trans_amount_count_quarter(df,quarter):
    trans_q=df[df['Quarter']==quarter]
    trans_q.reset_index(drop=True,inplace=True)
    trans_g=trans_q.groupby("State")[['Transaction count','Transaction amount']].sum()
    trans_g.reset_index(inplace=True)
    url='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for i in data1["features"]:
        state_name.append(i['properties']['ST_NM'])
    state_name.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india=px.choropleth(trans_g,geojson=data1,locations=state_name,featureidkey='properties.ST_NM',color='Transaction amount',color_continuous_scale="twilight",range_color=(trans_g['Transaction amount'].min(),trans_g['Transaction amount'].max()),hover_name='State',
                            title=f"Quarter {quarter} of Year {df['Year'].unique()} Transaction Amount",fitbounds="locations",height=800,width=700)
        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)
        
    with col2:
        fig_india1=px.choropleth(trans_g,geojson=data1,locations=state_name,featureidkey='properties.ST_NM',color='Transaction count',color_continuous_scale="twilight",range_color=(trans_g['Transaction count'].min(),trans_g['Transaction count'].max()),hover_name='State',
                                title=f"Quarter {quarter} of Year {df['Year'].unique()} Transaction count",fitbounds="locations",height=800,width=800)
        fig_india1.update_geos(visible=False)
        st.plotly_chart(fig_india1)
    col1,col2=st.columns(2)
    with col1:
        figure_trans_count=px.bar(trans_g, x="State" , y="Transaction count",title=f"Quarter {quarter} of Year {df['Year'].min()} Transaction count",height=600,width=750,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(figure_trans_count)
    with col2:
        figure_trans_amount=px.bar(trans_g,x='State',y="Transaction amount",title=f"Quarter {quarter} of Year {df['Year'].min()} Transaction amount",height=600,width=750,color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(figure_trans_amount)

def user_transbr_fig(df,year,state,quarter):
    agg_state=df[df['State']==state]
    agg_state.reset_index(drop=True,inplace=True)
    agg_year=agg_state[agg_state['Year']==year]
    agg_year.reset_index(drop=True,inplace=True)
    agg_quat=agg_year[agg_year['Quarter']==quarter]
    agg_quat.reset_index(drop=True,inplace=True)
    agg_quat_g=agg_quat.groupby("Mobile Brand")[['Total count']].sum()
    agg_quat_g.reset_index(inplace=True)
    fig_quat=px.bar(agg_quat_g,x="Mobile Brand",y="Total count",title=f"{state}'s user transaction count in quarter {quarter} of year {year} figure"
                    ,hover_name="Mobile Brand",color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_quat)

def map_district(df,state):
    trans_q=df[df['State']==state]
    trans_q.reset_index(drop=True,inplace=True)

    trans_q=trans_q.groupby("City")[['Transaction amount',"Transaction count"]].sum()
    trans_q.reset_index(inplace=True)
    trans_q
    fig_trans_amount_bar=px.bar(trans_q,x='Transaction amount',y='City',width=800,title=f"{state} Transaction amount",color="Transaction amount"
                                )
    st.plotly_chart(fig_trans_amount_bar)
    fig_trans_count_bar1=px.bar(trans_q,x='Transaction count',y='City',width=800,title=f"{state} Transaction count",color="Transaction count")
    st.plotly_chart(fig_trans_count_bar1)

st.set_page_config(layout="wide")

st.markdown(f"<h3 style=color:#F88379><center>PhonePe capstone project</center></h3>",unsafe_allow_html=True)

selected=sto.option_menu(
        menu_title=None,
        options=["Overview","Data analysis"],
        orientation="horizontal",
        icons=["1-circle-fill","2-circle-fill"],
        menu_icon="bank2",
        default_index=0)   

if selected=="Overview":
    st.header(":violet[PhonePe Pulse data visualization]")
    st.write("PhonePe Pulse Data Visualization and Exploration is a fascinating project that provides a user-friendly tool for exploring and visualizing data from the PhonePe Pulse Github repository.")
    st.header(":violet[About Phonepe]")
    st.write("PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India.Founded in December 2015, PhonePe offers a wide range of services, including money transfers, mobile recharges, utility bill payments, investments, and more.")
    st.write(f'''The PhonePe Pulse Data Visualization and Exploration project aims to:\n
                \n1.Extract data from the PhonePe Pulse Github repository.\n
                \n2.Transform and preprocess the data using Python and libraries like Pandas.\n
                \n3.Store the processed data in a MySQL database.\n
                \n4.Create an interactive and visually appealing dashboard using Streamlit and Plotly.\n
                \n5.Enable users to explore and visualize their transaction data effectively.''')
if selected=="Data analysis":
    st.header(':violet[Phonepe Pulse Data Visualization ]')
    st.write('**(Note)**:-This data between **2018** to **2022** in **INDIA**')
    col1,col2,col3=st.columns(3)
    with col3:
        state=st.selectbox("Select the state (only used for user analysis)",['Andaman And Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'])
    with col1:
        year=st.selectbox("Select year",[2018,2019,2020,2021,2022,2023])
    with col2:
        quarter=st.selectbox("Select quarter",[1,2,3,4])
    tab1,tab2,tab3=st.tabs(["Aggregrated analysis","Map analysis","Top analysis"])
    

    with tab1:
        option=st.radio("Select the option to show the analysis of the selected data",["Aggregated Transaction","Aggregated User"])
        if option=="Aggregated Transaction":
             tab4,tab5,tab6=st.tabs(["Year analysis","Quarter analysis","Transaction analysis"])
             with tab4:
                st.header(":violet[Year analysis]")
                #slide=st.slider("Select the year",agg_trans['Year'].unique().min(),agg_trans['Year'].unique().max())
                trans_year=trans_amount_count(agg_trans,year)
             #col1,col2=st.columns(2)'
             with tab5:
                st.header(":violet[Quarter analysis]")
                st.write(f"{state}'s Quarter {quarter} of year {year} analysis")
                #option=st.selectbox("Choose quarter",trans_year['Quarter'].unique())             
                trans_amount_count_quarter(trans_year,quarter)
             with tab6:
                 st.header(":violet[Transaction analysis]")
                 trans_s=trans_year[trans_year['State']==state]
                 trans_s.reset_index(drop=True,inplace=True)
                 trans_sg=trans_s.groupby("Transaction Type")[['Transaction amount',"Transaction count"]].sum()
                 trans_sg.reset_index(inplace=True)
                 fig_trans_amount_pie=px.pie(data_frame=trans_sg,names='Transaction Type',values='Transaction amount',width=800,title="Transaction amount",color="Transaction amount"
                                            ,hole=0.2)
                 st.plotly_chart(fig_trans_amount_pie)
                 fig_trans_count_pie=px.pie(data_frame=trans_sg,names='Transaction Type',values='Transaction count',width=800,title="Transaction count",color="Transaction count",hole=0.2)
                 st.plotly_chart(fig_trans_count_pie)
        elif option=="Aggregated User":
             st.header(":violet[Aggregrated User analysis]")
             st.write(f"Below you can find the analysis of {state}")
             col1,col2,col3=st.columns(3)
             user_transbr_fig(agg_user,year,state,quarter)
             
    with tab2:
        option1=st.radio("Select the option to show the analysis of the selected data",["Map Transaction","Map User"])
        if option1=="Map Transaction":
            st.header(":violet[Map transaction analysis]")
            st.write(f"{state}'s of year {year} analysis")
            map_trans_y=trans_amount_count(map_trans,year)
            st.header(":violet[Map transaction District]")
            st.write(f"{state}'s Quarter {quarter} of year {year} analysis")
            map_district(map_trans_y,state)
            #map_trans_year_quarter=trans_amount_count_quarter(map_trans_y,quarter)
            #map_district(map_trans_year_quarter,state)
        elif option1=="Map User":
             st.header(":violet[Map user analysis]")
             st.write(f"Below you can find the analysis of {state}")
             user_y=map_user[map_user['Year']==year]
             user_y.reset_index(drop=True,inplace=True)
             states=user_y[user_y['State']==state]
             users_g=states.groupby('District')[['Registered Users']].sum()
             users_g.reset_index(inplace=True)
             figure_user_count=px.bar(users_g, x="District" , y="Registered Users",title=f"{state}'s District and Transaction count of year {year}"
                                      ,height=600,width=750,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="District")
             st.plotly_chart(figure_user_count)
    with tab3:
        option2=st.radio("Select the option to show the analysis of the selected data",["Top Transaction","Top User"])
        if option2=="Top Transaction":
             st.write(f"Below graphs and map are entire top transaction of the year {year} in {state}")
             top_trans1=trans_amount_count(top_trans,year)
             st.header(":violet[Quarter analysis]")
             st.write(f"Below graphs and map are entire top transaction of the quarter {quarter} in year {year} of the each state")
             top_trans1_quat=trans_amount_count_quarter(top_trans1,quarter)
        elif option2=="Top User":
             col1,col2=st.columns(2)
             with col2:
                st.header(f":violet[Top registered users chart in {year}]")
                st.write(f"Below you can find the analysis of {state}")
                top_user_y=top_user[top_user['Year']==year]
                top_user_y.reset_index(drop=True,inplace=True)
                top_state=top_user_y[top_user_y['State']==state]
                top_users_g=top_state.groupby('District')[['Registered Users']].sum()
                top_users_g.reset_index(inplace=True)
                figure_top_user_count=px.bar(top_users_g, x="District" , y="Registered Users",title=f"District and Transaction count",height=600,width=600,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="District")
                st.plotly_chart(figure_top_user_count)

             with col1:
                 st.header(f":violet[Top registered users in {year} in {state}]")
                 top_users_g
                 st.header(" \n ")
                 st.header(" \n ")
                 st.header(" \n ")
                 st.header(" \n ")
                 st.header(" \n ")
                 st.header(" \n ")
                 st.header(f":violet[Top Registered users in {year} in INDIA]")
                 top_user_y=top_user[top_user['Year']==year]
                 top_user_y.reset_index(drop=True,inplace=True)
                 top_user_g=top_user_y.groupby("State")['Registered Users'].sum()
                 df_g=pd.DataFrame(top_user_g)
                 df_g.reset_index()
                 url='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
                 response=requests.get(url)
                 data1=json.loads(response.content)
                 state_name=[]
                 for i in data1["features"]:
                     state_name.append(i['properties']['ST_NM'])
                 state_name.sort()
                 fig_india=px.choropleth(df_g,geojson=data1,locations=state_name,featureidkey='properties.ST_NM',color='Registered Users',color_continuous_scale="twilight",range_color=(df_g['Registered Users'].min(),df_g['Registered Users'].max()),
                                         title=f"Quarter {quarter}  of Year {year} Top user",fitbounds="locations",height=600,width=600)
                 fig_india.update_geos(visible=False)
                 st.plotly_chart(fig_india)



    


