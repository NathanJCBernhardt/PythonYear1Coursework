def main():
    filename = input('Vote file name: ')
    nbrSeats = int(input('Number of seats to be allocated: '))
    method = input("Enter the Method (D/S): ")
    votes = readVoteFile(filename)
    seats = getSeats(votes, nbrSeats, method)
    for party in seats:
        print(party,'gets',seats[party],'seats')

def getSeats(votes,nbrSeats, method):
    seats = {}
    quotient = 0
    if method == "D":
        for party in votes:
            seats[party] = 0
        for round in range(0,nbrSeats):
            party = getWinner(votes,seats)
            seats[party] += 1
        return seats
    elif method == "S":
        for party in votes:
            seats[party] = 0
        for round in range(0, nbrSeats):
            party = getWinner2(votes, seats)
            seats[party] += 1
        return seats

def getWinner(votes,seats):
    maxQuotient = -1
    for party in votes:
        quotient = getQuotient(party,votes,seats)
        if quotient > maxQuotient:
            winner = party
            maxQuotient = quotient

    return winner

def getWinner2(votes, seats):
    maxQuotient = -1
    for party in votes:
        quotient = getQuotient2(party,votes,seats)
        if quotient > maxQuotient:
            winner = party
            maxQuotient = quotient
    return winner

def getQuotient(party,votes,seats):
    return votes[party]/(1 + seats[party])
def getQuotient2(party,votes,seats):
    return votes[party] /(2*seats[party] + 1)

def readVoteFile(filename):
    voteFile = open(filename)
    votes = {}
    for line in voteFile:
        lineSplit = line.split(':')
        party = lineSplit[0].strip()
        nbrVotes = int(lineSplit[1])
        votes[party] = nbrVotes
    return votes

def addTo(d1, d2): #For exercise 12
    for i,v in d2.items():
        if i not in d1.keys(): 
            d1[i] = v
        else:
            d1[i] = int(d1[i]) + int(d2[i]) 
    
    return d1 

def getTotalSeats(filename, method):# Exercise 12
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

    if method == "D": #D'hondt method
        for party in votes:
            seats[party] = 0
        for round in range(0,nbrSeats):
            party = getWinner(votes,seats)
            seats[party] += 1
        return seats
    else: #Sainte-Laguë method
        for party in votes:
            seats[party] = 0
        for round in range(0, nbrSeats):
            party = getWinner2(votes, seats)
            seats[party] += 1
        return seats
            
    newFile.close()

        
        
        
x = getTotalSeats("ukeu2019.txt", "S")
print(x)
    
