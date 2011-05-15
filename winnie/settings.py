# Typing Speed (in characters per minute)
TYPING_SPEED = 750 # Mine is ~550, 750 is exceedingly high

# Verbosity, the percentage of the time that winnie will 
# look for something to say in response.
VERBOSITY = 15

# LOGSIZE
LOGSIZE = 50

# IRC settings
IRC = (
    # nick first, any alt names after that (also things that people can call her)
    ('winniepooh','winnie','poohbear','thepooh','bear','pooh'),
    ('irc.freenode.net', 6667)    # server
)

IRC_CHANNELS = (
    '#'+IRC[0][0],                     # join the channel with our nickname
#    '#r.trees',
#    '#trees',
#    '#weedit'
)
IRC_CREDENTIALS = {
    'authority':'nickserv',
    'command':'identify %s %s',
    'creds': ('dottru@gmail.com', 'gottolovethe1')
}
# The db connection string
DATABASE = "mysql://winnie:lolhax@localhost/winnie"

# Handler Prefix (for commands %channels, %help, etc)
HANDLER_PREFIX = ':'

# HTTP Address
HTTP_ADDRESS = {
    'host': '0.0.0.0',
    'port': '8090'
}

# Directory paths
PATH = '/home/winnie/projects/winnie'
TEMPLATES_PATH = PATH + '/web/static/'
STATIC_PATH = TEMPLATES_PATH
