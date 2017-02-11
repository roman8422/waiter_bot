from errbot import BotPlugin, botcmd
import sys
from random import randrange
from time import sleep


class Waiter(BotPlugin):

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

    def _get_orders(self):
        restaurants = [
            'Токио',
            'Васаби',
        ]

        try:
            d = self['orders']
        except KeyError:
            d = {}
            for restaurant in restaurants:
                d[restaurant] = {}

        self._set_orders(d)
        return(d)

    def _set_orders(self, d):
        self['orders'] = d


    @botcmd()
    def order_add(self, msg, args):
        """Adds new order. Format: !order add restorant[:] 'place order text here'"""

        d = self._get_orders()

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
        self._set_orders(d)

        _return_message = ""
        _return_message += "/me accepted following order:\n"
        _return_message += "From: {}\n".format(msg.frm.nick)
        _return_message += "Restaurant: {}\n".format(_restaurant)
        _return_message += "Order content: {}\n".format(_order_content)

        return _return_message

    @botcmd()
    def order_list(self, msg, args):
        return self.orders_list(msg, args)

    @botcmd()
    def orders_list(self, msg, args):
        """Shows list of orders. Format: !orders list <rest_name | all>"""
        d = self._get_orders()
        _error_msg = "/me says:\n!orders list accepts one argument, {} given\n!orders list <rest_name | all>"

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
        _return_message = "/code\n"
        for _restaurant in _restaurants:
            _return_message += "\----------\n"
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
    def orders_remove(self, msg, args):
        """Clears list of orders. Format: !orders remove <restname | all>"""
        d = self._get_orders()
        _error_msg = "/me says:\n!orders remove accepts one argument, {} given\n!orders remove <rest_name | all>"

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

        _return_message = ''
        for _restaurant in _restaurants:
            _return_message += "/me says:\n"
            d[_restaurant] = {}
            _return_message += "orders for {} has been removed".format(_restaurant)

        self._set_orders(d)

        return _return_message

    @botcmd()
    def rest_add(self, msg, args):
        """Adds new restaurant. Format: !rest add <rest_name>"""

        d = self._get_orders()

        _args_num = len(args.split())
        if _args_num > 1:
            return "!rest add accepts only one argument, {} given\n !rest add <rest_name>".format(_args_num)

        _rest_in_d = False
        for rest in d.keys():
            if args.lower() == rest.lower():
                return '/me says:\nRestaurant {} is in the list already'.format(args)

        if not _rest_in_d:
            d[args] = {}
            self._set_orders(d)
            return '/me says:\nrestaurant {} has been added'.format(args)

    @botcmd()
    def rest_remove(self, msg, args):
        """Removes restaurant from list. Format: !rest remove <rest_name>"""
        d = self._get_orders()
        try:
            d.pop(args)
            self._set_orders(d)
            return "/me says:\nrestaurant {} has been removed from list".format(args)
        except KeyError:
            return "/me says:\n restaurant {} is not in the list".format(args)

    @botcmd()
    def rest_list(self, msg, args):
        """Shows available restaurant. Format: !rest list"""

        self._get_orders()

        _restaurants = self._make_rest_list()
        _keys = ""
        for key in _restaurants:
            _keys += key + '\n'

        _retern_message = '/me says:\nRestaurants list:\n{}'.format(_keys)

        return _retern_message

    @botcmd()
    def select_contact(self, msg, args):
        """Selects a person from order owners. Format: !select contact <rest_name | all>"""
        d = self._get_orders()
        fname = sys._getframe().f_code.co_name.replace('_', ' ')
        _error_msg = "/me says:\n!{func} accepts one argument, {nargs} given\n!{func} <rest_name>"

        if not args:
            return _error_msg.format(func=fname, nargs=0)

        _args_num = len(args.split())
        if _args_num != 1:
            return _error_msg.format(func=fname, nargs=_args_num)

        _restaurant = self._find_rest(args)
        if _restaurant[0] == '/':
            return _restaurant

        if _restaurant == 'all':
            _restaurants = list(d.keys())
        else:
            _restaurants = []
            _restaurants.append(_restaurant)

        _return_message = "/me says"
        for _restaurant in _restaurants:
            l = list(d[_restaurant].keys())
            if len(l) > 0:
                _contact = l[randrange(len(l))]

                _return_message += ("\nToday's contact for {rest} is " + _contact).format(rest=_restaurant)
            else:
                _return_message += '\nNo one has made an order in {rest} yet'.format(rest=_restaurant)

        return _return_message


    @botcmd
    def order_send(self, msg, args):
        caller = "Roman Vrublevskiy"
        try:
            phone_num = Waiter.find_phone_num(caller)
            return phone_num
        except Exception as e:
            return e

    @staticmethod
    def find_phone_num(caller):
        try:
            import contacts
        except ImportError:
            return "You should create contacts.py file with contacts list.\n" \
                   "Ex: contacts=[{'displayName': 'Roman Vrublevskiy', 'mobilePhone': '123456789'}]"

        for contact in contacts.contacts:
            if contact['displayName'] == caller:
                return contact['mobilePhone']
        raise LookupError("Phone number of {} wasn't found in contacts".format(caller))
