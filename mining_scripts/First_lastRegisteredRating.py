  # Prints the first and last registered rating (day/year/time).
  # Append this script into Apriori_Son.py script.
  
def first_lastRegisteredRatings(frequentItemsetsDict):  # using MovieBaskets.

    quintupleList = []  # list of 5-tuples
    df = ReadRatings('ratings.csv')

    for key, value in frequentItemsetsDict.items():
        if value >= 480 :
            if type(key) is tuple and len(key) == 5:
                quintupleList.append(key)

    maxTimestampList = []
    minTimestampList = []
    for i in quintupleList:
        auxMaxTimestampList = []
        auxMinTimestampList = []
        for j in i:
            maxx = 0
            minn = 100000000000000
            for k in df.loc[df["userId"] == j, "timestamp"]:
                if k <= minn:
                    minn = k
                if k >= maxx:
                    maxx = k
            auxMaxTimestampList.append(maxx)
            auxMinTimestampList.append(minn)

        maxTimestampList.append(auxMaxTimestampList)
        minTimestampList.append(auxMinTimestampList)

    createCSV2("userExperimentMaxTimestampList.csv", maxTimestampList)
    createCSV2("userExperimentMinTimestampList.csv", minTimestampList)

    flatMaxList = list(chain(*maxTimestampList))
    flatMinList = list(chain(*minTimestampList))

    x = max(flatMaxList)  # greatest timestamp amongst the users
    y = min(flatMinList)  # lowest timestamp amongst the users

    for i in quintupleList:
        for j in i:
            for k in df.loc[df["userId"] == j, "timestamp"]:
                if k == x:
                    z = j  # max id
                if k == y:
                    n = j
    h = (x % 31556926)  # day
    u = (y % 31556926)  # days

    q = h % 86400 # hours
    t = u % 86400 # hours

    o = q % 3600 # mins
    p = t % 3600 # mins

    g = o % 60  # secs
    s = p % 60  #secs

    o = int (o/60)
    p = int (p/60)

    q = int (q/3600)
    t = int (t/3600)

    h = int (h/86400)

    u = int (u/86400)

    x = int(x / 31556926)  # year
    y = int(y / 31556926)  # year

    x += 1970
    y += 1970

    if o < 10:
        o = "0" + str(o)
    if p < 10:
        p = "0" + str(p)

    print("Latest registered rating happened on day:", h, "of year:", x, "at:", str(q)+":"+str(o)+":"+str(g),"by user with id:", z)
    print("First ever registered rating happened on day:", u, "of year:", y, "at:", str(t)+":"+str(p)+":"+str(s),"by user with id:", n)
    
if __name__ == "__main__":
  first_lastRegisteredRatings(myAprioriHash(CreateMovieBaskets(ReadRatings('ratings.csv')), 480, 5))
