# ocafix

ocafix is a tool to schedule OCA fixtures.  After the initial parameters are defined, it then performs
Monte-Carlo simulations until it finds a fixture list that meets the constraints.  The fixtures are
then written to stdout.  A python pickle file (fixtures.pickle) is also created so that further analysis
can be undertaken.

The code is wriiten in Python3 and uses standard libraries.

## Current constraints

1. Fixtures lie with the two halves of the season
2. Fixtures occur on the club night of the home team
3. Fixtures are only between teams in the same division
4. Teams in the same division play each other twice; once at home and once away
5. Teams do not play each other twice during the same half of the season
6. Teams from the same club play each other at the beginning of the season halves
7. No team plays more than one match in the same week (except for the University)
8. No fixtures scheduled for the day after Kidlington
9. No fixtures scheduled for the day after The Witney Congress
9. No fixtures scheduled for Easter Bank Holiday
10. No fixtures scheduled for the day of the Peter Well's simultaneous event
11. No fixtures scheduled for the day of the Cowley Blitz
12. Fixtures between teams from the same club are scheduled at the begining of each half of the season
13. No matches to be scheduled outside ranges specified for clubs. Currently Abingdon School terms and University terms, excluding Michaelmas 1st week for initial preparation and Michaelmas and Trinity 8th week for exams.
14. Clubs do not have more than a specified number of fixtures at home on the same day (currently 2 for all clubs)
15. Cowley does not have more than 1 fixtures at home on the third Monday of the month
16. Witney does not have adjacent teams playing on the same night.
