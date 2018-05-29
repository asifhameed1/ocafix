#!/usr/bin/env python3

# Author David.Robson
# 2018-05-27 Created

from datetime import date,timedelta
import pickle
import sys

#---------------------------------------------------------------------------------------
def main():

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
#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
