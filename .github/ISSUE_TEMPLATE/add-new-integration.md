---
name: Add new integration
about: New integration issue template

---

## Overview
BookPro integrations are python classes inherited from thread class. These classes make request to the given endpoint and parse a list of books in a dictionary which is later used for further processing of results. These integrations help the BookPro to extend its search area to other websites. 

The already implemented integrations for some major sites are available [here](https://github.com/vshelke/bookpro/tree/master/bookpro/find_books/integrations).

### <NAME> Integration specs
* `url = ` without angle brackets.
* Refer [BeautifulSoup Implementation](https://github.com/vshelke/bookpro/blob/master/bookpro/find_books/integrations/infibeam.py)
* `data` dictionary
```python
data = {
    'title': '',
    'author': '',
    'offer_link': '',
    'link': '',
    'image': '',
    'price': None,
    'ISBN': '',
    'provider': ''
}
```

### Steps
* Create file in `find_books/integrations/<NAME>.py`
* Complete the `class <NAME> (Thread)` in `<NAME>.py`
* Complete the `parse_product` function to pull the details specified in `data` dictionary from the `soup`.
* Append the parsed items in `self.items`
* In `find_books/integrations/__init__.py` put `from .<NAME> import <NAME>`
* Import the class in `find_books/views.py` and use it in the `search` function to test the results.
* Run and check if results are shown.
