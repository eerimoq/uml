#!/usr/bin/env python3
#
# Life of a working man.
#
# The working man has two states; sleeping and awake. Monday to friday
# he goes to bed at 11 PM and wakes up early by the alarm. In the
# weekend he sleeps until well rested.
#

from time import ctime

from uml.state_machine import State
from uml.state_machine import Event
from uml.state_machine import StateMachine


class Alarm(object):
    """The alarm event.

    """

    def __init__(self, day, time):
        self.day = day
        self.time = time

    def __repr__(self):
        return '{}(day={}, time={})'.format(type(self).__name__,
                                            self.day,
                                            self.time)


class WellRested(object):
    """The well rested event.

    """


class ElevenPm(object):
    """The 11 PM event.

    """


class WorkingMan(StateMachine):

    def __init__(self):
        awake = State('Awake', on_exit=self.yawns)
        sleeping = State('Sleeping', on_enter=self.fell_asleep)
        transitions = [
            sleeping + Event(Alarm) [self.is_working_day] / self.on_alarm >> awake,
            sleeping + Event(WellRested) / self.on_well_rested >> awake,
            awake + Event(ElevenPm) >> sleeping
        ]
        super(WorkingMan, self).__init__(transitions)
        self.number_of_days_passed = 0

    def yawns(self):
        print('Yawns!')

    def fell_asleep(self):
        self.number_of_days_passed += 1

    def on_alarm(self, event):
        print('Eating breakfast {}!'.format(event.time))

    def on_well_rested(self, _):
        print('Well rested, eating brunch!')

    def is_working_day(self, event):
        if event.day % 7 in range(5):
            print('Working day!')
            return True
        else:
            print('Weekend!')
            return False

    def __str__(self):
        return '{} number of days passed.'.format(self.number_of_days_passed)


def main():
    working_man = WorkingMan()

    for day in range(10):
        print('======================= Day {} ======================='.format(day))
        working_man.process_event(Alarm(day, 2 * day))
        working_man.process_event(ElevenPm())

    print(working_man)


if __name__ == '__main__':
    main()
