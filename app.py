from datetime import date
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize API clients
OMDB_API_URL = "https://www.omdbapi.com/"
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "3d1cb94d909aab088231f5af899dffdc")
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Debug information
if not OMDB_API_KEY:
    st.error("OMDB API key not found in environment variables")
if not os.getenv("GROQ_API_KEY"):
    st.error("Groq API key not found in environment variables")

def get_movie_suggestions(genre, year, num_suggestions, content_type="movie"):
    """Get movie or series suggestions from OMDB API"""
    params = {
        "s": genre,
        "y": year if year else "",
        "apikey": OMDB_API_KEY,
        "type": content_type
    }
    
    try:
        # Using session for better connection handling
        session = requests.Session()
        response = session.get(OMDB_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data["Search"][:int(num_suggestions)]
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching movies: {str(e)}")
        return []

def get_content_details(imdb_id):
    """Get detailed information about a movie or series"""
    params = {
        "i": imdb_id,
        "apikey": OMDB_API_KEY
    }
    
    try:
        # Using session for better connection handling
        session = requests.Session()
        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                response = session.get(OMDB_API_URL, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.Timeout:
                if attempt == retries - 1:  # Last attempt
                    raise
                continue
    except Exception as e:
        st.error(f"Error fetching movie details: {str(e)}")
        return {
            "Title": "Error loading details",
            "Plot": "Unable to load movie details",
            "Poster": "",
            "imdbRating": "N/A",
            "Actors": "Not available"
        }

def process_query_with_llama(query, context=""):
    """Process user query using Groq's LLaMA model"""
    system_prompt = """You are a knowledgeable movie and TV series recommendation chatbot. 
    Use the provided context about movies/shows to give personalized recommendations. 
    Be friendly and conversational while providing specific, relevant suggestions."""
    
    user_message = f"Context: {context}\nUser Query: {query}"
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Using the correct model name for Groq - llama-3.3-70b-versatile
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error with AI response: {str(e)}")
        return "I apologize, but I'm having trouble accessing the AI model right now. You can still search for movies using the Quick Search tab!"

def get_tmdb_data_by_imdb_id(imdb_id):
    """Get movie data from TMDB using IMDb ID"""
    try:
        url = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id'
        session = requests.Session()
        retries = 3
        last_error = None
        
        for attempt in range(retries):
            try:
                response = session.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()
                if data.get('movie_results'):
                    return data['movie_results'][0]
                elif data.get('tv_results'):
                    return data['tv_results'][0]
                return None
            except (requests.Timeout, requests.RequestException) as e:
                last_error = e
                if attempt == retries - 1:
                    break
                continue
                
        if last_error:
            st.error(f"Error fetching TMDB data after {retries} attempts: {str(last_error)}")
        return None
    except Exception as e:
        st.error(f"Error fetching TMDB data: {str(e)}")
        return None

def get_poster_url(imdb_id):
    """Get poster URL from TMDB"""
    movie_data = get_tmdb_data_by_imdb_id(imdb_id)
    if movie_data and movie_data.get('poster_path'):
        return f"{TMDB_IMAGE_BASE}{movie_data['poster_path']}"
    return None

def filter_by_rating(movies, rating_filter):
    """Filter movies based on IMDb rating ranges"""
    if not rating_filter or rating_filter == "All":
        return movies
    
    filtered_movies = []
    for movie in movies:
        details = get_content_details(movie['imdbID'])
        rating = float(details.get('imdbRating', '0')) if details.get('imdbRating', 'N/A') != 'N/A' else 0
        
        if rating_filter == "Top Rated" and rating >= 8.0:
            filtered_movies.append(movie)
        elif rating_filter == "Good" and 6.5 <= rating < 8.0:
            filtered_movies.append(movie)
        elif rating_filter == "Average" and 5.0 <= rating < 6.5:
            filtered_movies.append(movie)
        elif rating_filter == "Low Rated" and rating < 5.0:
            filtered_movies.append(movie)
            
    return filtered_movies

def get_llm_movie_suggestions(content_type, genre, suggestion_type, num_suggestions, rating_filter, year, industry):
    """Get movie suggestions using LLM based on user parameters"""
    system_prompt = """You are a knowledgeable movie and TV series expert. Based on the given parameters, 
    suggest relevant titles from specific film industries. Only provide the exact titles without any additional text or explanation.
    For Bollywood, suggest Hindi movies; for Hollywood, suggest American/English movies; for Tollywood, suggest Telugu movies.
    When given a year range, suggest titles released during that period.
    Provide one title per line."""
    
    user_message = f"""Suggest {num_suggestions} {content_type}s with these criteria:
    - Genre: {genre}
    - Release Period: {year}
    - Type: {suggestion_type}
    - Rating category: {rating_filter}
    - Industry: {industry}
    
    Format: Only provide the exact titles, one per line. No additional text."""
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        # Split the response into individual titles
        suggested_titles = completion.choices[0].message.content.strip().split('\n')
        return [title.strip() for title in suggested_titles if title.strip()]
    except Exception as e:
        st.error(f"Error getting AI suggestions: {str(e)}")
        return []

def search_movie_by_title(title, content_type="movie"):
    """Search for a specific movie/series by title in OMDB"""
    params = {
        "t": title,  # Search by title
        "apikey": OMDB_API_KEY,
        "type": content_type
    }
    
    try:
        session = requests.Session()
        response = session.get(OMDB_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data
        return None
    except Exception as e:
        st.error(f"Error searching for {title}: {str(e)}")
        return None

def main():
    st.title("🎬 Movie/Series Recommendation Chatbot")
    st.write("Get personalized movie and TV series recommendations!")

    # Add tabs for different search options
    tab1, tab2 = st.tabs(["Quick Search", "Chat with AI"])

    with tab1:
        # Create three columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            content_type = st.selectbox("What are you looking for?", ["movie", "series"])
            industry = st.selectbox("Select Industry:", [
                "Hollywood", "Bollywood", "Tollywood", "Korean", "International", "Gujarati"
            ])
            genre = st.text_input("Enter genre (e.g., Action, Comedy, Drama):")
        
        with col2:
            suggestion_type = st.selectbox("Select suggestion type:", ["Any", "Random", "Top Rated", "Good", "Average", "Low Rated"])
            num_suggestions = st.number_input("Number of suggestions:", min_value=1, max_value=10, value=5)
            rating_filter = st.selectbox("Select IMDb rating range:", ["All", "Top Rated", "Good", "Average", "Low Rated"])

        # Year range selector
        start_year, end_year = st.slider(
            "Select year range:",
            min_value=1950,
            max_value=date.today().year,
            value=(2000, date.today().year),  # Default range from 2000 to present
            step=1
        )
        st.write(f"Selected period: {start_year} to {end_year}")

        if st.button("🔍 Search"):
            if genre:
                with st.spinner("Getting AI recommendations..."):
                    # First, get movie suggestions from LLM
                    suggested_titles = get_llm_movie_suggestions(
                        content_type=content_type,
                        genre=genre,
                        suggestion_type=suggestion_type,
                        num_suggestions=num_suggestions,
                        rating_filter=rating_filter,
                        year=f"{start_year}-{end_year}",  # Pass year range
                        industry=industry
                    )
                    
                    if suggested_titles:
                        st.subheader("Here's what I found:")
                        for title in suggested_titles:
                            with st.spinner(f"Fetching details for {title}..."):
                                movie_data = search_movie_by_title(title, content_type)
                                if movie_data:
                                    with st.expander(f"**{movie_data['Title']}** ({movie_data.get('Year', 'N/A')})"):
                                        col1, col2 = st.columns([1, 3])
                                        with col1:
                                            imdb_id = movie_data['imdbID']
                                            poster_url = get_poster_url(imdb_id)
                                            if poster_url:
                                                st.image(poster_url, use_column_width=True)
                                            else:
                                                st.write("🎬 No poster available")
                                        with col2:
                                            st.write(f"**Plot:** {movie_data.get('Plot', 'Not available')}")
                                            st.write(f"**Rating:** ⭐ {movie_data.get('imdbRating', 'N/A')}/10")
                                            st.write(f"**Cast:** {movie_data.get('Actors', 'Not available')}")
                                            st.write(f"**Director:** {movie_data.get('Director', 'Not available')}")
                                            st.write(f"**Genre:** {movie_data.get('Genre', 'Not available')}")
                                            st.write(f"**Language:** {movie_data.get('Language', 'Not available')}")
                                            st.write(f"**Country:** {movie_data.get('Country', 'Not available')}")
                                            st.write(f"**Awards:** {movie_data.get('Awards', 'Not available')}")
                                            imdb_url = f"https://www.imdb.com/title/{movie_data['imdbID']}/"
                                            st.markdown(f"[View on IMDb]({imdb_url})")
                    else:
                        st.warning("No suggestions found. Try different search terms.")
            else:
                st.warning("Please enter a genre.")

    with tab2:
        st.write("Chat with our AI to get personalized recommendations!")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask for movie/series recommendations..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = process_query_with_llama(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
