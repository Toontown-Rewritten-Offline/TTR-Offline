#!/bin/sh
cd ../../

export TTR_PLAYCOOKIE="Username"
export TTR_GAMESERVER="127.0.0.1"

python3 -m toontown.toonbase.ToontownStart
