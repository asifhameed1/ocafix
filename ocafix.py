#!/usr/bin/env python3

#######################################################################
# Author David.Robson
# 2018-05-24 Created
#
# The number of simulations to be undertaken is supplied by an argument.
# The default is one.
#######################################################################

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
'Wantage'    : 1,
'Cumnor'     : 2,
'MCS/B'      : 2,
'Abingdon'   : 2,

}

Monday    = 0
Tuesday   = 1
Wednesday = 2
Thursday  = 3

# Club,TeamNumber,Division,Match Night (Monday=0)

teams = [    

# Division 1
[
['University', 1, Thursday],
['Witney',     1, Monday],
['City',       1, Monday],
['Cowley',     2, Thursday],
['Cumnor',     1, Thursday],
['Banbury',    1, Thursday],
['Didcot',     1, Monday],
['Cowley',     1, Monday],
],

# Division 2

[
['Witney',     2, Monday],
['Bicester',   1, Monday],
['University', 2, Thursday],
['Banbury',    2, Thursday],
['Wantage',    1, Tuesday],
['Cowley',     3, Monday],
['City',       2, Monday],
['Didcot',     2, Monday],
],

# Division 3

[
['Cowley',     4, Thursday],
['MCS/B',      1, Monday],
['Didcot',     3, Wednesday],
['Banbury',    3, Thursday],
['City',       3, Monday],
['Witney',     3, Monday],
['Cowley',     5, Monday],
['Abingdon',   1, Monday],
],

# Division 4

[
['Didcot',     4, Monday],
['University', 3, Thursday],
['Cumnor',     2, Thursday],
['Witney',     4, Monday],
['Bicester',   2, Monday],
['Wantage',    2, Tuesday],
['Cowley',     6, Thursday],
],

]

# Following clubs will be scheduled as early in the season as possible

clubsForEarlyScheduling = [
'University'
]

# Following days will be excluded from fixtures for everyone

globalExcludedDays = [
date(2020,4,6),        # Peter Wells' Simultaneous
date(2020,2,3),        # Kidlington Tournament Hangover
date(2019,11,4),       # Witney Weekend Congress Hangover
date(2020,4,10),       # Good Friday
date(2020,4,13),       # Easter Bank Holiday 
date(2019,12,9),       # Cowley Blitz 
]

# Following days will be excluded from fixtures for specific teams
teamExcludedDays = {
'Cowley2'     : [
date(2020,4,9),       # Maunday Thursday
],
'Banbury1'  : [
    date(2019,9,12),date(2019,9,16),date(2019,9,26),date(2019,10,3),date(2019,10,7),date(2019,10,17),date(2019,10,24),date(2019,11,6),date(2019,11,12),date(2019,11,28),date(2019,12,16),date(2019,12,18),date(2020,1,9),date(2020,1,16),date(2020,1,22),date(2020,1,27),date(2020,1,28),date(2020,2,6),date(2020,2,13),date(2020,2,17),date(2020,2,18),date(2020,3,19),date(2020,3,23),date(2020,3,26),date(2020,4,2),date(2020,4,9),
],
'Banbury2'  : [
 date(2019,9,12),date(2019,9,26),date(2019,10,7),date(2019,10,15),date(2019,10,24),date(2019,11,12),date(2019,11,21),date(2019,11,28),date(2019,12,3),date(2019,12,12),date(2019,12,18),date(2020,1,9),date(2020,1,13),date(2020,1,28),date(2020,2,6),date(2020,2,13),date(2020,2,18),date(2020,2,27),date(2020,3,19),date(2020,3,23),date(2020,3,25),date(2020,4,2),date(2020,4,7),
],
'Banbury3'  : [
date(2019,9,11),date(2019,9,12),date(2019,9,19),date(2019,9,26),date(2019,10,1),date(2019,10,7),date(2019,10,9),date(2019,10,15),date(2019,10,17),date(2019,10,23),date(2019,10,30),date(2019,10,31),date(2019,11,7),date(2019,11,12),date(2019,11,14),date(2019,11,21),date(2019,12,2),date(2019,12,3),date(2019,12,5),date(2019,12,10),date(2019,12,12),date(2019,12,16),date(2020,1,9),date(2020,1,13),date(2020,1,21),date(2020,1,23),date(2020,1,28),date(2020,2,6),date(2020,2,10),date(2020,2,11),date(2020,2,13),date(2020,2,20),date(2020,2,25),date(2020,2,27),date(2020,3,12),date(2020,3,19),date(2020,3,25),date(2020,3,26),date(2020,4,2),date(2020,4,7),date(2020,4,15),
]

}

availablePeriods = {

'Abingdon' : [
[ date(2019,9,10), date(2019,10,11) ],     # 1st 
[ date(2019,10,28), date(2019,12,13) ],      # 2nd
[ date(2020,1,7), date(2020,2,14) ],      # 3rd
[ date(2020,2,24), date(2020,3,27) ],     # 4th
[ date(2020,4,21), date(2020,5,22) ],      # 5th
[ date(2020,6,1), date(2020,7,31) ],      # 6th
],

'University' : [
[ date(2019,10,20), date(2019,12,7) ],    # Michaelmas:  2nd to 7th week
[ date(2020,1,19), date(2020,3,14) ],      # Hilary:      1st to 8th week
[ date(2020,4,26), date(2030,6,20) ],     # Trinity:     1st to 4th week
],

}

# Weeks with the following days in them will be excluded from fixtures for everyone

globalExcludedWeeks = [
#date(2019,12,23).isocalendar()[1],
#date(2019,12,30).isocalendar()[1],
#date(2020,1,17).isocalendar()[1],
#date(2020,4,13).isocalendar()[1],
]

# Define the two halves of the season

firstDateOfFirstHalf=date(2019,9,30)
lastDateOfFirstHalf=date(2019,12,20)

firstDateOfSecondHalf=date(2020,1,6)
lastDateOfSecondHalf=date(2020,5,15)

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
        
           if phomeClub == 'Cowley' and 14 < pdate.day < 22 and homeFixturesOnThisDay >= 1:
              return False

        if fdate is not None:    # i.e. a fixture has already been scheduled


#--------------------------------------------------
#          Examine fixtures happening in this week
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

# Check if proposed away team already has a home fixture in this week
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
                for attempt in range(0,150):
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

# Increase score if home team already has an adjacent team playing on this day

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
                  score -= 10

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
            outputs.append(fdate.strftime('%Y-%m-%d (%a)') +" " + fdiv + " " + \
                    '{0: <12}'.format(fhomeClub + " " + str(fhomeTeamNumber))  + " v " + \
                    '{0: <12}'.format(fawayClub + " " + str(fawayTeamNumber)))

        outputs.sort()
        for output in outputs:
            print(output)
    except FileNotFoundError:
        print("ERROR: Pickle file not found",file=sys.stderr)
        pass

#---------------------------------------------------------------------------------------

def main(argv):

       numberOfSimulations = 50
       if len(argv) > 1:
          try:
             numberOfSimulations = int(argv[1])
          except ValueError:
             print ("Argument", argv[1], "is not a valid number of simulations", file=sys.stderr)
             sys.exit(2)
       
       solutionFound = False
       for j in range(0, numberOfSimulations):
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
    main( sys.argv)
