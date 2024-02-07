from panda3d.core import loadPrcFileData, StringStream
import PrivacyMatters
import builtins
import argparse

prc = PrivacyMatters.CONFIGFILE
loadPrcFileData('config', prc)

builtins.dcStream = StringStream()
dc = PrivacyMatters.DCFILE
dcStream.setData(dc)

parser = argparse.ArgumentParser()
parser.add_argument('--ai', action='store_true', help='Start the AI server.')
parser.add_argument('--uberdog', action='store_true', help='Start the UberDOG server.')
parser.add_argument('--dedicated', action='store_true', help='Start the Dedicated server.')
parser.add_argument('--game', action='store_true', help='Start the games client.')
args = parser.parse_args()

if args.dedicated:
    from toontown.toonbase import DedicatedServerStart
elif args.uberdog:
    from toontown.uberdog import ServiceStartUD
elif args.ai:
    from toontown.ai import ServiceStartAI
elif args.game:
    from toontown.toonbase import ToontownStart
