class Error(Exception):
    pass


class UnexpectedEventError(Error):
    pass


class State(object):
    """A state in the state machine.

    """

    def __init__(self, name, on_enter=None, on_exit=None):
        self._name = name
        self._on_enter = on_enter
        self._on_exit = on_exit
        self._transitions = []
        self._event = None

    @property
    def name(self):
        return self._name

    def __add__(self, other):
        """`other` is the event triggering a transition.

        """

        if not isinstance(other, Event):
            raise Error(
                'expected an Event instance, but got {}'.format(repr(other)))

        self._event = other

        return self

    def __rshift__(self, other):
        """`other` is the state to transition to.

        """

        if not isinstance(other, State):
            raise Error(
                'expected a State instance, but got {}'.format(repr(other)))

        self._transitions.append((self._event, other))

        return self

    def __repr__(self):
        transitions = self._transitions

        return 'State(name={}, transitions={})'.format(self._name,
                                                       transitions)


class Event(object):
    """An event in the state machine.

    """


    def __init__(self, cls):
        self.cls = cls
        self.guard = None
        self.action = None

    def __getitem__(self, key):
        """`key` is the transition guard.

        """

        if not callable(key):
            raise Error('expected a callable guard, but got {}'.format(key))

        self.guard = key

        return self

    def __truediv__(self, other):
        """`other` is the transition action.

        """

        if not callable(other):
            raise Error( 'expected a callable action, but got {}'.format(other))

        self.action = other

        return self

    def __repr__(self):
        name = self.cls.__name__

        if self.guard is None:
            guard = None
        else:
            guard = self.guard.__name__

        if self.action is None:
            action = None
        else:
            action = self.action.__name__

        return 'Event(name={}, guard={}, action={})'.format(name, guard, action)


class StateMachine(object):
    """A state machine.

    """

    def __init__(self, transitions):
        self._transitions = transitions
        self._current_state = self._transitions[0]

    def process_event(self, event):
        """Process given event `event`. Raises an `UnexpectedEventError` if
        given event was unexpected.

        """

        print('Current state: {}, Event to process: {}'.format(
            self._current_state.name,
            event))

        # # Is the event expected?
        # try:
        #     transition = self._current_state.events[type(event)]
        # except KeyError:
        #     raise UnexpectedEventError()
        #
        # if not transition.guard(event):
        #     return
        #
        # transition.action(event)
        #
        # self._current_state = transition.to_state

    def __str__(self):
        return self._current_state.name
