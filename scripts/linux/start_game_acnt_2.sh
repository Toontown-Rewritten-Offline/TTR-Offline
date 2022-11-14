#!/bin/sh
cd ../../

export TTR_PLAYCOOKIE=Username2
export TTR_GAMESERVER="127.0.0.1"

/usr/bin/python3 -m toontown.toonbase.ToontownStart
