from errbot import BotPlugin, botcmd

class Waiter(BotPlugin):
    """Bot to take dinner orders"""

    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello, waiter!"

    def rest_empty_error(self):
        return "/me says:\nYou should add some restaurants first. Use following command:\n!rest add <rest_name>\nCheck restaurants list with:\n!rest list"

    @botcmd()
    def order_add(self, msg, args):
        """Make your order. Format: !orderadd restorant[:] 'place order text here'"""

        _restaurant = args.split(' ')[0].strip(' :')
        _order_content = args.replace(_restaurant, '')
        _retern_message = ""
        _retern_message += "/me accepted following order:\n"
        _retern_message += "From: {}\n".format(msg.frm.nick)
        _retern_message += "Restaurant: {}\n".format(_restaurant)
        _retern_message += "Order content: {}\n".format(_order_content)

        return _retern_message
