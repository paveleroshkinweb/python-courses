from exceptions.socket_closed import SocketIOError


def _lock_method(method):
    if getattr(method, '_is_locked', False):
        raise Exception('Method already locked!')

    def inner(self, *args, **kwargs):
        with self._lock:
            if self.closed:
                raise SocketIOError(f"Can't {method.__name__} due to closed socket")
            return method(self, *args, **kwargs)
    inner.__name__ = method.__name__
    inner._is_locked = True
    return inner


def _lock_cls(cls, methodnames, lockfactory):
    init = cls.__init__

    def newinit(self, *args, **kwargs):
        init(self, *args, **kwargs)
        self._lock = lockfactory()

    cls.__init__ = newinit
    for methodname in methodnames:
        old_method = getattr(cls, methodname)
        new_method = _lock_method(old_method)
        setattr(cls, methodname, new_method)
    return cls


def lock(methodnames, lockfactory):
    return lambda cls: _lock_cls(cls, methodnames, lockfactory)

