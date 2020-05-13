"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size = queue_size_per_producer
        self.producers = []
        self.prod_id_last = 0
        self.prod_id_lock = Lock()
        self.carts = []
        self.cart_id_last = 0
        self.cart_id_lock = Lock()
        self.remove_product_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers.append([])
        self.prod_id_lock.acquire()
        aux = self.prod_id_last
        self.prod_id_last += 1
        self.prod_id_lock.release()
        return aux

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.producers[int(producer_id)]) >= self.queue_size:
            return False
        self.producers[int(producer_id)].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts.append([])
        self.cart_id_lock.acquire()
        aux = self.cart_id_last
        self.cart_id_last += 1
        self.cart_id_lock.release()
        return aux

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for i in range(self.prod_id_last):
            if product in self.producers[i]:
                self.producers[i].remove(product)
                self.carts[cart_id].append((product, i))
                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        for cart in self.carts[cart_id]:
            if cart[0] == product:
                self.producers[cart[1]].append(product)
                self.carts[cart_id].remove((product, cart[1]))
                return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        aux = []
        for cart in self.carts[cart_id]:
            aux.append(cart[0])
        return aux
