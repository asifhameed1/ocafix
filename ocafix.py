#!/usr/bin/env python3

# Author David.Robson
# 2018-05-24 Created

from datetime import date,timedelta
import pickle
import random
import sys

maxConcurrentHomeMatchesPerClub = {

'University' : 2,
'Witney'     : 2,
'City'       : 2,
'Cowley'     : 3,
'Banbury'    : 2,
'Didcot'     : 2,
'Bicester'   : 2,
'Wantage'    : 2,
'Cumnor'     : 2,
'MCS/B'      : 2,
'Abingdon'   : 2,

}

# Club,TeamNumber,Division,Match Night (Monday=0)

teams = [    

# Division 1
[
['University',1,3],
['Witney',1,0],
['City',1,0],
['Cowley',2,3],
['Witney',2,0],
['Banbury',1,1],
['Didcot',1,2],
['Cowley',1,0],
],

# Division 2

[
['Bicester',1,0],
['University',2,3],
['Banbury',2,1],
['Wantage',1,1],
['Cowley',3,0],
['Cumnor',1,3],
['City',2,0],
['Cowley',4,0],
],

# Division 3

[
['Didcot',2,2],
['MCS/B',1,0],
['Didcot',3,2],
['Banbury',3,2],
['City',3,0],
['Cumnor',2,4],
['Witney',3,0],
['Cowley',5,0],
],

# Division 4

[
['Didcot',4,0],
['University',3,3],
['Abingdon',1,0],
['Witney',4,0],
['Bicester',2,0],
['Wantage',2,0],
['Cowley',6,3],
],

]

# Following clubs will be scheduled as early in the season as possible

clubsForEarlyScheduling = [
'University'
]

# Following days will be excluded from fixtures for everyone

globalExcludedDays = [
date(2019,4,8),        # Peter Wells' Simultaneous
date(2019,2,4),        # Kidlington Tournament Hangover
date(2018,11,5),       # Witney Weekend Congress Hangover
date(2019,4,22),       # Easter Bank Holiday 
date(2019,4,22),       # Cowley Blitz 
]

# Following days will be excluded from fixtures for specific teams
teamExcludedDays = {
'Cowley2'     : [
date(2019,4,18),       # Maunday Thursday
]
}

availablePeriods = {

'Abingdon' : [
[ date(2018,9,4), date(2018,12,14) ],     # Michaelmas
[ date(2019,1,8), date(2019,3,29) ],      # Lent
[ date(2019,4,24), date(2019,7,5) ],      # Summer
],

'University' : [
[ date(2018,10,14), date(2018,12,1) ],    # Michaelmas:  2nd to 7th week
[ date(2019,1,13), date(2019,3,9) ],      # Hilary:      1st to 8th week
[ date(2019,4,28), date(2019,5,26) ],     # Trinity:     1st to 4th week
],

}

# Weeks with the following days in them will be excluded from fixtures for everyone

globalExcludedWeeks = [
#date(2019,4,1).isocalendar()[1],
#date(2019,4,8).isocalendar()[1],
#date(2019,4,15).isocalendar()[1],
#date(2019,4,22).isocalendar()[1],
]

# Define the two halves of the season

firstDateOfFirstHalf=date(2018,10,1)
lastDateOfFirstHalf=date(2018,12,21)

firstDateOfSecondHalf=date(2019,1,7)
lastDateOfSecondHalf=date(2019,5,16)

bestScore = 99999

fixtures = []
fixtureDate = {}  # key is homeClub.HomeTeamNumber.awayClub.awayTeamNumber

#---------------------------------------------------------------------------------------

def isFixtureOK ( pdate, pdivision, phomeClub, phomeTeamNumber, pawayClub, pawayTeamNumber,phomeClubNight):

    pweek = pdate.isocalendar()[1]
    homeFixturesOnThisDay = 0

# Check that proposed fixture is not an excluded day

    if pdate in globalExcludedDays:
       return False

# Check that proposed fixture is not in an excluded week

    if pweek in globalExcludedWeeks:
       return False

# Check that home team is playing in a their allowed period

    inAllowedPeriod = False
    try:
        for period in availablePeriods[phomeClub]:
            start, finish = period
            if start <= pdate <= finish:
               inAllowedPeriod = True
    except KeyError:
       inAllowedPeriod = True        # No list of allowed periods so assume all dates possible
    if not inAllowedPeriod:
       return False

# Check that away team is playing in their allowed period

    inAllowedPeriod = False
    try:
        for period in availablePeriods[pawayClub]:
            start, finish = period
            if start <= pdate <= finish:
               inAllowedPeriod = True
    except KeyError:
       inAllowedPeriod = True        # No list of allowed periods so assume all dates possible
    if not inAllowedPeriod:
       return False
    

# Check if date is excluded for the home team

    try:
        for excludedDate in teamExcludedDays[phomeClub + str(phomeTeamNumber)]:
            if pdate == excludedDate:
               return False
    except KeyError:
        pass

# Check if date is excluded for the away team

    try:
        for excludedDate in teamExcludedDays[pawayClub + str(pawayTeamNumber)]:
            if pdate == excludedDate:
               return False
    except KeyError:
        pass

    bicester1AtHomeOnThisDay  = False

    for fixture in fixtures:
        fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
        fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]

        if fhomeClub == phomeClub and fdate == pdate:
           homeFixturesOnThisDay += 1

# Check that the home club isn't exceeding its maximum number of fixtures per night
        
           try:
              if homeFixturesOnThisDay >= maxConcurrentHomeMatchesPerClub[phomeClub]:
                 return False
           except KeyError:
               print("No maxConcurrentHomeMatchesPerClub for",phomeClub,file=sys.stderr)
               sys.exit(2)

# Check that there isn't already a Cowley home fixtures on this day
# if it is the third Monday of the week (Stamp Club clash)
        
           if 14 < pdate.day < 22 and homeFixturesOnThisDay >= 1:
              return False

        if fdate is not None:    # i.e. a fixture has already been scheduled


#--------------------------------------------------
#          Examine fixtures happening on this day
#--------------------------------------------------

           fweek = fdate.isocalendar()[1]
           if pweek == fweek:

# Check if proposed home team already has a home fixture in this week
# Exclude the University, because of their short terms
        
              if phomeClub == fhomeClub and phomeClub != 'University' and phomeTeamNumber == fhomeTeamNumber:
                 return False

# Check if proposed home team already has a away fixture in this week
# Exclude the University, because of their short terms
        
              if phomeClub == fawayClub and phomeClub != 'University' and phomeTeamNumber == fawayTeamNumber:
                 return False

# Check if proposed away team already has a home ixture in this week
# Exclude the University, because of their short terms
        
              if pawayClub == fhomeClub and pawayClub != 'University' and pawayTeamNumber == fhomeTeamNumber:
                 return False

# Check if proposed away team already has an away fixture in this week
# Exclude the University, because of their short terms
        
              if pawayClub == fawayClub and pawayClub != 'University' and pawayTeamNumber == fawayTeamNumber:
                 return False

#--------------------------------------------------
#          Examine fixtures happening on this day
#--------------------------------------------------

           if pdate == fdate:

# Check if home team already has a home fixture on this day
        
              if (phomeClub == fhomeClub and phomeTeamNumber == fhomeTeamNumber) or phomeClub == fawayClub and phomeTeamNumber == fawayTeamNumber:
                 return False

# Check if away team already has a home fixture on this day
        
              if (pawayClub == fhomeClub and pawayTeamNumber == fhomeTeamNumber) or pawayClub == fawayClub and pawayTeamNumber == fawayTeamNumber:
                 return False

    return True

#---------------------------------------------------------------------------------------

def fillFixtures():

   fixtures.clear()

   # Generate required fixtures

   for division in range(0,len(teams)):
      for homeTeam in teams[division]:
          homeClub, homeTeamNumber, homeTeamNight = homeTeam
          for awayTeam in teams[division]:
              awayClub, awayTeamNumber, awayTeamNight = awayTeam
              if homeClub != awayClub or homeTeamNumber != awayTeamNumber: # teams cannot play themselves
                 awayClub, awayTeamNumber, awayTeamNight = awayTeam
                 fixture = ["Div" + str(division + 1), homeClub, homeTeamNumber, awayClub, awayTeamNumber, homeTeamNight]
                 fixtures.append(fixture)
                 fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)] = None

#  Randomize the order so that the next iteration will be different

   random.shuffle(fixtures)

# If the fixture is between two teams from the same club, put them at the beginning
# of the list so that they can be scheduled for the start of the season halves.

# Find the inter-club fixtures

   interClubFixtures = []
   for fixture in fixtures:
       fdiv, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
       if homeClub == awayClub:
          interClubFixtures.append(fixture)

# Then put the inter-club fixtures at the top of the fixture list

   for fixture in interClubFixtures:
       fixtures.remove(fixture)
       fixtures.insert(0, fixture)
#---------------------------------------------------------------------------------------

def attemptFixtures():

   # Clear old fixture dates

   for key,value in fixtureDate.items():
       fixtureDate[key] = None

   # Generate fixture dates

   for division in range(0,len(teams)):
      for fixture in fixtures:
          fdiv, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
          fdate = fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)]

          if fdate is None:
            # If return match already scheduled, schedule this one in the second half
             if  fixtureDate[awayClub + str(awayTeamNumber) + homeClub + str(homeTeamNumber)] is None:
                 firstDateOfHalf = firstDateOfFirstHalf
                 lastDateofHalf = lastDateOfFirstHalf
             # Otherwise schedule this in the first half
             else:
                 firstDateOfHalf = firstDateOfSecondHalf
                 lastDateofHalf = lastDateOfSecondHalf
             firstDayOfHalf = date.weekday(firstDateOfHalf)
             seasonLength = (lastDateofHalf - firstDateOfHalf).days

             fixtureOK = False;

# Try random dates in an attempt to spread the fixtures evenly through the available times

             if not fixtureOK:
                for attempt in range(1,150):
                   candidateDate = firstDateOfHalf + timedelta((homeClubNight - firstDayOfHalf) % 7)
                   if homeClub != awayClub: 
                      # Add a random shift of a whole number of weeks
                      randomWeekShift = 7 * int(random.randint(0,seasonLength - 7) / 7) 
                      candidateDate += timedelta(randomWeekShift)

                   fixtureOK = isFixtureOK ( candidateDate, fdiv, homeClub, homeTeamNumber, awayClub, \
                                             awayTeamNumber,homeClubNight )
                   if fixtureOK:
                      break 
                if not fixtureOK:
                   return False
        
             fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)] = candidateDate

   return True

#---------------------------------------------------------------------------------------

def scoreSimulation():

    score = 0

    for fixture in fixtures:
        div, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
        fdate = fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)]


        for lfixture in fixtures:

            ldiv, lhomeClub, lhomeTeamNumber, lawayClub, lawayTeamNumber,lhomeClubNight = lfixture
            ldate = fixtureDate[lhomeClub + str(lhomeTeamNumber) + lawayClub + str(lawayTeamNumber)]

            scoreForHomeTeamThisFixture = scoreForAwayTeamThisFixture = 0

            if fdate == ldate:
               if homeClub == lhomeClub and abs( homeTeamNumber - lhomeTeamNumber ) == 1:
                  scoreForHomeTeamThisFixture =  scoreForHomeTeamThisFixture * 3 + 1

               if homeClub == lawayClub and abs( homeTeamNumber - lawayTeamNumber ) == 1:
                  scoreForHomeTeamThisFixture =  scoreForHomeTeamThisFixture * 3 + 1

# Increase score if away team already has an adjacent team playing on this day

               if awayClub == lhomeClub and abs( awayTeamNumber - lhomeTeamNumber ) == 1:
                  scoreForAwayTeamThisFixture =  scoreForAwayTeamThisFixture * 3 + 1

               if awayClub == lawayClub and abs( awayTeamNumber - lawayTeamNumber ) == 1:
                  scoreForAwayTeamThisFixture =  scoreForAwayTeamThisFixture * 3 + 1

# Decrease score if Bicester teams are playing home matches on the same day

               if homeClub == 'Bicester' and lhomeClub == 'Bicester' and homeTeamNumber != lhomeTeamNumber:
                  score -= 20

            score += scoreForHomeTeamThisFixture + scoreForAwayTeamThisFixture

    return score

#---------------------------------------------------------------------------------------

def trySimulation(count):

   global bestScore

   for j in range(0,10000):
       fillFixtures()
       itWorked = attemptFixtures()
       if itWorked:
          break

   if itWorked:
      score = scoreSimulation()
      if score < bestScore:
         bestScore = score
         pickle.dump( [fixtures,fixtureDate] , open( "fixtures.pickle", "wb" ) )

   if itWorked:
      return True
   return False

#---------------------------------------------------------------------------------------

def printFixtureList():

    try:
        data = pickle.load(open( "fixtures.pickle", "rb" ))
        fixtures, fixtureDate = data

        outputs = []
        for fixture in fixtures:
            fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
            fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]
            outputs.append((fdate.strftime('%Y-%m-%d (%a)') +" " + fdiv + " " + fhomeClub + str(fhomeTeamNumber)\
                   + " v " + fawayClub + str(fawayTeamNumber)))
        outputs.sort()
        for output in outputs:
            print(output)
    except FileNotFoundError:
        print("ERROR: Pickle file not found",file=sys.stderr)
        pass

#---------------------------------------------------------------------------------------

def main():

       solutionFound = False
       for j in range(1,50):
           if trySimulation(j):
              solutionFound = True

       if solutionFound:
          printFixtureList()
          sys.exit(0)

       else:
          print("Unable to find a solution",file=sys.stderr)
          sys.exit(1)

#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
