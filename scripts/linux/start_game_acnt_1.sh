#!/bin/sh
cd ../../

export TTR_PLAYCOOKIE=Username
export TTR_GAMESERVER="192.168.12.156"

/usr/bin/python2 -m toontown.toonbase.ToontownStart
