"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.marketplace = marketplace
        self.carts = carts
        self.wait_time = retry_wait_time
        self.carts_ids = []

    def run(self):
        for cart in self.carts:
            self.carts_ids.append(self.marketplace.new_cart())
            for action in cart:
                if action["type"] == "add":
                    i = 0
                    while i < action["quantity"]:
                        ret = self.marketplace.add_to_cart( \
                        self.carts_ids[len(self.carts_ids) - 1], action["product"])

                        if ret:
                            i += 1
                        else:
                            sleep(self.wait_time)

                else:
                    for _ in range(action["quantity"]):
                        self.marketplace.remove_from_cart( \
                        self.carts_ids[len(self.carts_ids) - 1], action["product"])

        for cart in self.carts_ids:
            aux = self.marketplace.place_order(cart)
            for produs in aux:
                print(self.name, "bought", produs)
