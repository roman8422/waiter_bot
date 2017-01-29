import logging

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
        '@Roman',
)  # !! Don't leave that to "CHANGE ME" if you connect your errbot to a chat system !!

BOT_IDENTITY = {
    ## HipChat mode (Comment the above if using this mode)
    'username' : '1_2@chat.btf.hipchat.com',
    'password' : '123qweASD',
    ## Group admins can create/view tokens on the settings page after logging
    ## in on HipChat's website
    'token'    : 'Gu9OWkcnJMufrAwg3sHy8Ali87icGuJhFI6auUeO',
    ## If you're using HipChat server (self-hosted HipChat) then you should set
    ## the endpoint below. If you don't use HipChat server but use the hosted version
    ## of HipChat then you may leave this commented out.
    'endpoint' : 'https://hipchat.test.intra',
    'verify': False,
}

XMPP_CA_CERT_FILE = None
CHATROOM_PRESENCE = ('SPb lunch',
                     '1_spb_lunch',
)
CHATROOM_FN = 'LunchBot'
