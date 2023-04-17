import pandas as pd
from statistics import mean, median
from collections import Counter
import matplotlib.pyplot as plt

movies_raw = pd.read_csv("movies.csv")

# Get the mean movie budget
print(f"The average movie budget is ${round(mean(movies_raw['budget']))}")

# Get the most common movie genres

junk_chars = ['"', "}", "]"]

genre_list = []

# Breakup genres from raw data
for i in movies_raw['genres']:
  x = i.split("},")
  for j in x:
    split = j.partition('name":')[2]
    for junk_char in junk_chars:
      split = split.replace(junk_char, "")
    genre_list.append(split.strip())

a = Counter(genre_list)
print(f"\nThe most common genres are {a.most_common(5)}")

# Get the median movie runtime
runtimes = []
# Get each movie runtime and convert to int
for x in movies_raw['runtime']:
  try:
    runtimes.append(int(x))
  except ValueError:
    True

print(f"\nThe median runtime is {median(runtimes)} minutes")

# Top 10 Rated Movies
# Creates a dictionary of title:rating 
movie_with_rating = {
  movies_raw['title'][i]: movies_raw['vote_average'][i]
  for i in range(len(movies_raw['title']))
}
movie_with_rating = {
  k: v
  for k, v in sorted(
    movie_with_rating.items(), key=lambda item: item[1], reverse=True)
}

print(f"\nThe top 10 movies by rating are {list(movie_with_rating.items())[12:22]}")

# Graphing
genres = [a.most_common(5)[x][0] for x in range(5)]
occurences = [a.most_common(5)[x][1] for x in range(5)]

plt.bar(genres, occurences)
plt.title("Genres by Occurence")
plt.xlabel("Genres")
plt.ylabel("Number of Occurences")

plt.show()
