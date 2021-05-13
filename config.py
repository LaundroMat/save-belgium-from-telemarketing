class Config(object):
    DEBUG = True
    TEST = True


class TestConfig(Config):
    TEST = True
    DEBUG = False


class DevConfig(Config):
    DEBUG = True


class PrdConfig(Config):
    pass
