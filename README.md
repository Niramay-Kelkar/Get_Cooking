# GetCooking

Cooking Recommendations

### Overview
Cooking is both a passion and a big concern for some people. Cooking, on the other hand, can always use a helping hand. Being a student, deciding what to eat for lunch or dinner is always a challenge. When you only have a few ingredients in the kitchen, deciding what to make for dinner might be difficult. This prompted us to develop a system that can suggest recipes based on suggested ingredients. Recipe provider that uses web-scraped recipe data to provide users with the recipes based on their preferences and the ingredients they have.

### Goals
1. Create a search algorithm that utilizes similarity scoring to rank recipes according to the greatest similarity to the search query.
2. To provide recipes when the user has limited items in the kitchen, or cannot decide what to cook for his/meal.
3. Recommend recipes based on the dish name
4. Recommend recipes based on the ingredients the user has with him/her.

### Code Structure
<img width="267" alt="Screen Shot 2022-05-06 at 5 57 10 AM" src="https://user-images.githubusercontent.com/91446801/167110572-5838023a-5f95-4499-ab20-2df354595670.png">
main.py
readME.md
Food_search.py

### Dataset and Pre-processing
Scraped data from : https://www.jamieoliver.com/
#### Content extracted:
   - Recipe_urls
   - Recipe name
   - Ingredients
   - Serves
   - Cooking_time
   - Difficulty
#### Pre-processed dataset:
   - Recipe_urls
   - Recipe
   - Ingredients
   - Ingredients_parsed (stopwords, measure, unnecessary words like fresh, etc. removed)


### Modules
- Data Scraping (using BeautifulSoup) and Pre-Processing 
- API for Fetching Recipes - FastAPI
- Streamlit UI
- User Authentication and User Authorization - JWT
- Airflow workflows using Cloud Composer
-- RecipeCache - For storing cache if the user has no ingredients and wants recipes to be suggested
-- SendingEmails - when the user registers for subscriptions
- Data Validation and Unit testing - Regex and Pytests
- Deployment on Cloud (GCP)
- Hosting Streamlit - Streamlit.io
- Visualizations - Big Query and Data Studio
- Github Issues and Actions

### Folder Structure
#### Streamlit UI
 - Functionality:
If the user provides ingredients, search through the dataset and recommend recipes based on the ingredients that match. 
If the user has no ingredients, provide recipes from cache

##### Includes:
- User authentication and authorization using JWT
- App design elements
- Import data validations using regex
- Storing the registered users’ info and uploading it into GCP storage buckets
##### Files:
- Streamlit.py - has the design of the UI with error handling
- FoodSearch.py - takes the ingredients and gives dataframe as output based on the user input

#### FastAPI

- Input : User input of ingredients and no. of recommendendations
- Hosted on GCP
- Output : Recommended dataframe, which will be displayed by Streamlit.io

#### Airflow 
##### Functionality:
- Automates the workflows like caching 
- Deployment on cloud using Google Cloud Composer
##### Includes:
- Two automation tasks deployed on GCP
- Cloud Composer syntax of defining DAGs
- Storing the cache results on cloud
##### Files:
- Food_search_dag.py - for randomly updating cache daily to store 5 recipes 
- Send_email_dag.py - to send emails to the registered users 


#### Data Validations and Pytesting
Contains sample pytesting for the user input on Streamlit. The sample test cases and the status of the tests ran are uploaded in the same folder.

#### Data Visualization
- Geographical map - describes the location of the registered users
- Stacked column chart - shows the people who are satisfied by the app and who are not
- Pie Chart - shows the distribution of the users across different locations
- Bar Graph - shows the number of people registered from each location

<img width="817" alt="Visualization" src="https://user-images.githubusercontent.com/91446801/167113258-4f1073fb-26c1-4987-abf7-b933614f1a4e.png">

##### Details:
 - Once a new user registers, the user registry gets updated
The registry automatically gets uploaded to Storage bucket.
- Using BigQuery and Data Studio, the visualization are obtained

#### GitHub Actions
Find the workflow here : https://github.com/AkankshaTelagamsetty12/Get-Cooking-/actions/workflows/main.yml


## Test our aplication
To run our application, click on this link : https://share.streamlit.io/niramay-kelkar/get_cooking/main/Streamlit/streamlit.py

## Other useful links:
- Link to codelabs : https://codelabs-preview.appspot.com/?file_id=1wDG5Zv-_qauEu3lgfElM2hEnYv1rx5L9cm4OHCesvGk#2
- Link to Github issues : https://github.com/Niramay-Kelkar/Get-Cooking/projects/1
- Link to previous working repo : https://github.com/Niramay-Kelkar/Get-Cooking.git

### References

1. Fast API Authentication : https://www.youtube.com/watch?v=6hTRw_HK3Ts
2. Apache Airflow : https://insaid.medium.com/setting-up-apache-airflow-in-macos-2b5e86eeaf1
3. Cloud Composer : https://towardsdatascience.com/airflow-by-google-a-first-impression-of-cloud-composer-f4d9f86358cf
4. Send Emails Using Code : https://www.youtube.com/watch?v=Y_tnWTjTfzY
5. Web Scraping : https://towardsdatascience.com/building-a-recipe-recommendation-system-297c229dda7b
6. Uploading to GCP : https://stackoverflow.com/questions/40683702/upload-csv-file-to-google-cloud-storage-using-python
7. Unit Testing : https://www.youtube.com/watch?v=byaxg00Gf9I
8. BigQuerying using files from GCP storage : https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv
9. GitHub Actions : https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action
10. Streamlit UI : https://docs.streamlit.io/library/api-reference

