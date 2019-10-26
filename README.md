# cre

Cython based high performance alternative to Python (re) module for doing pattern search on large data-set.

Using this module search time can be significantly reduced by splitting search task across multiple application threads. **GIL (Global Interpretor Lock) is released during pattern search, allowing multiple threads to run simultaneously on multiple CPU cores.**

Pattern search is implemented in C utilizing GLib PCRE (Perl-compatible regular expressions) support.

#### Notes:
* Application using the module would be responsible for creating threads and splitting search task across them.
* Unlike Python (re) counterparts, match' and 'search' functions do not raise exception if provided regular-expression is incorrect. Explicit compilation using 'compile' function does raise exception if regular expression is incorrect.
* Module encodes unicode strings using 'utf-8' encoding before processing.
* Module does not implicitly compile and cache patterns internally. If required application has to explicitly compile pattern  using 'compile' function.
* Searched patterns must comply with PCRE (Perl-compatible regular expressions) standard.

### Usage

API is similar to Python (re) module

    import cre

    # search pattern
    cre.match('pattern', 'String containing pattern')

    # search using compiled pattern
    p = cre.compile('pattern')
    p.search(''String containing pattern'')
    
### Compatibility

* Module should work with Python 2.7.x and 3.3+.
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
