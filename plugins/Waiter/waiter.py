from errbot import BotPlugin, botcmd

class Waiter(BotPlugin):
    """Bot to take dinner orders"""

    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello, waiter!"
