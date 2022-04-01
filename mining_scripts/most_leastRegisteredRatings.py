  # Prints the greatest and least number of registered ratings with users' id.
  # Append this script into Apriori_Son.py script.
  
def experimentsOnUsers(frequentItemsetsDict):  # using MovieBaskets.

    quintupleList = []  # list of 5-tuples
    df = ReadRatings('ratings.csv')

    for key, value in frequentItemsetsDict.items():
        if value >= 480 :
            if type(key) is tuple and len(key) == 5:
                quintupleList.append(key)

    numOfRatingsList = []
    for i in quintupleList:
        auxNumOfRatingsList = []
        for j in i:
            k = len(df.loc[df["userId"] == j])
            auxNumOfRatingsList.append(k)
        numOfRatingsList.append(auxNumOfRatingsList)

    flatList = list(chain(*numOfRatingsList))

    x = max(flatList)
    y = min(flatList)

    for i in quintupleList:
        for j in i:
            if len(df.loc[df["userId"] == j]) == 2698:
                z = j
            if len(df.loc[df["userId"] == j]) == 635:
                n = j

    print("Most registered ratings:", x, "by user with id:", z)
    print("Least registered ratings:", y, "by user with id:", n)

if __name__ == "__main__":
  experimentsOnUsers(myAprioriHash(CreateMovieBaskets(ReadRatings('ratings.csv')), 480, 5))
