import math
import operator
def getTotal(dict1): # Exercise 1
    return sum(dict1.values()) #returns the sum of all values in the dictionary

def normalise(dict1): # Exercise 2
    temp = getTotal(dict1) #gets the sum of all values before going in the loop so they dont change
    for x in dict1:
        dict1[x] = dict1[x] / temp #value = value/sum of all values
    return dict1

def printNonZero(dict1): #Exercise 3
    for x,y in dict1.items():
        if y != 0:
            print ("{0} : {1}".format(x,y))

def analyse(x,y): #Exercise 4
    newy = {}
    normalise(x) #normalising before so we get the percentages of all votes

    for u,v in y.items():
        if v != 0:
            newy[u] = v
        else:
            x.pop(u, None) #if party has 0 seats, then remove the party from the first dictionary as well
    
    normalise(newy) #normalise the seats afterwards

    for j,k in newy.items():
        print("{0} : {1} % of votes vs {2} % of seats".format(j, round(x[j] * 100), round(k* 100)))

def addTo(d1, d2): #Exercise 5
    for i,v in d2.items():
        if i not in d1.keys(): #if d1 key isnt in d2, then add it
            d1[i] = v
        else:
            d1[i] = int(d1[i]) + int(d2[i]) #if d1 key is in d2, then add them together and return d1 modified
    
    return d1 

def getConstituencies(filename): #PART B Exercise 6
    newSet = set()
    newFile = open(filename)

    for line in newFile:
        if "_Constituency:" in line:
            line = line.strip() #remove "/n" from the end of string
            x = line.split(":")
            newSet.add(x[1]) #adds the Constituency to the set 

    newFile.close()
    return newSet

def getParties(filename): #Exercise 7
    newSet = set()
    newFile = open(filename)

    for line in newFile:
        if "_" not in line and line[0] != "\n": #if not _Constituency or _Seats
            x = line.split(":")
            newSet.add(x[0]) #adds the party to the set
    newFile.close()
    return newSet

def getVotesForConstituency(filename, cons): #Exercise 8
    dictionary = {}
    temp = "_Constituency:" + cons #joining the desired Constituency with "_Constituency"
    
    newFile = open(filename)

    always_append = False

    for line in newFile:
        if line[0] == "\n": #keep adding to dictionary until you reach the "\n"
            always_append = False
        
        if always_append or temp in line: #creating a state
            line = line.strip()
            x = line.split(":")
            dictionary.add({x[0] : x[1]}) #add the party and it's votes to the dictionary
            always_append = True
            
    del dictionary['_Constituency'] #deletes Constituency and seats from dictionary so it only returns the parties
    del dictionary['_Seats']
    
    newFile.close()
    return dictionary

def getTotalVotes(filename): #Exercise 9
    dict1 = {}
    tempdict = {}
    dict2 = {}
    newFile = open(filename)

    for line in newFile:
        tempdict = {} #temp dictionary for addto function
        if line[0] == "_" or line[0] == "\n":
            pass #do nothing
        else:
            line = line.strip() #removes \n
            x = line.split(":") #splits at the colon
           
            if x[0] in dict1.keys(): #if the party is in dictionary
                tempdict.update({x[0] : x[1]})  #add the party and its votes to the temp dictionary
                dict1 = addTo(dict1, tempdict) #call the addto function to add the votes together
                
            else:
                dict1.update({x[0] : x[1]}) #otherwise just add the party and it's votes to the dictionary
                
    newFile.close()
    
    return dict1


def getWinner(votes,seats): #utilises the D'hondt method
    maxQuotient = -1
    for party in votes:
        quotient = getQuotient(party,votes,seats) 
        if quotient > maxQuotient:
            winner = party
            maxQuotient = quotient

    return winner

def getQuotient(party,votes,seats):
    return votes[party]/(1 + seats[party])



def getTotalSeats(filename): #Exercise 10 and Exercise 12
    #Uses D'hondt method or Sainte-Laguë method
    seats = {}
    votes = {}
    nbrSeats = 0
    
    newFile = open(filename)
    
    for line in newFile:
        dict1 = {} #temporary dictionary for the addTo function
        if "_Seats" in line: #accesses the number of seats in each Constituency
            line = line.strip() #removes \n
            x = line.split(":") #splits the string at the ":"
            nbrSeats = nbrSeats + int(x[1]) #number of seats = number of seats + seats for each Constituency
        if line[0] == "_" or line[0] == "\n":
            pass #do nothing
        else: #if line contains a party
            line = line.strip()
            x = line.split(":")
            if x[0] in votes.keys(): #if party is a key in votes dictionary
                dict1.update({x[0] : int(x[1])}) #update the value with number of votes
                votes = addTo(votes, dict1)  # sum of the original votes and new votes from other Constituency
            else:
                votes.update({x[0] : int(x[1])}) #otherwise just add the party and it's votes to the dictionary

    for i,v in votes.items():
        seats.update({i : 0}) #intialising seats


    for party in votes:
        seats[party] = 0
    for round in range(0,nbrSeats):
        party = getWinner(votes,seats)
        seats[party] += 1
    return seats

            
    newFile.close()


