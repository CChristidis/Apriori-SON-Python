import pandas as pd
import csv
import time
import psutil
from itertools import combinations, islice, chain


def ReadRatings(csvRatingsFile):
    my_ratings_df = pd.read_csv(csvRatingsFile)
    return my_ratings_df


def ReadMovies(csvMovieFile):
    my_movies_df = pd.read_csv(csvMovieFile)
    return my_movies_df


def CreateUserBaskets(my_ratings_df):
    my_userBaskets = {}

    for i in range(len(my_ratings_df)):  # my_ratings_df.index.stop == overall number of csv rows
        if my_ratings_df.loc[i, "userId"] not in my_userBaskets:
            my_userBaskets[my_ratings_df.loc[i, "userId"]] = set()

        my_userBaskets[my_ratings_df.loc[i, "userId"]].add(my_ratings_df.loc[i, "movieId"])

    return my_userBaskets


def CreateMovieBaskets(my_ratings_df):
    my_movieBaskets = {}

    for i in range(len(my_ratings_df)):  # my_ratings_df.index.stop == overall number of csv rows
        if my_ratings_df.loc[i, "movieId"] not in my_movieBaskets :
            my_movieBaskets[my_ratings_df.loc[i, "movieId"]] = set()

        my_movieBaskets[my_ratings_df.loc[i, "movieId"]].add(my_ratings_df.loc[i, "userId"])

    return my_movieBaskets


def ExactCounting(itemBaskets):
    hashTable = {}  # init of hash-table structure for subset counting

    for i in itemBaskets:  # for every itme in basket...
        for j in range(len(itemBaskets[i])) :  # for every set in basket...
            for k in combinations(sorted(itemBaskets[i]), j+1):  # find every possible combination for this set
                if k not in hashTable:
                    hashTable[k] = 1
                else:
                    hashTable[k] += 1
    return hashTable


def myApriori(itemBaskets, minSupport, maxLength):
    listOfFreqItemsets = []  # list-of-lists which is going to be returned after the end of routine. Every list is a frequent itemset
    auxHashTable = {}  # hash table containg the counters for every frequent k-set

    for i in itemBaskets:  # for every userId(movieId)
        for j in itemBaskets[i]:  # for ever movieId(userId)
            if j not in auxHashTable:
                auxHashTable[j] = 1
            else:
                auxHashTable[j] += 1

    singletonList = []  # this list holds the frequent singletons of itemBaskets
    for i in auxHashTable:
        if auxHashTable[i] >= minSupport:
            singletonList.append(i)

    singletonList = sorted(singletonList)
    listOfFreqItemsets.append(singletonList)  # now we already have the most frequent 1-sets. (maxLength - 1)
    # more to go.

    for i in range(1, maxLength):
        """
        this for loop is used in order to create an order on k-sets constructions. e.g. if i = 1 -> we are constructing 2-sets (pairs)
        if i = 2 -> we are constructing 3-sets(triads)
        """
        auxHashTable = {}

        for j in itemBaskets:
            auxList = []
            """ auxList contains the frequent singletons belonging to every basket individually (itemBaskets[j], j == 0,1,...,len(itemBaskets)).
             Is a subset of singletonList. 
            """
            for k in singletonList:  # parsing the singletonList in order to find the 1-set that belong to itemBaskets[j]
                if k not in itemBaskets[j]:
                    continue  # goto next element of singletonList
                else:
                    auxList.append(k)  # append it to the auxiliary list.
            if i == 1:
                for k in combinations(auxList, 2):  # construct pairs (2-sets)
                    if k not in auxHashTable:
                        auxHashTable[k] = 1
                    else:
                        auxHashTable[k] += 1
            else:
                """ 
                we are going to construct k-set by conjoining the frequent (k-1)-set existing in currently
                processed basket (itemBaskets[j]) with elements from singletonList (frequent singletons).
                """
                for k in kMinusOneFreqSet:
                    if set(k).issubset(itemBaskets[j]):
                        for m in auxList:
                            """
                            construct k-set by conjoining a frequent (k-1)-set with a frequent singleton, both
                            being part of itemBaskets[j]
                            """
                            n = list(k)  # convert n tuple into a list so we can easily append m
                            if m not in n:   # if m already exists in n tuple, we are not able to create a k-set with it
                                n.append(m)  # if m doesn't exist in n tuple, append it.
                                n = tuple(sorted(n))  # sort the n+m list and convert it into a tuple. Now we have a new k-set
                                if n not in auxHashTable:
                                    auxHashTable[n] = 1
                                else:
                                    auxHashTable[n] += 1

        kMinusOneFreqSet = []
        """ 
        This list holds the sets that will be considered frequent below. 
        Named freqKMinusOneSetList because it will hold the frequent (k-1)-sets 
        which will be used in order to construct k-sets. This technique saves time 
        as we don't need to brute-forcely construct k-sets from scratch and only after that 
        check if these k-sets exceed the threshold of the applied support.
        """
        for j in auxHashTable:
            if auxHashTable[j] >= minSupport:  # support check...
                kMinusOneFreqSet.append(j)

        if len(kMinusOneFreqSet) == 0:  # check if there are still frequent itemsets left
            return listOfFreqItemsets

        listOfFreqItemsets.append(kMinusOneFreqSet)

    return listOfFreqItemsets


def makeChunks(itemBaskets, chunkSize):
    it = iter(itemBaskets)  # construct an iterator responsible for parsing itemBaskets dictionary.
    for i in range(0, len(itemBaskets), chunkSize):  # execute len(itemBaskets)/chunkSize iterations (number of chunks to be constructed).
        yield {k: itemBaskets[k] for k in islice(it, chunkSize)}  # yield the chunk containing the keys from it to chunkSize.
        """ 
        the first iteration will yield the chunk which is consisted by the first "chunkSize" keys of itemBaskets.
        the second iteration will yield the chunk which is consisted by the first "chuckSize" keys after the first "chunkSize" keys of itemBaskets.
        the third iteration will yield the chuck which is consisted by the first "chunkSize" keys after the first 2*"chunkSize" keys of itemBaskets.
        .
        .
        .
        the n-th iteration will yield the chunk which is consisted by the first "chunkSize" keys after the first (n-1)*"chunkSize" keys of itemBaskets
        """


def SON(itemBaskets, chunkSize, minSupport, maxLength):
    auxList = []  # contains the list of lists returned by myApriori for a certain chunk.
    aprioriHashTable = {}  # contains all the elements that exceed the (reducted) support, after every chunk has finished invoking myApriori .
    hashTable = {}  # contains the number of overall appearances (in every element of itemBaskets) of every element found in aprioriHashTable.

    for basket in makeChunks(itemBaskets, chunkSize):  # execute apriori algorithm for every chunk individually

        auxList = list((chain(*myApriori(basket, (minSupport / chunkSize), maxLength))))

        for i in auxList:  # add every element of auxList that exceed the s = (minSupport / chunkSize) support in aprioriHashTable
            aprioriHashTable[i] = 1

    l = list(itemBaskets.values())
    for i in aprioriHashTable:
        for j in l:
            if type(i) is tuple:
                if set(i).issubset(j) is True:
                    if i not in hashTable:
                        hashTable[i] = 1
                    else:
                        hashTable[i] += 1
            else:
                if i in j:
                    if i not in hashTable:
                        hashTable[i] = 1
                    else:
                        hashTable[i] += 1
    return hashTable


def createCSVFromDictionary(filepath, dictionary):  
    with open(filepath, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        for key, value in dictionary.items():
            writer.writerow([key, value])
        f.close()

def createCSVFromList(filepath, list):
    with open(filepath, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(list)


def myAprioriHash(itemBaskets, minSupport, maxLength):
    auxHashTable = {}  # hash table containg the counters for every frequent k-set
    hashTable = {}

    for i in itemBaskets:  # for every userId(movieId)
        for j in itemBaskets[i]:  # for ever movieId(userId)
            if j not in auxHashTable:
                auxHashTable[j] = 1
            else:
                auxHashTable[j] += 1

    singletonList = []  # this list holds the frequent singletons of itemBaskets
    for i in auxHashTable:
        if auxHashTable[i] >= minSupport:
            singletonList.append(i)
            hashTable[i] = auxHashTable[i]

    singletonList = sorted(singletonList)

    for i in range(1, maxLength):
        """
        this for loop is used in order to create an order on k-sets constructions. e.g. if i = 1 -> we are constructing 2-sets (pairs)
        if i = 2 -> we are constructing 3-sets(triads)
        """
        auxHashTable = {}

        for j in itemBaskets:
            auxList = []
            """ auxList contains the frequent singletons belonging to every basket individually (itemBaskets[j], j == 0,1,...,len(itemBaskets)).
             Is a subset of singletonList. 
            """
            for k in singletonList:  # parsing the singletonList in order to find the 1-set that belong to itemBaskets[j]
                if k not in itemBaskets[j]:
                    continue  # goto next element of singletonList
                else:
                    auxList.append(k)  # append it to the auxiliary list.
            if i == 1:
                for k in combinations(auxList, 2):  # construct pairs (2-sets)
                    if k not in auxHashTable:
                        auxHashTable[k] = 1
                    else:
                        auxHashTable[k] += 1
            else:
                """ 
                we are going to construct k-set by conjoining the frequent (k-1)-set existing in currently
                processed basket (itemBaskets[j]) with elements from singletonList (frequent singletons)
                """
                for k in kMinusOneFreqSet:
                    if set(k).issubset(itemBaskets[j]):
                        for m in auxList:
                            """
                            construct k-set by conjoining a frequent (k-1)-set with a frequent singleton, both
                            being part of itemBaskets[j]
                            """
                            n = list(k)  # convert n tuple into a list so we can easily append m
                            if m not in n:   # if m already exists in n tuple, we are not able to create a k-set with it
                                n.append(m)  # if m doesn't exist in n tuple, append it.
                                n = tuple(sorted(n))  # sort the n+m list and convert it into a tuple. Now we have a new k-set
                                if n not in auxHashTable:
                                    auxHashTable[n] = 1
                                else:
                                    auxHashTable[n] += 1

        kMinusOneFreqSet = []
        """ 
        This list holds the sets that will be considered frequent below. 
        Named freqKMinusOneSetList because it will hold the frequent (k-1)-sets 
        which will be used in order to construct k-sets. This technique saves time 
        as we don't need to brute-forcely construct k-sets from scratch and only after that 
        check if these k-sets exceed the threshold of the applied support.
        """
        for j in auxHashTable:
            if auxHashTable[j] >= minSupport:  # support check...
                kMinusOneFreqSet.append(j)
                hashTable[j] = auxHashTable[j]

        if len(kMinusOneFreqSet) == 0:  # check if there are still frequent itemsets left
            return hashTable

    return hashTable
