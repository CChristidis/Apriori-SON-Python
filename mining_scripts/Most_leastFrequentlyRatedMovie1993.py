  # Prints the most and least frequently rated movie of 1993
  # Append this script into Apriori_Son.py script.
  
def most_leastFrequentlyRatedMovie1993(frequentItemsetsDict):  # using UserBaskets.

    quintupleList = []  # list of 5-tuples
    df = ReadMovies('movies.csv')

    for key, value in frequentItemsetsDict.items():
        if value >= 140 :
            if type(key) is tuple and len(key) == 5:
                quintupleList.append(key)

    hashTable = {}
    for i in quintupleList:
        for j in i:
            k = df.loc[j - 1, "title"][:-7]
            if df.loc[j - 1, "title"][-5:-1] == "1993":
                if k not in hashTable:
                    hashTable[k] = 1
                else:
                    hashTable[k] += 1

    x = max(hashTable, key = hashTable.get)
    y = min(hashTable, key = hashTable.get)

    print("Most common movie of 1993 is:", x)
    print("Least common movie of 1993 is:", y)
    
if __name__ == "__main__":
  most_leastFrequentlyRatedMovie1993(myAprioriHash(CreateUserBaskets(ReadRatings('ratings.csv')), 140, 5))
