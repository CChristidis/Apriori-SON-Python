  # Prints the highest and lowest mean value of ratings with users' id

def experimentsOnUsers(frequentItemsetsDict):  # using MovieBaskets.

    quintupleList = []  # list of 5-tuples
    df = ReadRatings('ratings.csv')

    for key, value in frequentItemsetsDict.items():
        if value >= 480 :
            if type(key) is tuple and len(key) == 5:
                quintupleList.append(key)

    meanRatingsList = []
    for i in quintupleList:
        auxMeanRatingsList = []
        for j in i:
            m = len(df.loc[df["userId"] == j])
            summ = 0
            meann = 0
            for k in df.loc[df["userId"] == j, "rating"]:
                summ += k
            meann = float (summ/m)
            meann = round(meann, 3)

            auxMeanRatingsList.append(meann)
        meanRatingsList.append(auxMeanRatingsList)

    createCSV2("userExperimentMeanValueOfRatingsList.csv", meanRatingsList)
    flatMeanRatingsList = list(chain(*meanRatingsList))
    mx = max(flatMeanRatingsList)
    mn = min(flatMeanRatingsList)

    for i in quintupleList:
        for j in i:
            m = len(df.loc[df["userId"] == j])
            summ = 0
            meann = 0
            for k in df.loc[df["userId"] == j, "rating"]:
                summ += k
            meann = float(summ / m)
            meann = round(meann, 3)
            if meann == mx:
                z = j
            if meann == mn:
                n = j

    print("Greatest ratings mean value is:", mx,"by user with id:",z )
    print("Lowest ratings mean value is:", mn, "by user with id:",n )

if __name__ == "__main__":
  experimentsOnUsers(myAprioriHash(CreateMovieBaskets(ReadRatings('ratings.csv')), 480, 5))
