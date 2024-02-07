#!/usr/bin/env sudo /Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9
cd ../../

export TTR_PLAYCOOKIE="Username"
export TTR_GAMESERVER="127.0.0.1"

python3 -m toontown.toonbase.ToontownStart
