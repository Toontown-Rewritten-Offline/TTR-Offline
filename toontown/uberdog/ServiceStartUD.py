from panda3d.core import *
from direct.showbase import PythonUtil
import builtins
import os
import argparse

# Create directory trees to prevent database crashes
os.makedirs('astron/databases/astrondb', exist_ok = True) 
os.makedirs('astron/mongo/astrondb', exist_ok = True) 

''' WIP
if not ConfigVariableBool('auto-start-server', False):
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-channel', help='The base channel that the server may use.')
    parser.add_argument('--max-channels', help='The number of channels the server may use.')
    parser.add_argument('--stateserver', help="The control channel of this UD's designated State Server.")
    parser.add_argument('--astron-ip', help="The IP address of the Astron Message Director to connect to.")
    parser.add_argument('--eventlogger-ip', help="The IP address of the Astron Event Logger to log to.")
    args = parser.parse_args()

    localconfig = ''
    if args.base_channel: localconfig += 'air-base-channel %s\n' % args.base_channel
    if args.max_channels: localconfig += 'air-channel-allocation %s\n' % args.max_channels
    if args.stateserver: localconfig += 'air-stateserver %s\n' % args.stateserver
    if args.astron_ip: localconfig += 'air-connect %s\n' % args.astron_ip
    if args.eventlogger_ip: localconfig += 'eventlog-host %s\n' % args.eventlogger_ip
    loadPrcFileData('Command-line', localconfig)
WIP '''

loadPrcFile('config/dev.prc')

# Settings
print('ServiceStartUD: Loading settings.')
from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

# Configure/Start UberDog Server
class game:
    name = 'uberDog'
    process = 'server'
builtins.game = game

from otp.ai.AIBaseGlobal import *

from toontown.uberdog.ToontownUberRepository import ToontownUberRepository
simbase.air = ToontownUberRepository(config.ConfigVariableInt('air-base-channel', 1000000).getValue(),
                                     config.ConfigVariableInt('air-stateserver', 4002).getValue())
host = config.ConfigVariableString('air-connect', '127.0.0.1').getValue()
port = 7199
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)
simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception:
    import traceback
    info = traceback.format_exc()
    simbase.air.writeServerEvent('uberdog-exception', simbase.air.getAvatarIdFromSender(), simbase.air.getAccountIdFromSender(), info) 
    raise
