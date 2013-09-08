python-bigcommerce
==================

*NOTE* This package is still in development.  It will not work for you.

Python package for the BigCommerce API 

Installation
```
$ pip install python-bigcommerce
```


Getting Started
```
from bigcommerce import BigCommerce

bc = BigCommerce('DOMAIN','USERNAME','API_KEY')
bc.orders.filter({ 'limit': 10, 'page': 1 })
```