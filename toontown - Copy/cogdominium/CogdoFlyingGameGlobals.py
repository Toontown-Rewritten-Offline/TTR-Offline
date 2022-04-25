from direct.showbase import PythonUtil
from enum import Enum
from panda3d.core import VBase4, Vec3, Point3
from .CogdoUtil import VariableContainer, DevVariableContainer
#AI = VariableContainer()
#AI.GameActions = PythonUtil.Enum(('LandOnWinPlatform', 'WinStateFinished', 'GotoWinState', 'HitWhirlwind', 'HitLegalEagle', 'HitMinion', 'DebuffInvul', 'RequestEnterEagleInterest', 'RequestExitEagleInterest', 'RanOutOfTimePenalty', 'Died', 'Spawn', 'SetBlades', 'BladeLost'))
class AI:
    VariableContainer().BroadcastPeriod = 0.3
    VariableContainer().SafezoneId2DeathDamage = {2000: 1,
     1000: 2,
     5000: 4,
     4000: 8,
     3000: 12,
     9000: 16}
    VariableContainer().SafezoneId2WhirlwindDamage = {2000: 1,
     1000: 2,
     5000: 4,
     4000: 8,
     3000: 12,
     9000: 16}
    VariableContainer().SafezoneId2LegalEagleDamage = {2000: 2,
     1000: 4,
     5000: 8,
     4000: 16,
     3000: 24,
     9000: 32}
    VariableContainer().SafezoneId2MinionDamage = {2000: 1,
     1000: 2,
     5000: 4,
     4000: 8,
     3000: 12,
     9000: 16}
    class GameActions(Enum):
        LandOnWinPlatform = 1
        WinStateFinished = 2
        GotoWinState = 3
        HitWhirlwind = 4
        HitLegalEagle = 5
        HitMinion = 6
        DebuffInvul = 7
        RequestEnterEagleInterest = 8
        RequestExitEagleInterest = 9
        RanOutOfTimePenalty = 10
        Died = 11
        Spawn = 12
        SetBlades = 13
        BladeLost = 14
Camera = VariableContainer()
Camera.Angle = 12.5
Camera.Distance = 20
Camera.LookAtToonHeightOffset = 1.0
Camera.LeewayX = 0.5
Camera.MinLeewayZ = 0.5
Camera.MaxLeewayZ = 15.0
Camera.CatchUpRateZ = 3.0
Camera.LevelBoundsFactor = (0.6, 1.0, 0.9)
Camera.AlphaBetweenToon = 0.35
Camera.SpinRadius = 9.0
Camera.MaxSpinAngle = 20.0
Camera.MaxSpinX = 16.0
#Gameplay = VariableContainer()
class Gameplay:
    SecondsUntilGameOver = 60.0 * 3.0
    TimeRunningOutSeconds = 45.0
    IntroDurationSeconds = 24.0
    FinishDurationSeconds = 10.0
    GatherableFlashTime = 1.0
    ToonAcceleration = {'forward': 40.0,
     'backward': 40.0,
     'turning': 40.0,
     'boostUp': 15.0,
     'fall': 10.0,
     'activeDropDown': 20.0,
     'activeDropBack': 40.0,
     'fan': 80.0}
    ToonDeceleration = {'forward': 5.0,
     'backward': 3.0,
     'turning': 10.0,
     'fan': 25.0}
    ToonVelMax = {'forward': 15.0,
     'backward': 6.0,
     'turning': 10.0,
     'boost': 5.5,
     'fall': 10.0,
     'fallNoFuel': 70.0,
     'fan': 55.0}
    ToonTurning = {'turningSpeed': 15.0,
     'maxTurningAngle': 45.0}
    RayPlatformCollisionThreshold = 0.2
    UseVariableFanPower = True
    FanMaxPower = 1.0
    FanMinPower = 0.4
    FanCollisionTubeRadius = 4.0
    FanCollisionTubeHeight = 35.0
    FanStreamerMinDuration = 0.2
    FanStreamerMaxDuration = 0.5
    WhirlwindCollisionTubeHeight = 100
    WhirlwindCollisionTubeRadius = 4.0
    WhirlwindMoveBackDist = 15.0
    WhirlwindSpinTime = 1.0
    WhirlwindMoveBackTime = 0.5
    FlyingMinionCollisionRadius = 2.5
    FlyingMinionCollisionHeightOffset = 5.0
    FlyingMinionFloatOffset = 1.0
    FlyingMinionFloatTime = 1.0
    WalkingMinionCollisionRadius = 2.5
    WalkingMinionCollisionHeightOffset = 2.0
    MemoCollisionRadius = 1.5
    MemoSpinRate = 60.0
    DoesToonDieWithFuel = True
    SafezoneId2LaffPickupHealAmount = {2000: 1,
     1000: 2,
     5000: 4,
     4000: 8,
     3000: 12,
     9000: 16}
    InvulBuffTime = 15.0
    InvulBlinkTime = 5.0
    InvulSingleBlinkTime = 0.5
    PropellerCollisionRadius = 3.0
    PropellerRespawnTime = 5.0
    FuelBurnRate = 0.1
    DepleteFuelStates = ['FlyingUp']
    FuelNormalAmt = 1.0
    FuelLowAmt = 0.66
    FuelVeryLowAmt = 0.33
    RefuelPropSpeed = 5.0
    OverdrivePropSpeed = 2.5
    NormalPropSpeed = 1.5
    TargetedWarningLabelScale = 3.5
    TargetedWarningSingleBlinkTime = 0.25
    TargetedWarningBlinkTime = 3.0
    HitKnockbackDist = 15.0
    HitKnockbackTime = 0.5
    HitCooldownTime = 2.0
    #Gameplay.FuelStates = PythonUtil.Enum(('FuelNoPropeller', 'FuelEmpty', 'FuelVeryLow', 'FuelLow', 'FuelNormal'))
    #Gameplay.BackpackStates = PythonUtil.Enum(('Normal', 'Targeted', 'Attacked', 'Refuel'))
    class FuelStates(Enum):
        FuelNoPropeller = 1
        FuelEmpty = 2
        FuelVeryLow = 3
        FuelLow = 4
        FuelNormal = 5
    class BackpackStates(Enum):
        Normal = 1
        Targeted = 2
        Attacked = 3
        Refuel = 4
    BackpackRefuelDuration = 4.0
    BackpackState2TextureName = {BackpackStates.Normal: 'tt_t_ara_cfg_propellerPack',
     BackpackStates.Targeted: 'tt_t_ara_cfg_propellerPack_eagleTarget',
     BackpackStates.Attacked: 'tt_t_ara_cfg_propellerPack_eagleAttack',
     BackpackStates.Refuel: 'tt_t_ara_cfg_propellerPack_flash'}
    MinionDnaName = 'bf'
    MinionScale = 0.8
Gui = VariableContainer()
Gui.FuelNumBladesPos2D = (-0.005, -0.017)
Gui.FuelNumBladesScale = 0.07
Gui.FuelPos2D = (-1.19, -0.24)
Gui.NumBlades2FuelColor = {0: (0.9, 0.15, 0.15, 1.0),
 1: (0.9, 0.15, 0.15, 1.0),
 2: (0.9, 0.9, 0.15, 1.0),
 3: (0.25, 0.65, 0.25, 1.0)}
Gui.FuelNormalColor = (0.25, 0.65, 0.25, 1.0)
Gui.FuelLowColor = (0.9, 0.9, 0.15, 1.0)
Gui.FuelVeryLowColor = (0.9, 0.15, 0.15, 1.0)
Gui.ProgressPos2D = (1.15, -0.15)
Gui.ProgressHPos2D = (0, 0.82)
Gui.MarkerScale = 0.03
Gui.LocalMarkerScale = 0.0425
LegalEagle = VariableContainer()
LegalEagle.EagleAndTargetDistCameraTrackThreshold = 30.0
LegalEagle.InterestConeLength = 80
LegalEagle.InterestConeOffset = 5.0
LegalEagle.InterestConeAngle = 60
LegalEagle.DamageSphereRadius = 3.0
LegalEagle.OnNestDamageSphereRadius = 6.0
LegalEagle.VerticalOffset = -6.0
LegalEagle.PlatformVerticalOffset = 0.0
LegalEagle.LiftOffTime = 0.5
LegalEagle.LiftOffHeight = 5.0
LegalEagle.LockOnSpeed = 3.0
LegalEagle.LockOnTime = 2.0
LegalEagle.ExtraPostCooldownTime = 2.0
LegalEagle.LockOnDistanceFromNest = -7.0
LegalEagle.ChargeUpTime = 0.75
LegalEagle.RetreatToNestTime = 2.0
LegalEagle.PreAttackTime = 0.75
LegalEagle.PostAttackTime = 0.5
LegalEagle.RetreatToSkyTime = 1.25
LegalEagle.EagleAttackShouldXCorrect = True
LegalEagle.AttackRateOfChangeVec = Vec3(1.0, 1.0, 2.0)
LegalEagle.PostAttackLength = 5.0
LegalEagle.CooldownTime = 5.0
LegalEagle.PostCooldownHeightOffNest = 40.0
Dev = DevVariableContainer('cogdoflying')
Dev.DisableDeath = False
Dev.InfiniteFuel = False
Dev.InfiniteTimeLimit = True
Dev.Invincibility = False
Dev.NoLegalEagleAttacks = False
Audio = VariableContainer()
Audio.Cutoff = 75.0
Audio.MusicFiles = {'normal': 'phase_4/audio/bgm/MG_cannon_game.ogg',
 'end': 'phase_4/audio/bgm/FF_safezone.ogg',
 'waiting': 'phase_4/audio/bgm/m_match_bg2.ogg',
 'invul': 'phase_4/audio/bgm/MG_CogThief.ogg',
 'timeRunningOut': 'phase_7/audio/bgm/encntr_suit_winning_indoor.ogg'}
Audio.SfxFiles = {'propeller': 'phase_4/audio/sfx/TB_propeller.ogg',
 'propeller_damaged': 'phase_5/audio/sfx/tt_s_ara_cfg_propellers_damaged.ogg',
 'fan': 'phase_4/audio/sfx/target_wind_float_loop.ogg',
 'getMemo': 'phase_4/audio/sfx/MG_maze_pickup.ogg',
 'getLaff': 'phase_4/audio/sfx/avatar_emotion_laugh.ogg',
 'getRedTape': 'phase_5/audio/sfx/SA_red_tape.ogg',
 'invulBuff': 'phase_4/audio/sfx/ring_get.ogg',
 'invulDebuff': 'phase_4/audio/sfx/ring_miss.ogg',
 'refuel': 'phase_5/audio/sfx/LB_receive_evidence.ogg',
 'bladeBreak': 'phase_5/audio/sfx/tt_s_ara_cfg_propellerBreaks.ogg',
 'popupHelpText': 'phase_3/audio/sfx/GUI_balloon_popup.ogg',
 'collide': 'phase_3.5/audio/sfx/AV_collision.ogg',
 'whirlwind': 'phase_5/audio/sfx/tt_s_ara_cfg_whirlwind.ogg',
 'toonInWhirlwind': 'phase_5/audio/sfx/tt_s_ara_cfg_toonInWhirlwind.ogg',
 'death': 'phase_5/audio/sfx/tt_s_ara_cfg_toonFalls.ogg',
 'legalEagleScream': 'phase_5/audio/sfx/tt_s_ara_cfg_eagleCry.ogg',
 'toonHit': 'phase_5/audio/sfx/tt_s_ara_cfg_toonHit.ogg',
 'lose': 'phase_4/audio/sfx/MG_lose.ogg',
 'win': 'phase_4/audio/sfx/MG_win.ogg',
 'refuelSpin': 'phase_4/audio/sfx/clock12.ogg',
 'cogDialogue': 'phase_3.5/audio/dial/COG_VO_statement.ogg',
 'toonDialogue': 'phase_3.5/audio/dial/AV_dog_long.ogg'}
#Level = VariableContainer()
class Level:
    #GatherableTypes = PythonUtil.Enum(('Memo', 'Propeller', 'LaffPowerup', 'InvulPowerup'))
    #ObstacleTypes = PythonUtil.Enum(('Whirlwind', 'Fan', 'Minion'))
    #PlatformTypes = PythonUtil.Enum(('Platform', 'StartPlatform', 'EndPlatform'))
    class GatherableTypes(Enum):
        Memo = 1
        Propeller = 2
        LaffPowerup = 3
        InvulPowerup = 4
    class ObstacleTypes(Enum):
        Whirlwind = 1
        Fan = 2
        Minion = 3
    class PlatformTypes(Enum):
        Platform = 1
        StartPlatform = 2
        EndPlatform = 3
    PlatformType2SpawnOffset = {PlatformTypes.Platform: 2.5,
     PlatformTypes.StartPlatform: 5.0,
     PlatformTypes.EndPlatform: 5.0}
    QuadLengthUnits = 170
    QuadVisibilityAhead = 1
    QuadVisibilityBehind = 0
    StartPlatformLength = 55
    StartPlatformHeight = 20
    EndPlatformLength = 55
    EndPlatformHeight = 0
    FogColor = VBase4(0.18, 0.19, 0.32, 1.0)
    RenderFogStartFactor = 0.22
    GatherablesDefaultSpread = 1.0
    NumMemosInRing = 6
    PropellerSpinDuration = 10.0
    QuadsByDifficulty = {1: (2, 4, 5),
     2: (1, 3, 7),
     3: (6, 8)}
    DifficultyOrder = {2000: (1, 1, 1, 2, 1),
     1000: (1, 1, 2, 2, 1),
     5000: (1, 2, 1, 2, 2),
     4000: (1, 2, 1, 2, 3, 2),
     3000: (1, 2, 2, 3, 2, 3),
     9000: (2, 3, 2, 3, 2, 3, 2)}
    AddSparkleToPowerups = True
    AddParticlesToStreamers = True
    IgnoreLaffPowerups = False
    SpawnLaffPowerupsInNests = True
    LaffPowerupNestOffset = Point3(0.0, 2.0, 3.0)
    PlatformName = '*lightFixture'
    GatherablesPathName = 'gatherables_path*'
    GatherablesRingName = 'gatherables_ring_path*'
    PropellerName = '*propeller_loc*'
    PowerupType2Loc = {GatherableTypes.LaffPowerup: 'laff_powerup_loc*',
     GatherableTypes.InvulPowerup: 'invul_powerup_loc*'}
    PowerupType2Model = {GatherableTypes.LaffPowerup: 'legalEagleFeather',
     GatherableTypes.InvulPowerup: 'redTapePickup'}
    PowerupType2Node = {GatherableTypes.LaffPowerup: 'feather',
     GatherableTypes.InvulPowerup: 'redTape'}
    GatherableType2TextureName = {GatherableTypes.LaffPowerup: 'tt_t_ara_cfg_legalEagleFeather_flash',
     GatherableTypes.InvulPowerup: 'tt_t_ara_cfg_redTapePickup_flash',
     GatherableTypes.Memo: 'tt_t_ara_csa_memo_flash',
     GatherableTypes.Propeller: 'tt_t_ara_cfg_propellers_flash'}
    WhirlwindName = '*whirlwindPlaceholder'
    WhirlwindPathName = '_path*'
    StreamerName = '*streamerPlaceholder'
    MinionWalkingPathName = '*minion_walking_path*'
    MinionFlyingPathName = '*minion_flying_path*'
    LegalEagleNestName = '*eagleNest_loc*'
Dev.WantTempLevel = True
Dev.DevQuadsOrder = (1, 2, 3, 4, 5, 6, 7, 8)