  # Prints the genre of most and least common rated movie of 1993 

def experimentsOnMovies(frequentItemsetsDict):  # using UserBaskets.

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
    z = df.loc[df["title"] == x + " (1993)", "genres"]
    y = min(hashTable, key = hashTable.get)
    b = df.loc[df["title"] == y + " (1993)", "genres"]

    print("Genre of most common movie of 1993 is:", z)
    print("Genre of least common movie of 1993 is:", b)
    
if __name__ == "__main__":
  experimentsOnMovies(myAprioriHash(CreateUserBaskets(ReadRatings('ratings.csv')), 140, 5))
