description = 'Simulated chopper.'

devices = dict(
    speed=device('essiip.chopper.DelayedEpicsReadable',
                 description='',
                 unit='Hz',
                 readpv='', lowlevel=True),
    phase=device('essiip.chopper.DelayedEpicsReadable',
                 description='',
                 unit='deg',
                 readpv='', lowlevel=True),
    parkposition=device('essiip.chopper.DelayedEpicsReadable',
                        description='',
                        unit='deg',
                        readpv='', lowlevel=True),
    state=device('essiip.chopper.DelayedEpicsReadable',
                 description='',
                 unit='',
                 readpv='', lowlevel=True),

    chopper=device('essiip.chopper.EssChopper',
                   description='Chopper',
                   pvprefix='SIM:',
                   speed=['speed'],
                   phase=['phase'],
                   parkposition=['parkposition'],
                   state=['state'],
                   ),
)
