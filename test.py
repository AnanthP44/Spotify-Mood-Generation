import streamlit as st

# Function to display a Spotify embed, centered in a grid


def spotify_embed(embed_urls):
    spotify_html = '<div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 20px;">'
    
    for url in embed_urls:
        spotify_html += f"""
        <div style="flex: 1 1 300px; max-width: 300px;">
            <iframe src="{url}" width="300" height="380" frameborder="0" 
            allowtransparency="true" allow="encrypted-media"></iframe>
        </div>
        """
    
    spotify_html += '</div>'
    
    st.components.v1.html(spotify_html, height=800)



# List of Spotify embed URLs for 5 songs 
spotify_track_urls = [
    "https://open.spotify.com/embed/track/3n3Ppam7vgaVa1iaRUc9Lp",
    "https://open.spotify.com/embed/track/2RttW7RAu5nOAfq6YFvApB", #change these urls and make if statemetns 
    "https://open.spotify.com/embed/track/0VjIjW4GlUZAMYd2vXMi3b",
    "https://open.spotify.com/embed/track/7qiZfU4dY1lWllzX7mPBI3"
]

# Display the centered Spotify embeds for all 4 songs
spotify_embed(spotify_track_urls)
