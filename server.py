from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

# Load the data from CSV files
restaurants_df = pd.read_csv('restaurants.csv')
hotels_df = pd.read_csv('hotels.csv')

@app.route('/city', methods=['POST'])
def get_places_by_city():
    data = request.json
    city = data.get('city')

    if not city:
        return jsonify({'error': 'City not provided'}), 400

    # Filter restaurants by city
    city_restaurants = restaurants_df[restaurants_df['location'].str.lower() == city.lower()]

    # Sort restaurants by rating (descending) and price (ascending), then select top 5
    top_restaurants = city_restaurants.sort_values(by=['rating', 'average_price'], ascending=[False, True]).head(5)

    # Filter hotels by city
    city_hotels = hotels_df[hotels_df['city_name'].str.lower() == city.lower()]

    # Handle missing price values by filling with a high value to push them down in sorting
    city_hotels['Price'].fillna(city_hotels['Price'].max() + 1, inplace=True)

    # Sort hotels by rating (descending) and price (ascending), then select top 5
    top_hotels = city_hotels.sort_values(by=['Rating', 'Price'], ascending=[False, True]).head(5)

    # Convert results to dictionary format for JSON response
    top_restaurants_result = top_restaurants.to_dict(orient='records')
    top_hotels_result = top_hotels.to_dict(orient='records')

    return jsonify({
        'restaurants': top_restaurants_result,
        'hotels': top_hotels_result
    })

if __name__ == '__main__':
    app.run(debug=True)
