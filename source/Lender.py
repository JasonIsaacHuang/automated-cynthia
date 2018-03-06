class Lender:


    """
    Constructor for Lender Object.
    Holds all the data needed to be able to collect product data from a single source

    Args:
        source: An object handle for a particular source
        lender: The name of a lender available from the given source
        lender_url: The url that will contain product information from a given source
    """
    def __init__(self, source, lender, lender_url):
        self._source = source
        self._lender = lender
        self._lender_url = lender_url
        self._products = None

    def __str__(self):
        return self._lender + ' at ' + str(self._source)

    """
    Establishes all of the products available for a given lender from a given source
    
    Returns:
        No return value
    """
    def _prepare_products(self):

        if self._products == None:
            self._products = self._source.products(self._lender_url)

    """
    Returns all products offered by the given lender from a given source
    
    Returns:
        A dictionary of products to urls of the offered products
    """
    def products(self):

        self._prepare_products()

        return self._products

    """
    Returns a product instance from the given product name
    
    Args:
        product_name: The name of the product
    
    Returns:
        A single instance of an object
    """
    def product(self, product_name):

        self._prepare_products()
        if product_name in self._products.keys():
            return self._products[product_name]
        else:
            return None
        pass