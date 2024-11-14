import os
import json  # Import the json module for parsing
from flask import Flask, render_template, request
from groq import Groq
import re  # Import regular expression module for extracting JSON

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key='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')

# Function to get food recommendations from Groq based on mood
def get_food_recommendations(mood):
    chat_completion = client.chat.completions.create(
        messages=[ 
            {
                "role": "user",
                "content": f'''Recommend food based on the following mood: 
                {mood} 
                Provide the real life existing food recommendations in JSON format, with a "food_recommendations" field. 
                Each item in the list should include the food name and a URL to a recipe for that food.
                Make sure the url to recipe is a search onhttps://www.allrecipes.com/search?q="food"
                Give response only in json nothing else
                also add emojis before food name
                The format must be strictly follow:
                food_recommendations: [
                    {{ "food": "food_name", "recipe_url": "working_url_to_recipe" }},
                    ...
                ]
                ''' ,
            }
        ],
        model='llama3-70b-8192' #"llama3-8b-8192",  # Replace with the correct model if necessary
    )
    
    # Extract food recommendations from the API response
    food_recommendations = chat_completion.choices[0].message.content

    # Print the raw response for debugging purposes
    print("Raw API Response:")
    print(food_recommendations)

    # Use regex to extract the JSON portion of the response
    # match = re.search(r'```json\s*(\{.*\})\s*```', food_recommendations, re.DOTALL)

    try:
        food_json = json.loads(food_recommendations)
        print("Parsed JSON response:")
        print(food_json)
        return food_json.get('food_recommendations', [])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return ["Error parsing food recommendations"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the mood from the form
        mood = request.form['mood']
        
        # Get food recommendations for the given mood
        food_recommendations = get_food_recommendations(mood)
        print(food_recommendations)
        
        # Render the template with the food recommendations
        return render_template('index.html', food_recommendations=food_recommendations)
    
    return render_template('index.html', food_recommendations=None)

if __name__ == '__main__':
    app.run(debug=True)
