import requests
import base64

class BigCommerceError(Exception):
	pass

class BigCommerceResponseError(Exception):
    def __init__(self, http_response, content):
        self.http_response = http_response
        self.content = content

class Connection(object):
	
	def __init__(self, domain, api_user, api_key):
		self.domain = domain
		self.api_user = api_user
		self.api_key = api_key
		self.http = requests.Session()
		self.base_url = self.domain+'/api/v2/'
        self.http.headers.update(self.headers)

	def handle_response(self, response):
		pass
	
	@property
	def headers(self):
		""" Returns default headers, by setting the Content-Type, Accepts,
		User-Agent and Authorization headers. """
		auth = base64.b64encode(self.api_user + ':' + self.api_key)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth,
            'User-Agent': 'python-bigcommerce v{0}'.format(__version__)
        }
        return headers
    
	def delete(self, url, params=None):
	    """ Executes an HTTP DELETE request for the given URL.
	
	        ``params`` should be a dictionary
	    """
	    response = self.http.delete(url,
	                                params=params,
	                                **self.requests_params)
	    return self.process(response)
	
	def get(self, url, data=None):
	    """ Executes an HTTP GET request for the given URL.
	
	        ``data`` should be a dictionary of url parameters
	    """
	    response = self.http.get(url,
	                             headers=self.headers,
	                             params=data,
	                             **self.requests_params)
	    return self.process(response)
	
	def post(self, url, body=None):
	    """ Executes an HTTP POST request for the given URL. """
	    response = self.http.post(url,
	                              headers=self.headers,
	                              data=body,
	                              **self.requests_params)
	
	    return self.process(response)
	
	def put(self, url, data=None, body=None):
	    """ Executes an HTTP PUT request for the given URL. """
	    response = self.http.put(url,
	                             headers=self.headers,
	                             data=body,
	                             params=data,
	                             **self.requests_params)
	
	    return self.process(response)
	
	def process(self, response):
	    try:
	        code = response.status_code
	        body = response.json()
	        return Response(code, body, response.content, response)
	    except ValueError:
	        raise BigCommerceResponseError(response, response.content)


class BigCommerce(object):
    """ 
    """
    def __init__(self, domain=None, api_user=None, api_key=None):
		if not domain:
			try:
				self.api_key = os.environ['BIGCOMMERCE_DEFAULT_DOMAIN']
			except KeyError:
				raise BigCommerceError('No domain or BIGCOMMERCE_DEFAULT_DOMAIN given')


		if not api_key:
			try:
				self.api_key = os.environ['BIGCOMMERCE_API_KEY']
			except KeyError:
				raise BigCommerceError('No BIGCOMMERCE_API_KEY given')
		else:
			self.api_key = api_key
		
		self.api_version = 'v2'
		
		args = (self.base_url, self.api_key)
		
 		kwargs = dict(version=api_version)
 		self.orders = Orders(*args, **kwargs)
#  		self.account = Account(*args, **kwargs)
#  		self.output = Output(*args, **kwargs)
#  		self.input = Input(*args, **kwargs)
#  		self.report = None



class Orders(HTTPBackend):
    """ Contains all API methods relating to Orders."""
    def __init__(self, *args, **kwargs):
        kwargs['resource_name'] = 'inputs'
        super(Input, self).__init__(*args, **kwargs)
        
    def filter(self, params):
	   return self.get(self.base_url + '/orders.json')








# 
# 
# """
# This module provides an object-oriented wrapper around the BigCommerce V2 API
# for use in Python projects or via the Python shell.
# 
# """
# 
# import httplib2
# import base64
# import json
# import socks
# 
# API_HOST = 'http://store.mybigcommerce.com'
# API_PATH = '/api/v2'
# API_USER = 'admin'
# API_KEY  = 'yourpasswordhere'
# HTTP_PROXY = None
# HTTP_PROXY_PORT = 80
# 
# class Connection(object):
# 	host      = API_HOST
# 	base_path = API_PATH
# 	user 	  = API_USER
# 	api_key   = API_KEY
# 	http_proxy = HTTP_PROXY
# 	http_proxy_port = HTTP_PROXY_PORT
# 
# 	def handle_response(self, response):
# 		pass
# 
# 	def request_json(self, method, path, data=None):
# 		response, content = self.request(method, path, data)
# 		if response.status == 200 or response.status == 201:
# 			return json.loads(content)
# 		else:
# 			print response
# 			raise Exception(response.status)
# 
# 	def build_request_headers(self):
# 		auth = base64.b64encode(self.user + ':' + self.api_key)
# 		return { 'Authorization' : 'Basic ' + auth, 'Accept' : 'application/json' }
# 
# 	def request(self, method, path, body=None):
# 		if self.http_proxy is not None:
# 			proxy = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, self.http_proxy, self.http_proxy_port)
# 			http = httplib2.Http(proxy_info=proxy)
# 		else:
# 			http = httplib2.Http()
# 		url = self.host + self.base_path + path
# 		headers = self.build_request_headers()
# 		if body: headers['Content-Type'] = 'application/json'
# 		return http.request(url, method, headers=headers, body=body)
# 
# class Resource(object):
# 	"""Base class representing BigCommerce resources"""
# 
# 	client = Connection()
# 
# 	def __init__(self, fields=None):
# 		self.__dict__ = fields or dict()
# 
# class Time(Resource):
# 	"""Tests the availability of the API."""
# 
# 	@classmethod
# 	def get(self):
# 		"""Returns the current time stamp of the BigCommerce store."""
# 		return self.client.request_json('GET', '/time')
# 
# class Products(Resource):
# 	"""The collection of products in a store"""
# 
# 	@classmethod
# 	def get(self):
# 		"""Returns list of products"""
# 		products_list = self.client.request_json('GET', '/products')
# 		return [Product(product) for product in products_list]
# 
# 	@classmethod
# 	def get_by_id(self, id):
# 		"""Returns an individual product by given ID"""
# 		product = self.client.request_json('GET', '/products/' + str(id))
# 		return Product(product)
# 
# class Product(Resource):
# 	"""An individual product"""
# 
# 	def update(self):
# 		"""Updates local changes to the product"""
# 		body = json.dumps(self.__dict__)
# 		product = self.client.request_json('PUT', '/products/' + str(self.id), body)
# 
# 	def delete(self):
# 		"""Deletes the product"""
# 		response, content = self.client.request('DELETE', '/products/' + str(self.id))
# 
# class Brands(Resource):
# 	"""Brands collection"""
# 
# 	@classmethod
# 	def get(self):
# 		"""Returns list of brands"""
# 		brands_list = self.client.request_json('GET', '/brands')
# 		return [Brand(brand) for brand in brands_list]
# 
# 	@classmethod
# 	def get_by_id(self, id):
# 		"""Returns an individual brand by given ID"""
# 		product = self.client.request_json('GET', '/brands/' + str(id))
# 		return Product(product)
# 
# class Brand(Resource):
# 	"""An individual brand"""
# 
# 	def create(self):
# 		"""Creates a new brand"""
# 		body = json.dumps(self.__dict__)
# 		brand = self.client.request_json('PUT', '/brands', body)
# 
# 	def update(self):
# 		"""Updates local changes to the brand"""
# 		body = json.dumps(self.__dict__)
# 		brand = self.client.request_json('PUT', '/brands/' + str(self.id), body)
# 		print brand['name']
# 
# 	def delete(self):
# 		"""Deletes the brand"""
# 		response, content = self.client.request('DELETE', '/brands/' + str(self.id))
# 
# class Customers(Resource):
# 	"""Customers collection"""
# 
# 	@classmethod
# 	def get(self):
# 		"""Returns list of customers"""
# 		customers = self.client.request_json('GET', '/customers')
# 		return [Customer(customer) for customer in customers]
# 
# 	@classmethod
# 	def get_by_id(self, id):
# 		"""Returns an individual customer by given ID"""
# 		customer = self.client.request_json('GET', '/customers/' + str(id))
# 		return Customer(customer)
# 
# class Customer(Resource):
# 	"""An individual customer"""
# 
# 	def create(self):
# 		"""Creates a new customer"""
# 		body = json.dumps(self.__dict__)
# 		customer = self.client.request_json('PUT', '/customers', body)
# 
# 	def update(self):
# 		"""Updates local changes to the customer"""
# 		body = json.dumps(self.__dict__)
# 		customer = self.client.request_json('PUT', '/customers/' + str(self.id), body)
# 
# 	def delete(self):
# 		"""Deletes the customer"""
# 		response, content = self.client.request('DELETE', '/customers/' + str(self.id))
# 
# class Orders(Resource):
# 	"""Orders collection"""
# 
# 	@classmethod
# 	def get(self, fields=None):
# 		"""Returns list of orders"""
# 		orders = self.client.request_json('GET', '/orders', fields)
# 		return [Order(order) for order in orders]
# 
# 	@classmethod
# 	def get_by_id(self, id):
# 		"""Returns an individual order by given ID"""
# 		order = self.client.request_json('GET', '/orders/' + str(id))
# 		return Order(order)
# 
# class Order(Resource):
# 	"""An individual order"""
# 
# 	def create(self):
# 		"""Creates a new order"""
# 		body = json.dumps(self.__dict__)
# 		order = self.client.request_json('PUT', '/orders', body)
# 
# 	def update(self):
# 		"""Updates local changes to the order"""
# 		body = json.dumps(self.__dict__)
# 		order = self.client.request_json('PUT', '/orders/' + str(self.id), body)
# 
# 	def delete(self):
# 		"""Deletes the order"""
# 		response, content = self.client.request('DELETE', '/orders/' + str(self.id))
# 
# class OptionSets(Resource):
# 	"""Option sets collection"""
# 
# 	@classmethod
# 	def get(self):
# 		"""Returns list of option sets"""
# 		optionsets = self.client.request_json('GET', '/optionsets')
# 		return [OptionSet(optionset) for optionset in optionsets]
# 
# 	@classmethod
# 	def get_by_id(self, id):
# 		"""Returns an individual option set by given ID"""
# 		optionset = self.client.request_json('GET', '/optionsets/' + str(id))
# 		return OptionSet(optionset)
# 
# class OptionSet(Resource):
# 	"""An individual option set"""
# 
# 	def create(self):
# 		"""Creates a new option set"""
# 		body = json.dumps(self.__dict__)
# 		optionset = self.client.request_json('PUT', '/optionsets', body)
# 
# 	def update(self):
# 		"""Updates local changes to the option set"""
# 		body = json.dumps(self.__dict__)
# 		optionset = self.client.request_json('PUT', '/optionsets/' + str(self.id), body)
# 
# 	def delete(self):
# 		"""Deletes the option set"""
# 		response, content = self.client.request('DELETE', '/optionsets/' + str(self.id))
# 
# class Categories(Resource):
# 	"""Categories collection"""
# 
# 	@classmethod
# 	def get(self):
# 		"""Returns list of categories"""
# 		categories = self.client.request_json('GET', '/categories')
# 		return [Category(category) for category in categories]
# 
# 	@classmethod
# 	def get_by_id(self, id):
# 		"""Returns an individual category by given ID"""
# 		category = self.client.request_json('GET', '/categories/' + str(id))
# 		return Category(category)
# 
# class Category(Resource):
# 	"""An individual category"""
# 
# 	def create(self):
# 		"""Creates a new category"""
# 		body = json.dumps(self.__dict__)
# 		category = self.client.request_json('PUT', '/categories', body)
# 
# 	def update(self):
# 		"""Updates local changes to the category"""
# 		body = json.dumps(self.__dict__)
# 		category = self.client.request_json('PUT', '/categories/' + str(self.id), body)
# 
# 	def delete(self):
# 		"""Deletes the category"""
# 		response, content = self.client.request('DELETE', '/categories/' + str(self.id))

