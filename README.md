python-bigcommerce
==================

Python package for the BigCommerce API 

Installation
```
$ pip install python-bigcommerce
```


Getting Started
```
from bigcommerce import BigCommerce

bc = BigCommerce('DOMAIN','USERNAME','API_KEY')
bc.Orders.filter({ 'limit': 10, 'page': 1 })
```