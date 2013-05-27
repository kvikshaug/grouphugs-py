SERVER = 'localhost'
PORT = 6667
NICKS = ['test']
CHANNELS = ['#test']
MODULES = {
    'confession': {},
    'operator': {
        'operators': [
            'foo'
            ]
        },
    'seen': {},
    'logger': {}
}
DATABASE_URI = 'driver://user:pass@host/database'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s: %(message)s\n'
        },
        'verbose': {
            'format': '\n%(levelname)s (%(name)s) %(asctime)s\n%(pathname)s:%(lineno)d in %(funcName)s\n%(message)s\n'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'grouphugs.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}
