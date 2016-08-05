from nicos.devices.epics import EpicsReadable, EpicsMoveable, pvname, EpicsDevice
from nicos.core import status, Param, Override, Attach, usermethod, HasLimits, Moveable, SIMULATION, Value, tupleof


class EpicsFloatMoveable(EpicsMoveable):
    """
    Handles EPICS devices which can set and read a float value, but without limits.
    """
    valuetype = float


class EpicsStringMoveable(EpicsMoveable):
    """
    Handles EPICS devices which can set and read a string value.
    """
    valuetype = str


class EssChopper(Moveable):
    attached_devices = {
        'speed': Attach('Speed of the chopper disc.', EpicsMoveable),
        'phase': Attach('Phase of the chopper disc', EpicsMoveable),
        'parkposition': Attach('Position in parked state', EpicsMoveable),
        'state': Attach('Current state of the chopper', EpicsReadable),
        'command': Attach('Command PV of the chopper', EpicsMoveable)
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
        'fmtstr': Override(default='%.2f %.2f'),
        'unit': Override(mandatory=False),
    }

    hardware_access = False
    valuetype = tupleof(float, float)

    def doRead(self, maxage=0):
        return [self._attached_speed.read(maxage), self._attached_phase.read(maxage)]

    def doStart(self, pos):
        self._attached_speed.move(pos[0])
        self._attached_phase.move(pos[1])
        self._attached_command.move('start')

    def doStop(self):
        self._attached_command.move('stop')

    # def doReadAbslimits(self):
    #    return [(0.0, 40.0), (0.0, 360.0)]

    def doStatus(self, maxage=0):
        return self.state_map[self._attached_state.read()]

    @usermethod
    def initialize(self):
        self._attached_command.move('init')

    @usermethod
    def deinitialize(self):
        self._attached_command.move('deinit')

    @usermethod
    def parkAt(self, position):
        self._attached_parkposition.move(position)
        self._attached_command.move('park')

    @usermethod
    def unlock(self):
        self._attached_command.move('unlock')
