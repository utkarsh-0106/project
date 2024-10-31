from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie dataset
try:
    movies_list_df = pd.read_csv('movies_list.csv')
    print("Movies dataset loaded successfully.")
    print(movies_list_df.head())  # Print the first few rows to confirm
except Exception as e:
    print("Error loading movies dataset:", e)
    movies_list_df = pd.DataFrame()  # Create an empty DataFrame to prevent app crash

# Define mood categories and associated keywords (for simplicity)
mood_keywords = {
    'happy': ['comedy', 'adventure', 'animation', 'family', 'musical'],
    'sad': ['drama', 'tragedy', 'biography', 'war'],
    'excited': ['action', 'thriller', 'sci-fi', 'crime'],
    'romantic': ['romance', 'drama', 'love'],
    'adventurous': ['adventure', 'fantasy', 'sci-fi', 'action'],
    'motivational': ['biography', 'sports', 'inspirational', 'documentary']  # New entry for motivational mood
}

@app.route('/', methods=['GET'])
def index():
    # Ensure that movies_df is not empty
    if not movies_list_df.empty:
        movies_list = movies_list_df.to_dict(orient='records')
        return render_template('index.html', movies=movies_list)
    else:
        return "Movies dataset could not be loaded.", 500

# Function to categorize movies based on mood
def recommend_movies_by_mood(mood):
    # Get keywords associated with the selected mood
    keywords = mood_keywords.get(mood, [])
    print(f"Keywords for mood '{mood}':", keywords)
    
    # Filter movies that match the mood keywords in their genres
    filtered_movies = movies_list_df[movies_list_df['genres']
                                .str.lower()  # Convert genres to lowercase
                                .str.strip()  # Remove leading/trailing spaces
                                .str.contains('|'.join(keywords), na=False)]  # Match keywords
    
    # If no movies match, return a message
    if filtered_movies.empty:
        print(f"No movies found for mood: {mood}")
        return [{'message': f'No movies found for mood: {mood}'}]
    
    # Print filtered movies for debugging
    print("Filtered Movies for Mood:", filtered_movies[['title', 'genres']])
    
    # Return a list of movies that match the mood
    return filtered_movies[['title', 'genres', 'overview']].to_dict(orient='records')

# Route to get movie recommendation based on mood
@app.route('/recommend', methods=['POST'])
def recommend_movie():
    data = request.json
    mood = data.get('mood')
    print("Received mood:", mood)
    
    if not mood:
        return jsonify({'error': 'Please provide a mood'}), 400
    
    recommended_movies = recommend_movies_by_mood(mood)
    return jsonify({'mood': mood, 'movies': recommended_movies})

if __name__ == '__main__':
    app.run(debug=False)

# # lkjhgfdsawertyuiokmnbvcx
