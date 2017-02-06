from errbot import BotPlugin, botcmd

class Waiter(BotPlugin):
    """Bot to take dinner orders"""

    def _rest_empty_error(self):
        return "/me says:\nYou should add some restaurants first. Use following command:\n!rest add <rest_name>\nCheck restaurants list with:\n!rest list"

    def _make_rest_list(self):
        d = self['orders']
        _restaurants = list(d.keys())
        _restaurants.sort()
        return _restaurants

    @botcmd()
    def order_add(self, msg, args):
        """Make your order. Format: !orderadd restorant[:] 'place order text here'"""

        if 'orders' in self.keys():
            d = self['orders']
        else:
            return(self._rest_empty_error())

        _restaurant = args.split(' ')[0].strip(' :')
        _not_in_list = True
        for rest in self._make_rest_list():
            if _restaurant.lower() == rest.lower():
                _not_in_list = False

        if _not_in_list:
            return "/me says:\nDon't know this restaurant. Check spelling or add it with\n!rest add <rest_name>\nCheck restaurants list with:\n!rest list"

        _order_content = args.replace(_restaurant, '')
        _retern_message = ""
        _retern_message += "/me accepted following order:\n"
        _retern_message += "From: {}\n".format(msg.frm.nick)
        _retern_message += "Restaurant: {}\n".format(_restaurant)
        _retern_message += "Order content: {}\n".format(_order_content)

        return _retern_message


    @botcmd()
    def rest_add(self, msg, args):
        d = self['orders']

        _args_num = len(args.split())
        if _args_num > 1:
            return "!rest add accepts only one argument, {} given\n !rest add <rest_name>".format(_args_num)

        _rest_in_d = False
        for rest in d.keys():
            if args.lower() == rest.lower():
                return '/me says:\nrestaurant {} is in list already'.format(args)

        if not _rest_in_d:
            d[args] = {}
            self['orders'] = d
            return '/me says:\nrestaurant {} has been added'.format(args)


    @botcmd()
    def rest_list(self, msg, args):
        if 'orders' not in self.keys():
            return(self._rest_empty_error())
        else:
            _restaurants = self._make_rest_list()
            _keys = ""
            for key in _restaurants:
                _keys += key + '\n'

            return _keys

