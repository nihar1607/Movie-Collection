
import streamlit as st
import pandas as pd
import html

from database import (
    create_table,
    add_movie,
    get_movies,
    get_total_movies,
    get_average_rating,
    get_highest_rated_movie,
    get_genre_summary
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="CineVault | Movie Collection",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #090909;
    color: #ffffff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: #111111;
    border-right: 1px solid #292929;
}

section[data-testid="stSidebar"] h1 {
    color: #e50914;
    font-weight: 900;
    letter-spacing: -1px;
}

section[data-testid="stSidebar"] p {
    color: #aaaaaa;
}

h1, h2, h3 {
    color: white !important;
    font-weight: 800 !important;
}

p, label {
    color: #cccccc;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #e50914;
    color: white;
    border: none;
    border-radius: 7px;
    font-weight: 700;
    padding: 0.65rem 1.2rem;
    transition: 0.2s;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #b20710;
    color: white;
    border: none;
    transform: scale(1.02);
}

div[data-testid="stMetric"] {
    background: #181818;
    border: 1px solid #292929;
    border-radius: 12px;
    padding: 20px;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 800;
}

div[data-testid="stMetricLabel"] {
    color: #aaaaaa;
}

input, textarea {
    background-color: #202020 !important;
    color: white !important;
}

div[data-baseweb="select"] > div {
    background: #202020;
    color: white;
}

hr {
    border-color: #333333;
}

.poster-card {
    background: linear-gradient(145deg, #292929, #151515);
    border: 1px solid #333333;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.25s, border 0.25s;
    height: 100%;
}

.poster-card:hover {
    transform: translateY(-7px);
    border: 1px solid #e50914;
}

.poster-art {
    height: 155px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 55px;
    background: linear-gradient(135deg, #481014, #171717);
}

.poster-info {
    padding: 13px;
}

.poster-title {
    color: white;
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 7px;
    min-height: 36px;
}

.poster-meta {
    color: #aaaaaa;
    font-size: 12px;
    margin-bottom: 7px;
}

.rating {
    color: #ffc107;
    font-size: 13px;
    font-weight: 700;
}

.hero {
    background:
        linear-gradient(90deg, #090909 0%, rgba(9,9,9,.92) 35%, rgba(9,9,9,.2) 100%),
        linear-gradient(0deg, #090909, transparent 65%),
        linear-gradient(135deg, #63151b, #202020 65%, #101010);
    border-radius: 18px;
    padding: 55px 45px;
    min-height: 290px;
    border: 1px solid #333333;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-tag {
    color: #e50914;
    font-weight: 900;
    letter-spacing: 3px;
    font-size: 12px;
}

.hero-title {
    color: white;
    font-size: 42px;
    font-weight: 900;
    margin-top: 10px;
}

.hero-description {
    color: #dddddd;
    font-size: 14px;
    max-width: 570px;
}

.section-label {
    color: #e50914;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 2px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #333333;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HELPER FUNCTIONS ----------------

GENRE_EMOJI = {
    "Action": "💥",
    "Comedy": "😂",
    "Drama": "🎭",
    "Thriller": "🔪",
    "Science Fiction": "🚀",
    "Romance": "❤️",
    "Horror": "👻",
    "Adventure": "🌍",
    "Animation": "🎨",
    "Documentary": "🎥",
    "Other": "🎬"
}

def safe(value):
    return html.escape(str(value))


def movie_card(movie):
    movie_id, name, genre, rating, year = movie

    emoji = GENRE_EMOJI.get(genre, "🎬")

    st.markdown(f"""
    <div class="poster-card">
        <div class="poster-art">{emoji}</div>
        <div class="poster-info">
            <div class="poster-title">{safe(name)}</div>
            <div class="poster-meta">
                {safe(genre)} &nbsp; • &nbsp; {year}
            </div>
            <div class="rating">
                ★ {rating:.1f}/10
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def movie_section(movies):
    if not movies:
        st.info("No movies found. Add your first movie!")
        return

    for start in range(0, len(movies), 4):
        group = movies[start:start + 4]
        columns = st.columns(4)

        for col, movie in zip(columns, group):
            with col:
                movie_card(movie)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown(
    "<h1>🎬 CINEVAULT</h1>",
    unsafe_allow_html=True
)

st.sidebar.caption("YOUR PERSONAL CINEMA")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "EXPLORE",
    [
        "Home",
        "Add Movie",
        "My Collection",
        "Statistics"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="color:#777;font-size:12px;">
    CINEVAULT<br>
    Your movies. Your collection.<br><br>
    Powered by Python & SQLite
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- HOME PAGE ----------------

if page == "Home":

    movies = get_movies()

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">WELCOME TO CINEVAULT</div>
        <div class="hero-title">Your Cinema.<br> Your Collection.</div>
        <div class="hero-description">
            Discover, organize and manage your favourite movies
            in one beautiful place.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="section-label">YOUR LIBRARY</div>',
                unsafe_allow_html=True)

    st.title("Collection Overview")

    total = get_total_movies()
    average = get_average_rating()
    highest = get_highest_rated_movie()

    c1, c2, c3 = st.columns(3)

    c1.metric("🎬 Total Movies", total)
    c2.metric("⭐ Average Rating", f"{average:.1f}/10")

    if highest:
        c3.metric("🏆 Top Movie", f"{highest[3]:.1f}/10")
    else:
        c3.metric("🏆 Top Movie", "N/A")

    st.write("")

    if highest:
        st.markdown("### 🏆 Featured Movie")

        st.markdown(f"""
        <div style="
            background:linear-gradient(110deg,#401015,#181818);
            border:1px solid #4b292b;
            border-radius:14px;
            padding:25px;
        ">
            <div style="color:#e50914;font-size:12px;
            font-weight:900;letter-spacing:2px;">
                TOP RATED IN YOUR COLLECTION
            </div>
            <h2>{safe(highest[1])}</h2>
            <p style="color:#bbbbbb;">
                {safe(highest[2])} &nbsp; • &nbsp; {highest[4]}
            </p>
            <h3 style="color:#ffc107 !important;">
                ★ {highest[3]:.1f}/10
            </h3>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("### 🔥 Recently Added")

    if movies:
        movie_section(movies[:8])
    else:
        st.info("Your collection is empty. Start adding movies!")


# ---------------- ADD MOVIE PAGE ----------------

elif page == "Add Movie":

    st.markdown('<div class="section-label">BUILD YOUR LIBRARY</div>',
                unsafe_allow_html=True)

    st.title("➕ Add a Movie")

    st.write("Add a new title to your personal cinema collection.")

    st.write("")

    with st.container(border=True):

        with st.form("add_movie_form"):

            movie_name = st.text_input(
                "Movie Name",
                placeholder="Enter movie title..."
            )

            col1, col2 = st.columns(2)

            with col1:
                genre = st.selectbox(
                    "Genre",
                    list(GENRE_EMOJI.keys())
                )

            with col2:
                release_year = st.number_input(
                    "Release Year",
                    min_value=1888,
                    max_value=2100,
                    value=2020
                )

            rating = st.slider(
                "Your Movie Rating",
                min_value=0.0,
                max_value=10.0,
                value=7.0,
                step=0.1
            )

            submitted = st.form_submit_button(
                "＋ Add to My Collection",
                use_container_width=True
            )

            if submitted:
                if movie_name.strip():

                    add_movie(
                        movie_name.strip(),
                        genre,
                        rating,
                        int(release_year)
                    )

                    st.success(
                        f"🎉 {movie_name} added to your collection!"
                    )

                else:
                    st.error("Please enter a movie name.")


# ---------------- MY COLLECTION PAGE ----------------

elif page == "My Collection":

    st.markdown('<div class="section-label">EXPLORE YOUR LIBRARY</div>',
                unsafe_allow_html=True)

    st.title("🎞️ My Collection")

    movies = get_movies()

    if movies:

        col1, col2 = st.columns([2, 1])

        with col1:
            search = st.text_input(
                "🔍 Search movies",
                placeholder="Search by movie name..."
            )

        with col2:
            genres = ["All"] + sorted(
                set(movie[2] for movie in movies)
            )

            selected_genre = st.selectbox(
                "Filter by Genre",
                genres
            )

        filtered = movies

        if search:
            filtered = [
                movie for movie in filtered
                if search.lower() in movie[1].lower()
            ]

        if selected_genre != "All":
            filtered = [
                movie for movie in filtered
                if movie[2] == selected_genre
            ]

        st.caption(f"{len(filtered)} movies found")

        st.divider()

        movie_section(filtered)

    else:
        st.info("Your collection is empty. Add your first movie!")


# ---------------- STATISTICS PAGE ----------------

elif page == "Statistics":

    st.markdown('<div class="section-label">COLLECTION INSIGHTS</div>',
                unsafe_allow_html=True)

    st.title("📊 Your Movie Analytics")

    movies = get_movies()
    summary = get_genre_summary()

    if movies:

        total = get_total_movies()
        average = get_average_rating()

        col1, col2 = st.columns(2)

        col1.metric("Total Movies", total)
        col2.metric("Average Rating", f"{average:.2f}/10")

        st.divider()

        st.subheader("🎭 Genre Distribution")

        df = pd.DataFrame(
            summary,
            columns=["Genre", "Movie Count"]
        )

        st.bar_chart(
            df.set_index("Genre"),
            color="#E50914"
        )

        st.subheader("📋 Genre-wise Summary")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("⭐ Movie Ratings")

        rating_df = pd.DataFrame(
            [
                {
                    "Movie": movie[1],
                    "Rating": movie[3]
                }
                for movie in movies
            ]
        )

        st.bar_chart(
            rating_df.set_index("Movie"),
            color="#E50914"
        )

    else:
        st.info("Add movies to view your collection analytics.")


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#666;font-size:12px;">
        🎬 CINEVAULT | YOUR PERSONAL MOVIE COLLECTION
        <br><br>
        Built with Python • Streamlit • SQLite
    </div>
    """,
    unsafe_allow_html=True
)
