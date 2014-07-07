"""A quick and dirty state machine inspired by the rails plugin, acts_as_state_machine.
When implementing this on a model, the model is expected to have a character field in the database called "state."
Next, come up with a few states that a model can be in and initialize a machine object with those states.
Now you need to define the way a model moves from one state to the next.
You do this by calling the 'event' method on the machine object.

The first event argument defines the name of the method which will transition you to the next (to) state.
The next argument is a dictionary defining what the current state must be in order to transition to the ending state.
So, in the example, an Entry can transition from any state (the '*') to the draft state by calling entry.draft().
An entry can also transition from the 'draft' or 'hidden' state to the 'published' state which is enforced when calling entry.publish().

You can see what state a model object is in by calling <model_object>.state but sometimes it is more desirable
to explicitly ask if a model object is in a particular state; this is done by the calling <model_object>.is_published()
or <model_object>.is_draft().
All the code does is prefix "is_" to the "to" state which returns a True or False if the model is in that particular state.

Author:
    santuri
Posted:
    May 4, 2008
Language:
    Python
Django Version:
    .96
Tags:
    state-machine
Score:
    4 (after 4 ratings)
URL:
    http://djangosnippets.org/snippets/737/
"""

from django.db import models
from django.utils.functional import curry

class MachineError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Machine():
    def __init__(self, model, states, **kwargs):
        self.model = model
        try:
            initial_state = kwargs.pop('initial')
        except:
            raise MachineError("Must give an initial state")
        self._set_initial_or_retrieve_state(initial_state)
        self.states = []
        self.state_triggers = {}
        for state in states:
            if isinstance(state, str):
                self.states.append(state)
            elif isinstance(state, dict):
                state_name = state.keys()[0]
                self.states.append(state_name)
                self.state_triggers[state_name] = state[state_name]
        self.states = tuple(self.states)

    def _extract_from_state(self, kwargs):
        try:
            coming_from = kwargs.pop('from')
        except KeyError:
            raise MachineError("Missing 'from'; must transtion from a state")

        if isinstance(coming_from, str):
            if coming_from not in self.states and coming_from != '*':
                raise MachineError("from: '%s' is not a registered state" % coming_from)
        elif isinstance(coming_from, list):
            for state in coming_from:
                if state not in self.states:
                    raise MachineError("from: '%s' is not a registered state" % coming_from)
        return coming_from

    def _extract_to_state(self, kwargs):
        try:
            going_to = kwargs.pop('to')
        except KeyError:
            raise MachineError("Missing 'to'; must transtion to a state")

        if going_to not in self.states:
            raise MachineError("to: '%s' is not a registered state" % coming_from)
        return going_to

    def _set_initial_or_retrieve_state(self, initial):
        try:
            self.state = self._update_state_from_model()
        except AttributeError:
            raise MachineError("The model for this state machine needs a state field in the database")
        if not self.model.state:
            self.state = self._update_model(initial, False)

    def _update_state_from_model(self):
        self.state = self.model.state

    def _update_model(self, state, save=True):
        self.model.state = state
        if save:
            self.model.save()
        self.state = self.model.state

    def end_state(self, **kwargs):
        self._update_state_from_model()
        state = kwargs.get('state')
        from_states = kwargs.get('from_states')
        from_states = from_states if from_states != "*" else [self.state]
        if self.state in from_states:
            if state in self.state_triggers and 'enter' in self.state_triggers[state]:
                self.state_triggers[state]['enter']()
            self._update_model(state)
            return self.state
        else:
            raise MachineError("Cannot transition to %s from %s" % (state, self.state))

    def is_state(self, state, *args):
        self._update_state_from_model()
        return self.state == state

    def event(self, end_state, transition):
        coming_from = self._extract_from_state(transition)
        going_to = self._extract_to_state(transition)
        is_state = "is_%s" % going_to
        setattr(self.model, end_state, curry(self.end_state, state=going_to, from_states=coming_from))
        setattr(self.model, is_state, curry(self.is_state, going_to))


class Entry(models.Model):
    state = models.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)

        states = (
            'draft',
            'hidden',
            {'published': {'enter': self.dothing}},
        )

        self.machine = Machine(self, states, initial='draft')

        self.machine.event('draft', {'from': '*', 'to': 'draft'})
        self.machine.event('publish', {'from': ['draft', 'hidden'], 'to': 'published'})
        self.machine.event('hide', {'from': '*', 'to': 'hidden'})

    def dothing(self):
        print "Someone called me"

# >>> e=Entry()
# >>> e.is_published()
# False
# >>> e.is_draft()
# True
# >>> e.publish()
# Someone called me
# 'published'
# >>> e.is_published()
# True
# >>>
