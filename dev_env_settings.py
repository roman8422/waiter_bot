BOT_ADMINS = (
        '1_1@chat.btf.hipchat.com',
)

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

CHATROOM_FN = 'LunchBot'

BOT_ALT_PREFIXES = ('Err', '@LunchBot',)
