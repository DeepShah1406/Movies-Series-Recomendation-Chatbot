# 🎬 Movie/Series Recommendation Chatbot

An AI-powered Streamlit chatbot that recommends movies and TV series based on user preferences using a Large Language Model (LLM), OMDb API, and TMDb API.

---

## 📌 Project Overview

The **Movie/Series Recommendation Chatbot** allows users to get personalized movie or series suggestions by interacting with an intelligent chatbot interface. It uses a powerful LLM (Groq’s **LLaMA-3.3-70B**) to understand natural language queries and generate relevant movie titles. It then fetches detailed movie metadata using **OMDb** and **TMDb APIs**.

---

## 🚀 Features

- 🔍 **Two Recommendation Modes**:

  - **Quick Search**: Uses structured filters (genre, rating, year range, industry).
  - **Chat with AI**: Free-form conversation using LLM to generate suggestions.

- 🎥 **LLM-Based Title Suggestions**:  
  Understands complex user queries like “10 action movies starring Tom Cruise or RDJ”.

- 🧠 **Groq LLaMA-3.3-70B Integration**:  
  High-performance, low-latency LLM used via Groq API.

- 🗃️ **OMDb + TMDb API Integration**:  
  Fetches rich metadata: plot, actors, genre, IMDB rating, country, posters, and more.

- 📊 **Rating-Based Filtering**:  
  Dynamically filter content by IMDb ratings (Top Rated, Good, Average, Low Rated).

- 🏷️ **Multilingual & Regional Content**:  
  Includes Bollywood, Hollywood, Tollywood, Korean, Gujarati, and International cinema.

- 🖼️ **Poster Fetching from TMDb**:  
  Dynamically fetches and displays movie/series posters using TMDb API and IMDb ID.

---

## 🛠️ Tech Stack

| Component        | Technology                         |
| ---------------- | ---------------------------------- |
| Programming      | Python 3.13.3                      |
| Frontend         | Streamlit 1.38.0                   |
| LLM Integration  | Groq API using LLaMA-3.3-70B       |
| Movie Metadata   | OMDb API, TMDb API                 |
| Environment Vars | `python-dotenv`                    |
| HTTP Requests    | `requests`, with session + retries |

---

## ⚙️ Setup Instructions

### 📁 Clone the repository

```bash
git clone https://github.com/yourusername/Movie-Series-Recommendation-Chatbot.git
cd Movie-Series-Recommendation-Chatbot
```

### 🧪 Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, manually install:

```bash
pip install streamlit requests python-dotenv
```

### 🔐 Set environment variables

Create a `.env` file in the root folder:

```
OMDB_API_KEY=your_omdb_api_key
TMDB_API_KEY=your_tmdb_api_key
GROQ_API_KEY=your_groq_api_key
```

> ℹ️ You can obtain a free OMDb API key at: [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)
> TMDb API: [https://developer.themoviedb.org/](https://developer.themoviedb.org/)
> Groq API: [https://console.groq.com/](https://console.groq.com/)

---

## ▶️ Run the App

```bash
streamlit run main.py
```

Then visit: [http://localhost:8501](http://localhost:8501)

---

## 💡 How It Works

1. **User Inputs**:

   - Genre, Industry, Year Range, Suggestion Type (Quick Search tab)
   - OR free-form query in “Chat with AI” tab

2. **LLM Processing**:

   - Uses Groq's LLaMA model to understand input and generate movie titles

3. **Metadata Lookup**:

   - OMDb is queried by title/ID for movie details
   - TMDb is queried by IMDb ID for poster and fallback data

4. **Display**:

   - Posters, plots, actors, ratings, IMDb links are presented using Streamlit UI

---

## 🎯 Sample Queries (Chat Tab)

- “Suggest 5 action movies starring Tom Cruise.”
- “Give me 3 good Hindi romantic dramas from the 2000s.”
- “Recommend Oscer winning Japanese anime movies released after 2001.”

---

## 📈 Future Improvements

- 🧠 **Conversational Memory**: Retain session context for better follow-ups.
- 🧩 **More Streaming APIs**: Integrate Netflix, Prime Video, Disney+.
- 🌍 **Multilingual Expansion**: Support for regional languages.
- 🧾 **User Feedback**: Like/dislike to improve future suggestions.
- 🛰️ **Cloud Deployment**: Host on HuggingFace Spaces, Streamlit Cloud, or Render.

---

## 🧪 Project Structure (Simplified)

```
📁 Movie-Series-Recommendation-Chatbot
├── main.py                 # Streamlit app entry point
├── .env                    # Environment variable file
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## 🪪 License

This project is licensed under the [MIT License](https://github.com/DeepShah1406/Movies-Series-Recomendation-Chatbot/blob/main/LICENSE).

---

## 📬 Contact

- 📧 Email: [shahdeep1406@gmail.com](mailto:shahdeep1406@gmail.com)
- 🐙 GitHub: [DeepShah1406](https://github.com/DeepShah1406)
- 💼 LinkedIn: [deepshah1406](https://www.linkedin.com/in/deepshah1406)

---

## 🙏 Acknowledgments

- [Groq](https://groq.com) for blazing fast LLaMA API
- [OMDb API](https://www.omdbapi.com) for movie/series data
- [TMDb API](https://developer.themoviedb.org/) for posters and metadata
- [Streamlit](https://streamlit.io) for building interactive web UIs
