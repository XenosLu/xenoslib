from .common import RestartSelfIfUpdated

class SingletonWithArgs:
    """带参数的单例模式, 通过继承使用，需放到第一继承位"""
    def __new__(cls, *args, **kwargs):
        arg = '%s%s' % (args, kwargs)
        if not hasattr(cls, '_instances'):
            cls._instances = {}
        if not cls._instances.get(arg):
            cls._instances[arg] = super().__new__(cls)
        return cls._instances[arg]

