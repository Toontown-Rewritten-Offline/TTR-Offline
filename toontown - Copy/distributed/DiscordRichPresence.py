import time
from ctypes import * # Used to interact with DLL
from direct.task import Task # Used to manage the Callback timer

class DiscordRichPresence:
    zone2imgdesc = { # A dict of ZoneID -> An image and a description
        1000: ["donalds-dock", "In Donald's Dock"],
        1100: ["donalds-dock", "On Barnacle Boulevard"],
        1200: ["donalds-dock", "On Seaweed Street"],
        1300: ["donalds-dock", "On Lighthouse Lane"],

        2000: ["toontown-central", "In Toontown Central"],
        2100: ["toontown-central", "On Silly Street"],
        2200: ["toontown-central", "On Loopy Lane"],
        2300: ["toontown-central", "On Punchline Place"],

        3000: ["the-brrrgh", "In The Brrrgh"],
        3100: ["the-brrrgh", "On Walrus Way"],
        3200: ["the-brrrgh", "On Sleet Street"],
        3300: ["the-brrrgh", "On Polar Place"],
        
        4000: ["minnies-melodyland", "In Minnie's Melodyland"],
        4100: ["minnies-melodyland", "On Alto Avenue"],
        4200: ["minnies-melodyland", "On Baritone Boulevard"],
        4300: ["minnies-melodyland", "On Tenor Terrace"],

        5000: ["daisy-gardens", "In Daisy Gardens"],
        5200: ["daisy-gardens", "On Daisy Drive"],
        5300: ["daisy-gardens", "On Tulip Terrace"],
        5400: ["daisy-gardens", "On Sunflower Street"],

        6000: ["acorn-acres", "At Acorn Acres"],

        8000: ["toontown-speedway", "In Goofy's Speedway"],

        9000: ["donalds-dreamland", "In Donald's Dreamland"],
        9100: ["donalds-dreamland", "On Lullaby Lane"],
        9200: ["donalds-dreamland", "On Pajama Place"],

        10000: ["bossbot-hq", "At Bossbot HQ"],
        10100: ["bossbot-hq", "In The CEO Clubhouse"],
        10200: ["bossbot-hq", "In The CEO Clubhouse"],
        10500: ["bossbot-hq", "In The Front Three"],
        10600: ["bossbot-hq", "In The Middle Six"],
        10700: ["bossbot-hq", "In The Back Nine"],

        11000: ["sellbot-hq", "At Sellbot HQ"],
        11100: ["sellbot-hq", "In The VP Lobby"],
        11200: ["sellbot-hq", "In The Sellbot HQ Factory Exterior"],
        11500: ["sellbot-hq", "In The Sellbot Factory"],
        
        12000: ["cashbot-hq", "At Cashbot HQ"],
        12100: ["cashbot-hq", "In The CFO Lobby"],
        12500: ["cashbot-hq", "In The Cashbot Coin Mint"],
        12600: ["cashbot-hq", "In The Cashbot Dollar Mint"],
        12700: ["cashbot-hq", "In The Cashbot Bullion Mint"],

        13000: ["lawbot-hq", "At Lawbot HQ"],
        13100: ["lawbot-hq", "In The CJ Lobby"],
        13200: ["lawbot-hq", "In The DA's Office Lobby"],
        13300: ["lawbot-hq", "In The Lawbot Office A"],
        13400: ["lawbot-hq", "In The Lawbot Office B"],
        13500: ["lawbot-hq", "In The Lawbot Office C"],
        13600: ["lawbot-hq", "In The Lawbot Office D"],

        14000: ["tutorial", "In The Toontorial"],

        16000: ["estate", "At A Toon Estate"],

        17000: ["minigames", "In The Minigames Area"],

        18000: ["party", "At A Toon Party"],
   }
    
    def __init__(self):
        self.CodeHandle = cdll.LoadLibrary("SDK.dll") # Load the RP code
        self.CodeHandle.DLLMain()
        self.UpdateTask = None
        self.details = "Loading" # The writing next to the photo
        self.image = "logo" #The main photo
        self.imageTxt = "OSToontown" # Hover text for the main photo
        self.smallLogo = "globe" # Small photo in corner
        self.state = "" # Displayed underneath details - used for boarding groups
        self.smallTxt = "Loading" # null this out
        self.PartySize = 0
        self.MaxParty = 0

    def stopBoarding(self):  #Boarding groups :D
        self.PartySize = 0
        self.state = ""
        self.MaxParty = 0
        self.setData()

    def AllowBoarding(self, size):
        self.state = "In A Boarding Group"
        self.PartySize = 1
        self.MaxParty = size
        self.setData()

    def setBoarding(self, size): # Sets how many members are in a boarding group
        self.PartySize = size
        self.setData()

    def setData(self): # Manually update all vars
        self.CodeHandle.DoCallbacks()
        details = self.details
        image = self.image
        imageTxt = self.imageTxt
        smallLogo = self.smallLogo
        smallTxt = self.smallTxt
        state = self.state
        party = self.PartySize
        maxSize = self.MaxParty
        self.CodeHandle.SetData(details.encode('utf_8'), state.encode('utf_8'), smallLogo.encode('utf_8'), smallTxt.encode('utf_8'), image.encode('utf_8'), imageTxt.encode('utf_8'), maxSize, party)

    def DoCallbacks(self, task): # Recieves any messages from discord and handles them
        self.CodeHandle.DoCallbacks()
        return task.again

    def UpdateTasks(self, task):
        self.UpdateTask = True
        self.setData()
        return task.again

    def AvChoice(self): # Call in pick-a-toon
        self.image = "logo"
        self.details = "Picking-A-Toon"
        self.setData()

    def Launching(self): # Call When loading game - toontownstart
        self.image = "logo"
        self.details = "Loading"
        self.setData()

    def Making(self): # Call in make-a-toon
        self.image = "logo"
        self.details = "Making A Toon"
        self.setData()

    def StartTasks(self): # Call JUST before base.run() in toontown-start
        taskMgr.doMethodLater(10, self.UpdateTasks, 'UpdateTask')
        taskMgr.doMethodLater(0.016, self.DoCallbacks, 'RPC-Callbacks')

    def setZone(self,Zone): # Set image and text based on the zone
        if not isinstance(Zone, int):
            return
        Zone -= Zone % 100
        data = self.zone2imgdesc.get(Zone,None)
        if data:
            self.image = data[0]
            self.details = data[1]
            self.setData()
        else:
            print("Error: Zone Not Found!")

    def setDistrict(self,Name): # Set the image text the district name
        self.smallTxt = Name
