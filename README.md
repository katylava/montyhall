montyhallsim.py
===============

    Usage: montyhallsim.py --doors 3 --iterations 100 --verbose

    Options:
      -h, --help            show this help message and exit
      -d DOORS, --doors=DOORS
                            Number of doors for game
      -i ITERATIONS, --iterations=ITERATIONS
                            Number of iterations to trial
      -v, --verbose


Sample Output
-------------

    > ./montyhallsim.py -d 10 -i 100000
    =================================================
    SWITCHED: 50052 games, 5676 cars, 44376 goats
    KEPT: 49948 games, 4958 cars, 44990 goats
    Switched win ratio: 0.1134
    Kept win ratio: 0.0993
