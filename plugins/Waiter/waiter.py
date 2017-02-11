from errbot import BotPlugin, botcmd
import sys
from random import randrange


class Waiter(BotPlugin):

    def _check_for_bad_arguments(self, args, func=False, n_args=1, accepts_all=False):
        if not func:
            raise SyntaxError("Function is not passed in")
        func_str = func.__name__.replace("_", " ")

        _error_msg = "/me says:\n" \
                     "!{func} accepts {n_args} argument{s}, {args_given} given\n" \
                     "{docstring}"

        s = "s"
        if n_args == 1:
            s = ""

        _args_num = len(args.split())
        if _args_num == 0 and accepts_all:
            return 0

        if _args_num != n_args:
            raise SyntaxError(_error_msg.format(
                func=func_str,
                n_args=n_args,
                s=s,
                args_given=_args_num,
                docstring=func.__doc__)
            )

    def _get_rest_from_input(self, input, accepts_all=False):
        input = input.strip(" :")
        _not_in_list = True
        for rest in self._get_orders().keys():
            if input.lower() == rest.lower():
                return(rest)
            if input.lower() == "all":
                return "all"

        if len(input) == 0 and accepts_all:
            return "all"
        if _not_in_list:
            return "/me says:\n" \
                   "Don't know this restaurant. " \
                   "Check spelling or add it with\n" \
                   "!rest add <rest_name>\n" \
                   "Check restaurants list with:\n" \
                   "!rest list"

    def _get_orders(self):
        restaurants = [
            "Токио",
            "Васаби",
        ]

        try:
            d = self["orders"]
        except KeyError:
            d = {}

        for restaurant in restaurants:
            if restaurant not in d.keys():
                d[restaurant] = {}

        self._set_orders(d)
        return(d)

    def _set_orders(self, d):
        self["orders"] = d


    @botcmd()
    def order_add(self, msg, args):
        """Adds new order. Format: !order add restorant[:] 'place order text here'"""

        d = self._get_orders()

        _input = args.splitlines()
        _restaurant_input = _input[0].split(" ")[0]
        _restaurant = self._get_rest_from_input(_restaurant_input)

        if _restaurant[0] == "/":
            return _restaurant

        # remove spaces in lines
        _stripped_input = []
        for line in _input:
            _stripped_input.append(line.strip())

        _order_content = "\n".join(_stripped_input)
        # remove restaurant from input
        _order_content = _order_content.replace(_restaurant_input, "").strip()

        d[_restaurant][msg.frm.nick] = _order_content
        self._set_orders(d)

        _return_message = "/me accepted following order:\n" \
                        "From: {nick}\n" \
                        "Restaurant: {rest}\n" \
                        "Order content: {content}\n".format(
                            nick=msg.frm.nick,
                            rest=_restaurant,
                            content=_order_content,
                        )

        return _return_message

    @botcmd()
    def orders_list(self, msg, args):
        """Alias for !order list"""
        return self.order_list(msg, args)

    @botcmd()
    def order_list(self, msg, args):
        """Shows list of orders. Format: !order list [rest_name=all]"""

        try:
            self._check_for_bad_arguments(args, func=self.order_list, n_args=1, accepts_all=True)
        except SyntaxError as e:
            return str(e)

        try:
            return self._generate_order_list(args)
        except SyntaxError as e:
            return e

    def _generate_order_list(self, args, for_rest=False):
        d = self._get_orders()

        _restaurant = self._get_rest_from_input(args, accepts_all=True)
        if _restaurant[0] == "/":
            raise SyntaxError(_restaurant)

        if _restaurant == "all":
            _restaurants = list(d.keys())
        else:
            _restaurants = []
            _restaurants.append(_restaurant)

        _ident = "  "
        if not for_rest:
            _return_message = "/code\n"
        else:
            _return_message = ""
        for rest in _restaurants:
            if not for_rest:
                _return_message += "\----------\n"
                _return_message += rest + ":\n"
            _num = 0
            for name, order in d[rest].items():
                _num += 1
                _return_message += "Гость " + str(_num)
                if not for_rest:
                    _return_message += " (" + name + ")"
                _return_message += "\n"
                if "\n" in order:
                    for line in order.splitlines():
                        _return_message += _ident + line.strip() + "\n"
                else:
                    _return_message += _ident + order + "\n"

        return _return_message

    @botcmd()
    def orders_remove(self, msg, args):
        """Alias for !order remove"""
        return self.order_remove(msg, args)

    @botcmd()
    def order_remove(self, msg, args):
        """Clears list of orders. Format: !order remove <restname | all>"""
        d = self._get_orders()
        try:
            self._check_for_bad_arguments(args, func=self.order_remove, n_args=1)
        except SyntaxError as e:
            return str(e)

        _restaurant = self._get_rest_from_input(args)
        if _restaurant[0] == "/":
            return _restaurant

        if _restaurant == "all":
            _restaurants = list(d.keys())
        else:
            _restaurants = []
            _restaurants.append(_restaurant)

        _return_message = "/me says:\n"
        for _restaurant in _restaurants:
            d[_restaurant] = {}
            _return_message += "orders for {} have been removed\n".format(_restaurant)

        self._set_orders(d)

        return _return_message

    @botcmd()
    def rest_add(self, msg, args):
        """Adds new restaurant. Format: !rest add <rest_name>"""

        d = self._get_orders()
        try:
            self._check_for_bad_arguments(args, func=self.rest_add, n_args=1)
        except SyntaxError as e:
            return str(e)

        for rest in d.keys():
            if args.lower() == rest.lower():
                return "/me says:\nRestaurant {} is in the list already".format(args)

        d[args] = {}
        self._set_orders(d)
        return "/me says:\nrestaurant {} has been added".format(args)

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

        d = self._get_orders()
        _rests = [k for k in d.keys()]
        _rests.sort()
        _rests_str = "\n".join(_rests)

        _return_message = "/me says:\nRestaurants list:\n{}".format(_rests_str)

        return _return_message

    @botcmd()
    def select_contact(self, msg, args):
        """Selects a person from order owners. Format: !select contact <rest_name | all>"""
        d = self._get_orders()

        try:
            self._check_for_bad_arguments(args, func=self.select_contact, n_args=1)
        except SyntaxError as e:
            return str(e)

        _restaurant = self._get_rest_from_input(args)
        if _restaurant[0] == "/":
            return _restaurant

        if _restaurant == "all":
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
                _return_message += "\nNo one has made an order in {rest} yet".format(rest=_restaurant)

        return _return_message


    @botcmd
    def order_send(self, msg, args):
        try:
            self._check_for_bad_arguments(args, func=self.select_contact, n_args=1)
        except SyntaxError as e:
            return str(e)

        _restaurant = self._get_rest_from_input(args)
        if _restaurant[0] == "/":
            raise SyntaxError(_restaurant)
        if _restaurant != "Токио":
            return "Sorry, just Токио for now"
        caller = "Roman Vrublevskiy"
        try:
            phone_num = Waiter.find_phone_num(caller)
        except Exception as e:
            return e
        try:
            return self._generate_order_list(args, for_rest=True)
        except SyntaxError as e:
            return e

    @staticmethod
    def find_phone_num(caller):
        try:
            import contacts
        except ImportError:
            return "You should create contacts.py file with contacts list.\n" \
                   "Ex: contacts=[{'displayName': 'Roman Vrublevskiy', 'mobilePhone': '123456789'}]"

        for contact in contacts.contacts:
            if contact["displayName"] == caller:
                return contact["mobilePhone"]
        raise LookupError("Phone number of {} wasn't found in contacts".format(caller))
