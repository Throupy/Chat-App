"""Cooldown function decorator."""
import time


class Cooldown:
    """Cooldown decorator."""

    def __init__(self, timeout):
        """Initialise cooldown class."""
        self.timeout = timeout
        self.calltime = time.time() - timeout
        self.func = None
        self.obj = None

    def __call__(self, *args, **kwargs):
        """When the decorated function runs."""
        if self.func is None:
            self.func = args[0]
            return self
        now = time.time()
        if now - self.calltime >= self.timeout:
            self.calltime = now
            if self.obj is None:
                return self.func.__call__(*args, **kwargs)
            else:
                return
                self.func.__get__(self.obj, self.objtype)(*args, **kwargs)

    def __get__(self, obj, objtype):
        """Get the decorator."""
        self.obj = obj
        self.objtype = objtype
        return self

    @property
    def remaining(self):
        """Get the remaining time left on the cooldown."""
        now = time.time()
        delta = now - self.calltime
        if delta >= self.timeout:
            return 0
        return round(self.timeout - delta)

    @remaining.setter
    def remaining(self, value):
        """Set the remaining time left on the cooldown."""
        self.calltime = round(time.time() - self.timeout + value)
