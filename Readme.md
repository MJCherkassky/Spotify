# Background

For this project, I attempt to extract my own user data using Spotify's API. This is a project in several parts:
    
    1. Create an application that reads my "recently played" items on Spotify. The application stores the following data:
        a. Title
        b. Artist
        c. Genre
        d. playback time
        e. album art url
        f. Track Spotify ID
        g. Artist Spotify ID
    
    2. Creates a new playlist based on the top song from artists "related to" (similar genre, music style, collaborations, etc) the artist on your recently played, and compiles all spotify ID's to create and save a new playlist on my iPhone Spotify app.

    3. Save all stored data to a SQL database using SQLAlchemy and PostgreSQL
    
    4. Understand my own listening habits by connecting Tableau dashboard to my PostgreSQL db

    5. Find a way to quantify whether or not Spotify is actually any good at recommending music for me.

