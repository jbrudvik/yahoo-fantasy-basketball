"""
Utilities for scraping Yahoo pages

The yahooscraper package is organized into modules and submodules. Each leaf
module (i.e., module without submodules) contains functions that take a single
argument -- HTML text of the page represented by the module and its
namespacing -- and return some data parsed from the page.

Additionally, each leaf module also includes a `url()` function, which returns
the URL of the page represented by the module. In cases where the module
represents a set of URLs, this function takes parameters.

If the data is not found, `None` is returned. Or, in cases where an iterable
should be returned, an empty iterable may be returned.
"""

from . import login, fantasy

__all__ = ['login', 'fantasy']
