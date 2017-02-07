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

    def _find_rest(self, input):
        input = input.strip(' :')
        _not_in_list = True
        for rest in self._make_rest_list():
            if input.lower() == rest.lower():
                return(rest)
            if input.lower() == 'all':
                return 'all'

        if _not_in_list:
            return "/me says:\nDon't know this restaurant. Check spelling or add it with\n!rest add <rest_name>\nCheck restaurants list with:\n!rest list"


    @botcmd()
    def order_add(self, msg, args):
        """Make your order. Format: !orderadd restorant[:] 'place order text here'"""

        if 'orders' in self.keys():
            d = self['orders']
        else:
            return(self._rest_empty_error())

        _input = args.splitlines()
        _restaurant_input = _input[0].split(' ')[0]
        _restaurant = self._find_rest(_restaurant_input)

        if _restaurant[0] == '/':
            return _restaurant

        # remove spaces in lines
        _stripped_input = []
        for line in _input:
            _stripped_input.append(line.strip())

        _order_content = '\n'.join(_stripped_input)
        # remove restaurant from input
        _order_content = _order_content.replace(_restaurant_input, '').strip()

        d[_restaurant][msg.frm.nick] = _order_content
        self['orders'] = d

        _return_message = ""
        _return_message += "/me accepted following order:\n"
        _return_message += "From: {}\n".format(msg.frm.nick)
        _return_message += "Restaurant: {}\n".format(_restaurant)
        _return_message += "Order content: {}\n".format(_order_content)

        return _return_message

    @botcmd()
    def orders_list(self, msg, args):
        d = self['orders']
        _error_msg = "/me says:\n!orders list accepts one argument, {} given\n!orders list <rest_name>"

        if not args:
            return _error_msg.format(0)

        _args_num = len(args.split())
        if _args_num != 1:
            return _error_msg.format(_args_num)

        _restaurant = self._find_rest(args)
        if _restaurant[0] == '/':
            return _restaurant

        if _restaurant == 'all':
            _restaurants = list(d.keys())
        else:
            _restaurants = []
            _restaurants.append(_restaurant)

        _ident = "  "
        _return_message = ''
        for _restaurant in _restaurants:
            _return_message += "---\n"
            _return_message += _restaurant + ":\n"
            _num = 0
            for key, val in d[_restaurant].items():
                _num += 1
                _return_message += 'Гость ' + str(_num) + ' (' + key + ')\n'
                if '\n' in val:
                    for line in val.splitlines():
                        _return_message += _ident + line.strip() + '\n'
                else:
                    _return_message += _ident + val + '\n'

        return _return_message

    @botcmd()
    def order_list_all(self):
        d = self['orders']
        for key in d.keys():
            return key

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
    def rest_remove(self, msg, args):
        """Remove restaurand from list. Format: !rest remove <restaurant>"""
        d = self['orders']
        try:
            d.pop(args)
            self['orders'] = d
            return "/me says:\nrestaurant {} has been removed from list".format(args)
        except KeyError:
            return "/me says:\n restaurant {} is not in the list".format(args)

    @botcmd()
    def rest_list(self, msg, args):

        if 'orders' not in self.keys():
            return(self._rest_empty_error())

        _restaurants = self._make_rest_list()
        _keys = ""
        for key in _restaurants:
            _keys += key + '\n'

        _retern_message = '/me says:\nRestaurants list:\n{}'.format(_keys)

        return _retern_message
