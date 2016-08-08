description = 'Chopper cascade with 8 choppers.'


def get_chopper_configuration(chopper_pv_prefix, chopper_number):
    chopper_base_pv = chopper_pv_prefix + str(chopper_number)
    return {
        '{}_speed'.format(chopper_base_pv):
            device('essiip.chopper.EpicsFloatMoveable',
                   pollinterval=0.5,
                   abslimits=(0, 40),
                   description='Speed control of chopper {}'.format(chopper_number),
                   readpv='{}:Spd-RB'.format(chopper_base_pv),
                   writepv='{}:Spd'.format(chopper_base_pv),
                   lowlevel=True),

        '{}_phase'.format(chopper_base_pv):
            device('essiip.chopper.EpicsFloatMoveable',
                   pollinterval=0.5,
                   description='Phase control of chopper {}'.format(chopper_number),
                   readpv='{}:Phs-RB'.format(chopper_base_pv),
                   writepv='{}:Phs'.format(chopper_base_pv),
                   lowlevel=True
                   ),

        '{}_park'.format(chopper_base_pv):
            device('essiip.chopper.EpicsFloatMoveable',
                   pollinterval=0.5,
                   description='Park control of chopper {}'.format(chopper_number),
                   readpv='{}:ParkAng-RB'.format(chopper_base_pv),
                   writepv='{}:ParkAng'.format(chopper_base_pv),
                   lowlevel=True
                   ),

        '{}_state'.format(chopper_base_pv):
            device('devices.epics.EpicsReadable',
                   pollinterval=0.5,
                   description='State information of chopper {}'.format(chopper_number),
                   readpv='{}:State'.format(chopper_base_pv),
                   lowlevel=True
                   ),

        '{}_command'.format(chopper_base_pv):
            device('essiip.chopper.EpicsStringMoveable',
                   description='Command interface of chopper {}'.format(
                       chopper_number),
                   readpv='{}:CmdL'.format(chopper_base_pv),
                   writepv='{}:CmdS'.format(chopper_base_pv),
                   lowlevel=True
                   ),

        chopper_base_pv:
            device('essiip.chopper.EssChopper',
                   description='Chopper {}'.format(chopper_number),
                   speed=['{}_speed'.format(chopper_base_pv)],
                   phase=['{}_phase'.format(chopper_base_pv)],
                   parkposition=['{}_park'.format(chopper_base_pv)],
                   state=['{}_state'.format(chopper_base_pv)],
                   command=['{}_command'.format(chopper_base_pv)]
                   )
    }


devices = {}

for i in range(1, 9):
    devices.update(get_chopper_configuration('chopper', i))
