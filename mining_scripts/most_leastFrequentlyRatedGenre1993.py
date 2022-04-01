  # Prints the most and least frequently rated genre of 1993.
  # Append this script into Apriori_Son.py script.
  
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
            k = df.loc[j - 1, "genres"].split("|")
            print(k)
            if df.loc[j - 1, "title"][-5:-1] == "1993":
                for m in k:
                    if m not in hashTable:
                        hashTable[m] = 1
                    else:
                        hashTable[m] += 1

    x = max(hashTable, key = hashTable.get)
    y = min(hashTable, key = hashTable.get)

    print("Most common genre of 1993 is:", x)
    print("Least common genre of 1993 is:", y)
    
if __name__ == "__main__":
  experimentsOnMovies(myAprioriHash(CreateUserBaskets(ReadRatings('ratings.csv')), 140, 5))
