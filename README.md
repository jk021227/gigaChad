# Team Members 🤖

`jk021227` - Jhon Kim 

`shayanahmad7`- Shayan Ahmad

`bipana06` - Bipana Bastola 


# Description 👐

This is a web scrapping project that extracts restaurant/menu data from Deliveroo's website using beautifulsoup4 and the requests pacakge in Python. Deliveroo is an online food delivery company based in UK but with a strong presence in the UAE. All of our group members frequently use this back in Abu Dhabi. Our project essentially scrapes UAE's deliveroo's data and uses it to create a meal plan recommendation to the user.

# How does it work ❓

It fetches the top restaurant for each cuisine (American, Arabic, Asian, etc.) under top offers, scrapes all of each restaurant's menu items alongside its description and price. It saves this into a csv file database which is then used in `macros.py` where we make API calls to populate the database with further nutritional information per menu item (i.e. protein, carbs, fat in grams). Finally, this consolidated database called (`restaurants_sample_with_nutrition.csv`) is then used to in `meal_plan.py` where the user is asked a series of questions such as their age, weight, height, gender, and their nutritional goals. After the program gets all the information from the user, it generates a meal plan for the user based on their information from the database.

# Installation 🐛

To get started, clone the repository to your local machine and navigate to the project's directory. 

Inside of `gigaChad/`, create a `.env` file with the following contents:

```
{
    OPENAI_API_KEY=YOUR_API_TOKEN_HERE
}
```
Replace the text `YOUR_API_TOKEN_HERE` with your OpenAI API Key, and save. 

# Dependencies 🫶

gigaChad uses OpenAI's API that require unique keys for access. 

If you do not have a personal OpenAI API key, create an account via this [link](https://platform.openai.com/), charge your account with money💰 then create an API key. Once you do that, copy that API key and place it inside your .env file as OPENAI_API_KEY=(your API key).

# How to run 🏃‍♀️

Since running `macros.py` costs money due to the OpenAI API, we've created a `restaurants_sample_with_nutrition.csv` file for you to use with `meal_plan.py`! How thoughtful of us 💕 So, to save both money and time (because time is money), simply run the following commands in your terminal:

```bash
pip install -r requirements.txt
python meal_plan.py
```

And... voilà! You'll now have your very own meal recommender that helps you meet your nutritional goals!

# Side notes 📝

1. We have only scrapped 1 restaurant for each cuisine under top offers since that's already around ~1300 menu items. If you want to get a larger database, with all the restaurants per cuisine, in line 19 of `main.py`, remove `[:1]` from `for tag in restaurant_tags[:1]:` to just `for tag in restaurant_tags:`.

2. Since the data is being acquired from multiple links for different cuisines, it might take some time for the program to finish running, so be patient please. 🥰