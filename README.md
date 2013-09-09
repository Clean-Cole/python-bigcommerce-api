python-bigcommerce
==================
Python for the BigCommerce API

*NOTE* 
This is still in development.

Installation:
requires requests
```
$ pip install python-bigcommerce
```

Usage:
You can initalize an instance with your authentication credentials or set them as environment variables.

```
from bigcommerce import BigCommerce
bc = BigCommerce('DOMAIN','USERNAME','API_KEY')
```
or
```
os.environ['BIGCOMMERCE_STORE_DOMAIN']
os.environ['BIGCOMMERCE_API_USERNAME']
os.environ['BIGCOMMERCE_API_KEY']
```

You can access resources with similar methods depending on their availability in the API.
{Resoure}.{all,filter,get,create,update,count,delete,delete_bulk}
```
bc.time.get()

result = bc.products.update("product_id", {
	'name' => 'Super Happy Funtime Product!'
})
>>> result.status_code
201
>>> result.body
{u'name': 'Super Happy Funtime Product!',...}


bc.orders.filter({ 'limit': 10, 'page': page# })
bc.orders.count()

```