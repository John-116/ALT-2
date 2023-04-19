import pandas as pd
import lib

print(
    """
  __  __            _        ___                                            _           
 |  \/  | ___ __ __(_) ___  | _ \ ___  __  ___  _ __   _ __   ___  _ _   __| | ___  _ _ 
 | |\/| |/ _ \\ V /| |/ -_) |   // -_)/ _|/ _ \| '  \ | '  \ / -_)| ' \ / _` |/ -_)| '_|
 |_|  |_|\___/ \_/ |_|\___| |_|_\\___|\__|\___/|_|_|_||_|_|_|\___||_||_|\__,_|\___||_|  
                                                                                        
by John Denny and Vishrut Srinivasa
"""
)
rating_file = input("Please enter name of your rating file: ")

# Check if user file exists
try:
    user_raw = pd.read_csv(rating_file)
except FileNotFoundError:
    exit("File Does Not Exist. Please ensure you are entering a valid file")

# Open Movie Database
movies_raw = pd.read_csv("movies.csv")

junk_chars = ['"', "}", "]"]


def Get_Genres(index):
    # Convert the raw genres to a useable list
    genres = []
    genres_raw = movies_raw["genres"][index].split("},")
    for i in genres_raw:

        split = i.partition('name":')[2]
        for y in junk_chars:
            split = split.replace(y, "")
        genres.append(split.strip())
    return genres


def Get_Tags(index):
    tags_raw = movies_raw["keywords"][index].split("},")

    tags = [i.partition('name": ')[2] for i in tags_raw]
    tags[-1] = tags[-1][
        :-2
    ]  # Remove the last 2 characters of the last tag as it is always }]
    tags = [i.replace('"', "") for i in tags]  # Remove Quotations
    return tags


movie_with_genre = {
    movies_raw["original_title"][i]: Get_Genres(i) for i in range(len(movies_raw))
}

movie_with_tag = {
    movies_raw["original_title"][i]: Get_Tags(i) for i in range(len(movies_raw))
}

# Dict with {Movie A user has watched: Rating the user gave that movie}
user_movies_with_rating = {
    user_raw["Title"][i]: user_raw["Rating"][i] for i in range(len(user_raw))
}

# Get a List of all genres that the user watched
total_user_genres = []
for k, v in user_movies_with_rating.items():
    total_user_genres += movie_with_genre[k]
user_genres = list(set(total_user_genres))

# Get a List of all tags the user watched
total_user_tags = []
for i in movie_with_tag.keys():
    total_user_tags += movie_with_tag[i]
user_tags = list(set(total_user_tags))

# Make a dict where
# {genre_name : [score,number of scores added]}
genre_scores_raw = {k: [0, 0] for k in user_genres}
# {tag: [score, number of scores added]}
tag_scores_raw = {k: [0, 0] for k in user_tags}

# Score Each Genre
for i in user_movies_with_rating:
    for x in movie_with_genre[i]:
        genre_scores_raw[x][0] += user_movies_with_rating[i]
        genre_scores_raw[x][1] += 1

# Score each tag
for i in user_movies_with_rating:
    for x in movie_with_tag[i]:
        tag_scores_raw[x][0] += user_movies_with_rating[i]
        tag_scores_raw[x][1] += 1

# Average the scores
genre_scores = {k: v[0] / v[1] for k, v in genre_scores_raw.items()}
tag_scores = {k: v[0] / max([v[1], 1]) for k, v in tag_scores_raw.items()}
# Sorts the genres and tags from highest rating to lowest rating
genre_scores = {
    k: v for k, v in sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
}
tag_scores = {
    k: v for k, v in sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
}

# Prints all movies where top 3 genres are present
movies_with_top_3_genres = lib.recommendByGenre(list(genre_scores.keys())[:3])


def score_movie(movie_name):
    # Get the genres
    try:
        genres_of_current_movie = movie_with_genre[movie_name]
    except KeyError:
        return 0

    num_of_genres_scorable = 0
    genre_score = 0

    # Get the tags
    tags_of_current_movie = movie_with_tag[movie_name]
    num_of_tags_scorable = 0
    current_tags_score = 0

    # If a movie has a common genre or score increase it's score by its associated amount
    for i in genres_of_current_movie:
        if i in user_genres:
            genre_score += genre_scores[i]
            num_of_genres_scorable += 1

    for i in tags_of_current_movie:
        if i in user_tags:
            current_tags_score += tag_scores[i]
            num_of_tags_scorable += 1

    # Final Score Average Genre Score + 0.5 Average Tag Score
    final_score = (genre_score / num_of_genres_scorable) + (
        current_tags_score / num_of_tags_scorable
    ) / 2
    return final_score


# Score all movies with top 5 genres
movie_scored_unsorted = {k: score_movie(k) for k in movies_with_top_3_genres}

recList = {
    k: v
    for k, v in sorted(movie_scored_unsorted.items(), key=lambda x: x[1], reverse=True)
}

recList = {k: v for k, v in recList.items() if k not in user_movies_with_rating.keys()}

# Output Recommendations
top_5_recommendations = list(recList.keys())[:5]

print("Recommendations\n")
for i in top_5_recommendations:
    print(i)
    overview = movies_raw["overview"][(list(movies_raw["original_title"]).index(i))]
    print(f"Overview:\n{overview}\n\n")
