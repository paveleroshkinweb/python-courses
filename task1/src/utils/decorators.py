from exceptions.socket_closed import SocketIOError


def check_if_socket_closed(methodnames):

    def _check_method(method):
        if getattr(method, 'is_checking', False):
            raise Exception('Method already checking!')

        def inner(self, *args, **kwargs):
            if self.closed:
                raise SocketIOError(f"Can't {method.__name__} due to closed socket")
            return method(self, *args, **kwargs)

        inner.__name__ = method.__name__
        inner.is_checking = True
        return inner

    def _check_cls(cls, methodnames):
        for methodname in methodnames:
            old_method = getattr(cls, methodname)
            new_method = _check_method(old_method)
            setattr(cls, methodname, new_method)
        return cls

    return lambda cls: _check_cls(cls, methodnames)
