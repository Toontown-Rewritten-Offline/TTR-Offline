from toontown.toonfest.DistributedToonfestTrampolineActivity import DistributedToonfestTrampolineActivity

class DistributedToonfestVictoryTrampolineActivity(DistributedToonfestTrampolineActivity):

    def __init__(self, cr, doJellyBeans = True, doTricks = False, texture = None):
        DistributedToonfestTrampolineActivity.__init__(self, cr, doJellyBeans, doTricks, 'phase_13/maps/tt_t_ara_pty_trampolineVictory.jpg')
