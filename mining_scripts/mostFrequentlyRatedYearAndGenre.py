  # Prints most-least frequently rated genre and year.


def experimentsOnMovies(frequentItemsetsDict):  # using UserBaskets.

    quintupleList = []  # list of 5-tuples
    df = ReadMovies('movies.csv')

    for key, value in frequentItemsetsDict.items():
        if value >= 140 :
            if type(key) is tuple and len(key) == 5:
                quintupleList.append(key)

    createCSV2("quintuples.csv", quintupleList)

    yearList = []
    genreList = []
    for i in quintupleList:
        auxYearList = []
        hashTable = {}
        for j in i:
            auxYearList.append(df.loc[j-1, "title"][-5:-1])
            for k in df.loc[j-1, "genres"].split("|"):
                if k not in hashTable:
                    hashTable[k] = 1
                else:
                    hashTable[k] += 1

        genreList.append(max(hashTable, key=hashTable.get))
        yearList.append(auxYearList)

    flatYearList = list(chain(*yearList))

    hashTable = {}
    for i in genreList:
        if i not in hashTable:
            hashTable[i] = 1
        else:
            hashTable[i] += 1
    x = (max(hashTable, key = hashTable.get))

    hashTable = {}
    for i in flatYearList:
        if i not in hashTable:
            hashTable[i] = 1
        else:
            hashTable[i] += 1
    y = (max(hashTable, key = hashTable.get))

    createCSV2("moviesExperimentGenreList.csv", genreList)
    createCSV2("moviesExperimentYearList.csv", yearList)
    print("Most common genre amongst the quintuples is:", x)
    print("Most common year of release amongst the quintuples is:", y)


if __name__ == "__main__":
    experimentsOnMovies(myAprioriHash(CreateUserBaskets(ReadRatings('ratings.csv')), 140, 5))
