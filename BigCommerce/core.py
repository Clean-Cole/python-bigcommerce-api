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


class Orders(Connection):
    """ Contains all API methods relating to Orders."""
    def __init__(self, *args, **kwargs):
        kwargs['resource_name'] = 'inputs'
        super(Input, self).__init__(*args, **kwargs)
        
    def filter(self, params):
	   return self.get(self.base_url + '/orders.json')