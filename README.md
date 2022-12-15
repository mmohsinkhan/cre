# cre

Cython based high performance alternative to Python (re) module for doing basic pattern matching on large data-set.

Using this module execution time can be significantly reduced by splitting search task across multiple threads. **GIL (Global Interpretor Lock) is released during pattern match, allowing multiple threads to run simultaneously on multiple CPU cores.**

Pattern matching is implemented in C utilizing GLib PCRE (Perl-compatible regular expressions) support.

#### Notes:
* Application would be responsible for creating threads and splitting pattern matching task across them.
* Unlike Python (re) module, 'match' and 'search' methods do not raise exception if provided regular-expression is incorrect. Explicit compilation using 'compile' method does raise exception if regular expression is incorrect.
* Strings are encoded using 'utf-8' before processing.
* Patterns are not implicitly compiled and cached internally. If required application has to explicitly compile pattern using 'compile' method.
* Searched patterns must comply with PCRE (Perl-compatible regular expressions) standard.

### Usage

API is similar to Python (re) module

    import cre as re

    # search pattern
    re.match('pattern', 'String containing pattern')

    # search using compiled pattern
    p = re.compile('pattern')
    p.search('String containing pattern')
    
### Compatibility

* cre should work with Python 2.7.x and 3.3+.
* Compilation has been tested with Cython 0.29.13.

### Installation

#### Prerequisites

* Development package of Python.
* GLib 2.0 development package.
* pkg-config utility.
* Cython (Optional)

If Cython is installed (.pyx) file is converted to (.c) file during installation, otherwise pre-packaged (.c) file is compiled.

#### Install From Source

* Checkout the repo.
* Install module
	    
	    pip install ./cre/

### Demonstration

Run provided 'demo.py' script.
