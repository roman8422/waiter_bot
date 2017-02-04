import logging
from pathlib import Path

from prod_creds import BOT_IDENTITY

if Path('dev_creds.py').is_file():
    from dev_creds import BOT_IDENTITY

## BOT_IDENTITY should be imported from separate file that's not checked out to git
## Example:
#BOT_IDENTITY = {
#    ## HipChat mode (Comment the above if using this mode)
#    'username' : '1_2@chat.btf.hipchat.com',
#    'password' : '123qweASD',
#    ## Group admins can create/view tokens on the settings page after logging
#    ## in on HipChat's website
#    'token'    : 'Gu9OWkcnJMufrAwg3sHy8Ali87icGuJhFI6auUeO',
#    ## If you're using HipChat server (self-hosted HipChat) then you should set
#    ## the endpoint below. If you don't use HipChat server but use the hosted version
#    ## of HipChat then you may leave this commented out.
#    'endpoint' : 'https://hipchat.test.intra',
#    'verify': False,
#}


# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

#BACKEND = 'Text'  # Errbot will start in text mode (console only mode) and will answer commands from there.
BACKEND = 'Hipchat'

BOT_DATA_DIR = r'/local/errbot-root/data'
BOT_EXTRA_PLUGIN_DIR = '/local/errbot-root/plugins'

BOT_LOG_FILE = r'/local/errbot-root/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = (
        '1_1@chat.btf.hipchat.com',
)

XMPP_CA_CERT_FILE = None
CHATROOM_PRESENCE = ('SPb lunch',
)
CHATROOM_FN = 'LunchBot'

# BOT_EXTRA_PLUGIN_DIR = '/local/errbot-plugins/'
BOT_ALT_PREFIXES = ('Err', '@LunchBot',)
