import requests, base64, os

class BigCommerceError(Exception):
	pass

class BigCommerceResponseError(Exception):
	def __init__(self, http_response, content):
		self.http_response = http_response
		self.content = content


class BigCommerce(object):
	'''
    '''
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
		self.orders = Orders(*args, **kwargs)


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

	def handle_response(self, response):
		pass


	def delete(self, url, params=None):
		'''
		'''
		response = self.http.delete(url,params=params,**self.requests_params)
		return self.process(response)
	
	def get(self, url, data=None):
		'''
	    '''
		response = self.http.get(url,
	                             headers=self.headers,
	                             params=data,
	                             **self.requests_params)
		return self.process(response)
	
	def post(self, url, body=None):
		'''
		'''
		response = self.http.post(url,
	                              headers=self.headers,
	                              data=body,
	                              **self.requests_params)
		return self.process(response)
	
	def put(self, url, data=None, body=None):
		'''
		'''
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

class Response(object):
	def __init__(self, code, body, raw_body, raw_response):
		self.code = code
		self.body = body
		self.raw_body = raw_body
		self.raw_response = raw_response


class Orders(Connection):
	'''
    '''
	def __init__(self, *args, **kwargs):
		super(Orders, self).__init__(*args, **kwargs)
	def filter(self, dict):
		return self.get(self.base_url + '/orders.json', dict)