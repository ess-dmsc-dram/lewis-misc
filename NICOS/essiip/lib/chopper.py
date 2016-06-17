from nicos.devices.epics import EpicsReadable, pvname, EpicsDevice
from nicos.core import status, Param, Override, Attach, usermethod, Readable, SIMULATION


class DelayedEpicsReadable(EpicsDevice, Readable):
    parameters = {
        'readpv': Param('PV for reading device value',
                        type=pvname, mandatory=False),
    }

    parameter_overrides = {
        'pollinterval': Override(default=0.5)
    }

    pv_parameters = set(('readpv',))

    def doPreinit(self, mode):
        self._pvs = {}
        self._pvctrls = {}

    def doRead(self, maxage=0):
        try:
            return self._get_pv('readpv')
        except KeyError:
            raise RuntimeError('test')

    def setPVName(self, name):
        self._setROParam('readpv', name)
        self._initialise_pvs()


class EssChopper(EpicsDevice, Readable):
    parameters = {
        'pvprefix': Param('PV prefix of the chopper.', type=pvname, mandatory=True)
    }

    attached_devices = {
        'speed': Attach('Speed of the chopper disc', DelayedEpicsReadable),
        'phase': Attach('Phase of the chopper disc', DelayedEpicsReadable),
        'parkposition': Attach('Position in parked state', DelayedEpicsReadable),
        'state': Attach('Current state of the chopper', DelayedEpicsReadable)
    }

    state_map = {
        'init': (status.ERROR, 'Interlocks not fulfilled'),
        'stopped': (status.OK, 'Waiting for commands'),
        'parked': (status.OK, 'Parked'),
        'parking': (status.BUSY, 'Moving to park position'),
        'accelerating': (status.BUSY, 'Adjusting speed to target'),
        'phase_locking': (status.BUSY, 'Acquiring phase lock'),
        'phase_locked': (status.OK, 'Speed and phase locked'),
        'stopping': (status.BUSY, 'Decelerating disc'),
        'idle': (status.OK, 'Disc rotating freely, waiting for command.'),
        'bearings': (status.BUSY, 'Initialising bearings'),
    }

    parameter_overrides = {
        'unit': Override(mandatory=False),
    }

    internal_chopper_fields = {
        'speed_setpoint': 'Spd',
        'phase_setpoint': 'Phs',
        'parkposition_setpoint': 'ParkAng',
        'command': 'CmdS',
    }

    def _get_pv_parameters(self):
        return self.internal_chopper_fields.keys()

    def _get_pv_name(self, pvparam):
        return self.pvprefix + self.internal_chopper_fields[pvparam]

    def doInit(self, mode):
        if mode != SIMULATION:
            self._attached_speed.setPVName(self.pvprefix + 'Spd-RB')
            self._attached_phase.setPVName(self.pvprefix + 'Phs-RB')
            self._attached_state.setPVName(self.pvprefix + 'State')
            self._attached_parkposition.setPVName(self.pvprefix + 'ParkAng-RB')

    def doRead(self, maxage=0):
        return round(self._attached_speed.read(maxage), 2), round(self._attached_phase.read(maxage), 2)

    def doStatus(self, maxage=0):
        return self.state_map[self._attached_state.read()]

    @usermethod
    def interlock(self):
        self._put_pv('command', 'init')

    @usermethod
    def setSpeedAndPhase(self, speed, phase):
        self._put_pv('speed_setpoint', speed)
        self._put_pv('phase_setpoint', phase)
        self._put_pv('command', 'start')

    @usermethod
    def stop(self):
        self._put_pv('command', 'stop')

    @usermethod
    def parkAt(self, position):
        self._put_pv('parkposition_setpoint', position)
        self._put_pv('command', 'park')

    @usermethod
    def coast(self):
        self._put_pv('command', 'unlock')

    @usermethod
    def release(self):
        self._put_pv('command', 'deinit')
