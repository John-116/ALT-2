import numpy as np
import pandas as pd


# Making a dict with the name(str) as the key and the genres(list) as the value
df = pd.read_csv("movies.csv")  # reading the excel file and turning it into a dataframe
titleList = df["title"].to_list()  # turning the data under the column "title" to a list
genreList = df["genres"].to_list()  # ^^^ same as above, but column ---> "genres"


globalList = []  # making a list
genreTypes = []  # ^^^ same
for i in genreList:  # iterating through every element of the genreList
    i: str = i.replace("]", "").replace(
        "}", ""
    )  # data-cleaning as we do not need the closing brackets as they affect the
    myList: list = i.split(
        ","
    )  # spliting the list wherever there is a "," and making it into a list
    myList = [
        myList[i] for i in range(len(myList)) if i % 2
    ]  # We only keep the odd indexed elements as they have the genre name, the even indexed elements have genre id
    localList = []  # making a new list
    for i in myList:  # iterating through myList
        word = i[9:].replace(
            '"', ""
        )  # subslicing the string from the 9th element onwards and replacing the "\'\" as it will affect how it is stored in the list as a string, "example" & "'example" ---> more harder to read and access
        if word not in genreTypes:
            genreTypes.append(word)
        localList.append(word)  # append the word to localList
    globalList.append(localList)  # appending the localList to the globalList
titleGenreDict = {
    k: v for k, v in zip(titleList, globalList)
}  # creating a dict with dictionary comphrehension, we first use the zip function to merge the titleList & the globalList
# this means we have an iterator, where every element is a tuple, with the first element of the tuple being the movie name, and the second element being a list of its genres
# it uses the first element (name) to make a key and the second element (list of genres) to make a value ---> this makes a dictionary


def commonGenres(genre: str):  # making a function
    commonList = []
    for (
        i
    ) in (
        titleGenreDict.items()
    ):  # iterates throughout the items of the dict ---> tuple ---> (key, values)
        if (
            genre in i[1]
        ):  # if the wanted genre is in the 2nd element --> list of genres that movie has
            commonList.append(
                i[0]
            )  # it appends the name of the movie to the list ---> first element
    return commonList  # returns the list


moviesDict = {}
for i in genreTypes:  # iterating through every element in the list (genreTypes)
    moviesDict[i] = commonGenres(
        i
    )  # making the element the key and assigning the value as the list the function commonGenres returns


def recommendByGenre(genres: list[str]):
    myList1 = np.array([moviesDict[genres.pop()]])
    for i in genres:
        mList = moviesDict[i]
        myList1 = np.intersect1d(myList1, mList)
    return list(myList1)


def recommendByMovie(name: str):
    genres = titleGenreDict[name]
    return recommendByGenre(genres)


"""newDF = pd.read_csv("user_in.csv")
name = newDF["Title"].to_list()
ratings = newDf["Rating"].to_list()
newDict = {}"""
