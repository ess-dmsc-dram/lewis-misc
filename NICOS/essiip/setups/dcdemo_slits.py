description = 'Three slit systems'


def get_slit_configuration(slit_number):
    return {
        'slit{}hl'.format(slit_number):
            device('essiip.epics_motor.EpicsMotor',
                   description='Slit {} Horizontal Left'.format(slit_number),
                   fmtstr='%.2f',
                   unit='mm',
                   motorpv='s{}l:m1'.format(slit_number),
                   lowlevel=True,
                   ),
        'slit{}hr'.format(slit_number):
            device('essiip.epics_motor.EpicsMotor',
                   description='Slit {} Horizontal Right'.format(slit_number),
                   fmtstr='%.2f',
                   unit='mm',
                   motorpv='s{}r:m1'.format(slit_number),
                   lowlevel=True,
                   ),
        'slit{}vb'.format(slit_number):
            device('essiip.epics_motor.EpicsMotor',
                   description='Slit {} Vertical Bottom'.format(slit_number),
                   fmtstr='%.2f',
                   unit='mm',
                   motorpv='s{}b:m1'.format(slit_number),
                   lowlevel=True,
                   ),
        'slit{}vt'.format(slit_number):
            device('essiip.epics_motor.EpicsMotor',
                   description='Slit {} Vertical Top'.format(slit_number),
                   fmtstr='%.2f',
                   unit='mm',
                   motorpv='s{}t:m1'.format(slit_number),
                   lowlevel=True,
                   ),
        'slit{}'.format(slit_number):
            device('devices.generic.Slit',
                   description='Slit {}'.format(slit_number),
                   left='slit{}hl'.format(slit_number),
                   right='slit{}hr'.format(slit_number),
                   top='slit{}vt'.format(slit_number),
                   bottom='slit{}vb'.format(slit_number),
                   opmode='offcentered',
                   coordinates='opposite',
                   ),
    }


devices = {}

for i in range(1, 4):
    devices.update(get_slit_configuration(i))
