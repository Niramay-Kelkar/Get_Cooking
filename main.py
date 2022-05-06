from fastapi import FastAPI
import pandas as pd
from Food_Search import *

app = FastAPI()

@app.get("/")
def root():
    return{'message':'Hello World!'}

@app.get("/ingredients/{ingredients}/number/{num}")
def getRecommendations(ingredients, num):
    r =  get_pred(ingredients, num)
    return r


def get_pred(ingredients, number):
    ingred = ingredients.split(", ")
    n_rec = int(number)
    recipe = search_ingredients(ingred , n_rec)
    recipe['recipe_urls'] = recipe['recipe_urls'].apply(make_clickable)
    #recipe = recipe.to_html(escape=False)
    return recipe

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('/')[5]
    return f'<a target="_blank" href="{link}">{text}</a>'