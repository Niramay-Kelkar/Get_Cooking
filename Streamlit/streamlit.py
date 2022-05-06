from pydoc import cli
from random import sample
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import storage
import numpy as np
import pandas as pd
import streamlit_authenticator as stauth
from PIL import Image
import requests
# Bring your packages onto the path
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

# Now do your import
from Food_Search import *

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('/')[5]
    return f'<a target="_blank" href="{link}">{text}</a>'

def validate_phone(phone_number):
    if len(phone_number)<10:
        raise ValueError("Phone number cannot be less than 10")

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials)
table_id = 'recipe-recommendation-348000.get_cooking.users'

# Perform query.
# Reference: https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries#bigquery_simple_app_query-python
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.experimental_memo to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

# Reference link: https://cloud.google.com/bigquery/docs/updating-data#python
def updateApihits(query):
    query_job = client.query(query)
    query_job.result()    
    assert query_job.num_dml_affected_rows is not None
    return query_job.num_dml_affected_rows

fullnames = run_query("SELECT fullname FROM " + table_id +  " LIMIT 10")
password_rows = run_query("SELECT password FROM " + table_id + " LIMIT 10")
password = []
names = []
unames = []
uname = run_query("SELECT username FROM " + table_id + " LIMIT 10")

# Print results.
for row in password_rows:
    password.append(row['password'])

for row in fullnames:
    names.append(row['fullname'])

for row in uname:
    unames.append(row['username'])

# Reference: https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031
hashed_passwords = stauth.Hasher(password).generate()

authenticator = stauth.Authenticate(names,unames,hashed_passwords,
    'stauth','mysecretkey',cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    getCurrentUser = username
    apihits = run_query("SELECT apihits FROM " + table_id + " WHERE username = " + ("'%s'" % (getCurrentUser)))
    st.markdown("# *Get Cooking! :cooking:*")
    image = 'https://storage.cloud.google.com/get-cooking/image.jpeg'
    st.image(image, caption='', width=700)
    
    st.markdown(
        "## You have the ingredients, we have the recipes for you! :genie: "
    )
    st.markdown(
        "### Given a list of ingredients, what different recipes can you make? :stew: "
    )
    
    st.markdown(
        "For example, what recipes can you make with the food in your kitchen? :bento: Our app will look through over thousands of recipes to find top matches for you! :mag: Try it out for yourself below! :arrow_down:"
    )

    st.text("")

    selection = st.selectbox(
     'Do you have any ingredients? Worry not if you do no have them; we will suggest you some easy recipes!',
     ('Select','Yes', 'No'))

    container = st.container()

    if selection == 'Yes':
        
        with st.container():
            ingredients = st.text_input("Enter ingredients you would like to cook with")
            if str(ingredients).isnumeric():
                st.write("Enter valid ingredient!")
            n_rec = st.text_input("Enter number of recipes you want")
            execute_recsys = st.button("Give me recommendations!")

            if execute_recsys :
                if int(n_rec)>0:
                    ingred = ingredients.split(", ")
                    n_rec = int(n_rec)
                    col1, col2, col3 = st.columns([1, 6, 1])
                    with col2:
                        gif_runner = st.image("input/cooking_gif.gif")
                    recipe = search_ingredients(ingred , n_rec)
                    # link is the column with hyperlinks
                    recipe['recipe_urls'] = recipe['recipe_urls'].apply(make_clickable)
                    recipe = recipe.to_html(escape=False)
                    st.write(recipe, unsafe_allow_html=True)
                    gif_runner.empty()
                
                elif int(n_rec) ==0: 
                    st.write("Please provide a value greater than zero. ")
                
                else:
                    st.write("Please provide a valid input")

    elif selection == 'No':
        client_bucket = storage.Client(credentials=credentials)
        bucket = client_bucket.get_bucket('get-cooking')
        
        blob = bucket.get_blob('dags/export_dataframe.csv')

        downloaded_blob = blob.download_as_string()
        from io import StringIO

        s=str(downloaded_blob,'utf-8')

        downloaded_blob = StringIO(s) 


        df_random=pd.read_csv(downloaded_blob)

        st.write(df_random)

        if st.button('Submit'):
            api=[]
            api = run_query("SELECT apihits FROM " + table_id + " WHERE username = " + ("'%s'" % (getCurrentUser)))
            print(api)
            apicount = 0
            apihit = [d['apihits'] for d in api]
            
            apicount = apihit[0] + 1
            for x in api:
                for y in x:
                    x.update({y: apicount})
            result = updateApihits("UPDATE " + table_id + " SET apihits = " + str(apicount) + " WHERE username = " + ("'%s'" % (getCurrentUser)))

            # res = requests.get(f"http://127.0.0.1:8000/{title}")
            # output = pd.read_csv(res)
            # print(output)
            # out = output.get("message")
            if apicount < 15:

                df = pd.read_csv('https://storage.googleapis.com/get-cooking/dataset/PP_users.csv')
                
                sample_data = df.head()
                st.dataframe(sample_data)
                st.write('The current recommendations is for ', title)
            else:
                st.write('User Request Limit Exceeded')
           
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')