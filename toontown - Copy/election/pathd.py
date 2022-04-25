# Embedded file name: toontown.election.pathd
import sys
from .InvasionPathDataAI import pathfinder
while True:
    navFrom, navTo, radius = eval(input())
    path = pathfinder.planPath(navFrom, navTo, radius)
    print(path)
    sys.stdout.flush()