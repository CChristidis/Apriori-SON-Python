  # Prints the highest and lowest rated movies

def experimentsOnMovies(frequentItemsetsDict):  # using UserBaskets.

    quintupleList = []  # list of 5-tuples
    df1 = ReadMovies('movies.csv')
    df2 = ReadRatings('ratings.csv')

    for key, value in frequentItemsetsDict.items():
        if value >= 140:
            if type(key) is tuple and len(key) == 5:
                quintupleList.append(key)

    #createCSV2("quintuples.csv", quintupleList)

    ratingsList = []
    for i in quintupleList:
        auxRatingsList = []
        hashTable = {}
        for j in i:
            mean = 0
            sum  = 0
            l = len(df2.loc[df2["movieId"] == j])
            #auxRatingsList.append(df2.loc[j - 1, "title"][-5:-1])
            for k in df2.loc[df2["movieId"] == j, "rating"]:
                sum += k
            mean = float(sum/l)
            auxRatingsList.append(mean)
        ratingsList.append(auxRatingsList)

    flatRatingsList = list(chain(*ratingsList))

    x = max(flatRatingsList)
    y = min(flatRatingsList)

    for i in quintupleList:
        for j in i:
            mean = 0
            sum = 0
            l = len(df2.loc[df2["movieId"] == j])
            for k in df2.loc[df2["movieId"] == j, "rating"]:
                sum += k
            mean = float(sum / l)
            if mean == x:
                z = j
            if mean == y:
                n = j

    z = df1.loc[z, "title"]
    n = df1.loc[n, "title"]

    r1 = z[:-7]
    r2 = n[:-7]

    z = z[-5:-1]
    n = n[-5:-1]


    print("Highest rated movie is:", r1,"with a mean value of ratings equal to:", x,"released in year:", z)
    print("Lowest rated movie is:", r2, "with a mean value of ratings equal to:", y,"released in year:", n)


if __name__ == "__main__":
  experimentsOnMovies(myAprioriHash(CreateUserBaskets(ReadRatings('ratings.csv')), 140, 5))
