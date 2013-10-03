import requests, base64, os, datetime
from requests.exceptions import ConnectionError

class BigCommerceError(Exception):
	pass
class BigCommerceErrorApiLimit(BigCommerceError):
	pass
class BigCommerceErrorNotModified(BigCommerceError):
	pass
class BigCommerceErrorUnauthorized(BigCommerceError):
	pass

class BigCommerce(object):
	def __init__(self, domain=None, api_user=None, api_key=None):
		if not domain:
			try:
				self.domain = os.environ['BIGCOMMERCE_STORE_DOMAIN']
			except KeyError:
				raise BigCommerceError('No domain or BIGCOMMERCE_STORE_DOMAIN given')
		else:
			self.domain = domain

		if not api_key:
			try:
				self.api_key = os.environ['BIGCOMMERCE_API_KEY']
			except KeyError:
				raise BigCommerceError('No BIGCOMMERCE_API_KEY given')
		else:
			self.api_key = api_key
		
		if not api_user:
			try:
				self.api_user = os.environ['BIGCOMMERCE_API_USERNAME']
			except KeyError:
				raise BigCommerceError('No BIGCOMMERCE_API_USERNAME given')
		else:
			self.api_user = api_user
		
		self.api_version = 'v2'
		
		args = (self.domain, self.api_user, self.api_key)
		kwargs = dict()
		self.brands = Brands(*args, **kwargs)
		self.categories = Categories(*args, **kwargs)
		self.orderstatuses = OrderStatuses(*args, **kwargs)
		self.customergroups = CustomerGroups(*args, **kwargs)
		self.coupons = Coupons(*args, **kwargs)
		self.time = Time(*args, **kwargs)
		self.store = Store(*args, **kwargs)
		self.countries = Countries(*args, **kwargs)
		self.states = States(*args, **kwargs)
		self.customers = Customers(*args, **kwargs)
		self.addresses = Addresses(*args, **kwargs)
		self.options = Options(*args, **kwargs)
		self.orders = Orders(*args, **kwargs)
		self.products = Products(*args, **kwargs)
		self.redirects = Redirects(*args, **kwargs)
		self.shipping = Shipping(*args, **kwargs)

class Connection(object):
	
	def __init__(self, domain, api_user, api_key):
		self.domain = domain
		self.api_user = api_user
		self.api_key = api_key
		self.http = requests.Session()
		self.base_url = 'https://'+self.domain+'/api/v2'
		auth = base64.b64encode(self.api_user + ':' + self.api_key)
		self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + auth,
            'User-Agent': 'python-bigcommerce v0.1'
        }
		
		self.http.headers.update(self.headers)
		
		self.requests_params = {
            'timeout': None,
            'proxies': None,
            'cert': None,
            'verify': None,
        }
	def call(self, url, method='GET', data=None, body=None, modified_since=None):

		if modified_since and ( isinstance(modified_since, datetime.date) or isinstance(modified_since, basestring)):
			self.headers['If-Modified-Since'] = unicode(modified_since)
			self.http.headers.update(self.headers)
		
		try:
			if method == 'GET':
				response = self.http.get(url, headers=self.headers, params=data, **self.requests_params)
			elif method == 'POST':
				response = self.http.post(url, headers=self.headers, data=body, **self.requests_params)
			elif method == 'PUT':
				response = self.http.put(url, headers=self.headers, data=body, params=data, **self.requests_params)
			elif method == 'DELETE':
				response = self.http.delete(url,params=data,**self.requests_params)
			
			return self.process(response)
			
		except ConnectionError,e:
			if e.find('MaxRetryError') != -1:
				raise BigCommerceErrorApiLimit('BigCommerceApiLimit: API Limit for this url reached')
		
		
			

	def process(self, response):
		code = response.status_code
		
		if code == 304:
				raise BigCommerceErrorNotModified('(304) Not Modified')
		
		if code == 401:
			raise BigCommerceErrorUnauthorized('(401) The Credentials Supplied Were Invalid')
		
		if code == 204:
			body = None
		else:
			body = response.json()

		return Response(code, body, response.content, response)

class Response(object):
	def __init__(self, code, body, raw_body, raw_response):
		self.code = code
		self.body = body
		self.raw_body = raw_body
		self.raw_response = raw_response
	
class Brands(Connection):
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/brands.json', 'GET', data, modified_since=modified_since)
	def get(self, brand_id):
		return self.call(self.base_url + '/brands/%s.json' % str(brand_id), 'GET')
	def update(self, brand_id, data):
		return self.call(self.base_url + '/brands/%s.json' % str(brand_id), 'PUT', data)
	def count(self):
		return self.call(self.base_url + '/brands/count.json', 'GET')
	def delete(self, brand_id):
		return self.call(self.base_url + '/brands/%s.json' % str(brand_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/brands.json', 'DELETE', data)
	
class Categories(Connection):
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/categories.json', 'GET', data, modified_since=modified_since)
	def get(self, category_id):
		return self.call(self.base_url + '/categories/%s.json' % str(category_id), 'GET')
	def update(self, category_id, data):
		return self.call(self.base_url + '/categories/%s.json' % str(category_id), 'PUT', data)
	def count(self):
		return self.call(self.base_url + '/categories/count.json', 'GET')
	def delete(self, category_id):
		return self.call(self.base_url + '/categories/%s.json' % str(category_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/categories.json', 'DELETE', data)
	
class OrderStatuses(Connection):
	def all(self):
		return self.call(self.base_url + '/orderstatuses.json', 'GET')
	def get(self, status_id):
		return self.call(self.base_url + '/orderstatuses/%s.json' % str(status_id), 'GET')

class CustomerGroups(Connection):
	def all(self, modified_since=None):
		return self.call(self.base_url + '/customer_groups', 'GET', None, modified_since=modified_since)
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/customer_groups', 'GET', data, modified_since=modified_since)
	def get(self, group_id):
		return self.call(self.base_url + '/customer_groups/%s' % str(group_id), 'GET')
	def create(self, data):
		return self.call(self.base_url + '/customer_groups', 'POST', data)
	def count(self):
		return self.call(self.base_url + '/customer_groups/count', 'GET')
	def delete(self, group_id):
		return self.call(self.base_url + '/customer_groups/%s.json' % str(group_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/customer_groups', 'DELETE', data)

class Coupons(Connection):
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/coupons.json', 'GET', data, modified_since=modified_since)
	def get(self, coupon_id):
		return self.call(self.base_url + '/coupons/%s.json' % str(coupon_id), 'GET')
	def update(self, coupon_id, data):
		return self.call(self.base_url + '/coupons/%s.json' % str(coupon_id), 'PUT', data)
	def count(self):
		return self.call(self.base_url + '/coupons/count.json', 'GET')
	def delete(self, coupon_id):
		return self.call(self.base_url + '/coupons/%s.json' % str(coupon_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/coupons.json', 'DELETE', data)

class Time(Connection):
	def get(self):
		return self.call(self.base_url + '/time.json', 'GET')
	
class Store(Connection):
	def get(self):
		return self.call(self.base_url + '/store.json', 'GET')
	
class Countries(Connection):
	def filter(self, data=None):
		return self.call(self.base_url + '/countries', 'GET', data)
	def get(self, country_id):
		return self.call(self.base_url + '/countries/%s.json' % str(country_id), 'GET')
	def count(self):
		return self.call(self.base_url + '/countries/count.json', 'GET')
	
class States(Connection):
	def filter(self, data=None):
		return self.call(self.base_url + '/countries/states.json', 'GET', data)
	def get(self, state_id):
		return self.call(self.base_url + '/countries/states/%s.json' % str(state_id), 'GET')
	def count(self):
		return self.call(self.base_url + '/countries/states/count.json', 'GET')
	
class Customers(Connection):
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/customers.json', 'GET', data, modified_since=modified_since)
	def get(self, customer_id):
		return self.call(self.base_url + '/customers/%s.json' % str(customer_id), 'GET')
	def update(self, customer_id, data):
		return self.call(self.base_url + '/customers/%s.json' % str(customer_id), 'PUT', data)
	def count(self):
		return self.call(self.base_url + '/customers/count.json', 'GET')
	def delete(self, customer_id):
		return self.call(self.base_url + '/customers/%s.json' % str(customer_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/customers.json', 'DELETE', data)
	
class Addresses(Connection):
	pass

class Options(Connection):
	def all(self, modified_since=None):
		return self.call(self.base_url + '/options.json', 'GET', None, modified_since=modified_since)
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/options.json', 'GET', data, modified_since=modified_since)
	def get(self, option_id):
		return self.call(self.base_url + '/options/%s.json' % str(option_id), 'GET')
	def update(self, option_id, data):
		return self.call(self.base_url + '/options/%s.json' % str(option_id), 'PUT', data)
	def create(self, data):
		return self.call(self.base_url + '/options.json', 'POST', data)
	def count(self):
		return self.call(self.base_url + '/options/count.json', 'GET')
	def delete(self, option_id):
		return self.call(self.base_url + '/options/%s.json' % str(option_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/options.json', 'DELETE', data)
	
# @TODO: Figure out a solution for handling sub Coupons, Products, Shipments, & Shipping Addresses
class Orders(Connection):
	def filter(self, data=None, modified_since=None, inc_products=False):
		result = self.call(self.base_url + '/orders.json', 'GET', data, modified_since=modified_since)
		if inc_products:
			try:
				prod_result = self.call(result.body['products']['url'], 'GET').body
				result.body['products'] = [] if not prod_result else prod_result
			except Exception,e:
				pass
		return result
	def get(self, order_id, inc_products=False):
		result = self.call(self.base_url + '/orders/%s.json' % str(order_id), 'GET')
		if inc_products:
			try:
				prod_result = self.call(result.body['products']['url'], 'GET').body
				result.body['products'] = [] if not prod_result else prod_result
			except Exception,e:
				pass
		return result
	def update(self, order_id, data):
		return self.call(self.base_url + '/orders/%s.json' % str(order_id), 'PUT', data)
	def create(self, data):
		return self.call(self.base_url + '/orders.json', 'POST', data)
	def count(self):
		return self.call(self.base_url + '/orders/count.json', 'GET')
	def delete(self, order_id):
		return self.call(self.base_url + '/orders/%s.json' % str(order_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/orders.json', 'DELETE', data)

# @TODO: Figure out a solution for handling sub SKUs, Fields, Discounts, Images, Options, Rules, & Videos
class Products(Connection):
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/products.json', 'GET', data, modified_since)
	def get(self, order_id):
		return self.call(self.base_url + '/products/%s.json' % str(order_id), 'GET')
	def update(self, order_id, data):
		return self.call(self.base_url + '/products/%s.json' % str(order_id), 'PUT', data)
	def create(self, data):
		return self.call(self.base_url + '/products.json', 'POST', data)
	def count(self):
		return self.call(self.base_url + '/products/count.json', 'GET')
	def delete(self, order_id):
		return self.call(self.base_url + '/products/%s.json' % str(order_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/products.json', 'DELETE', data)
	
class Redirects(Connection):
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/redirects', 'GET', data, modified_since=modified_since)
	def get(self, redirect_id):
		return self.call(self.base_url + '/redirects/%s' % str(redirect_id), 'GET')
	def create(self, data):
		return self.call(self.base_url + '/redirects', 'POST', data)
	def count(self):
		return self.call(self.base_url + '/redirects/count', 'GET')
	def delete(self, redirect_id):
		return self.call(self.base_url + '/redirects/%s.json' % str(redirect_id), 'DELETE')
	def delete_bulk(self, data=None):
		return self.call(self.base_url + '/redirects', 'DELETE', data)
	
class Shipping(Connection):
	def all(self, modified_since=None):
		return self.call(self.base_url + '/shipping/methods.json', 'GET', None, modified_since=modified_since)
	def filter(self, data=None, modified_since=None):
		return self.call(self.base_url + '/shipping/methods.json', 'GET', data, modified_since=modified_since)
	def get(self, method_id):
		return self.call(self.base_url + '/shipping/methods/%s.json' % str(method_id), 'GET')