configfile = open('private_client.prc', 'r')
configlines = configfile.read()
configlines = configlines.encode('utf-8')
data = 'CONFIGFILE = %s' % configlines + '\n'

dcfile = open('ttrp.dc', 'r')
dclines = dcfile.read()
dclines = dclines.encode('utf-8')
data += 'DCFILE = %s' % dclines

finalfile = open('PrivacyMatters.py', 'a+')
finallines = finalfile.write(data)