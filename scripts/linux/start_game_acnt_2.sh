#!/bin/sh
cd ../../

export TTR_PLAYCOOKIE=Username2
export TTR_GAMESERVER="192.168.12.156"

/usr/bin/python2 -m toontown.toonbase.ToontownStart
