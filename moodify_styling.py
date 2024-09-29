st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
    }

    /* Target the Streamlit main content container */
    .main {
        background: linear-gradient(270deg, #ff6f61, #d3e0ea, #00c9ff, #ff6f61);
        background-size: 800% 800%;
        animation: gradientAnimation 12s ease infinite;
        height: 100vh;
        width: 100vw;
        position: absolute;
        top: 0;
        left: 0;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0;
    }

    h2 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 2em;
        text-align: center;
        margin-top: 0;
    }

    </style>

    <div>
        <h1>Howdy!</h1>
        <h2>Welcome to Moodify</h2>
        <h2>Let your mood drive Spotify</h2>
    </div>
    """,
    unsafe_allow_html=True,
)