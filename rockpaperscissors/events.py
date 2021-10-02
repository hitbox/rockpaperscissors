from collections import defaultdict

_events = defaultdict(list)

def subscribe(event, func):
    _events[event].append(func)

def emit(event, *data):
    for func in _events.get(event, []):
        func(event, *data)
