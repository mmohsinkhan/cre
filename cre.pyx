"""
Cython based high performance alternative to Python (re) module for
doing pattern search on large data-set.

Using this module search time can be significantly reduced by splitting
search task across multiple threads. GIL (Global Interpretor Lock) is
released during pattern search, allowing multiple threads to run
simultaneously on multiple CPU cores.

Pattern search is implemented in C utilizing GLib PCRE (Perl-compatible
regular expressions) support.

Notes:
* Application using the module would responsible for creating threads
and splitting search task across them.
* Unlike Python (re) counterparts, match' and 'search' functions do not
raise exception if provided regular-expression is incorrect. Explicit
compilation using 'compile' function does raise exception if regular
expression is incorrect.
* Module encodes unicode strings using 'utf-8' encoding before
processing.
* Module does not implicitly compile and cache patterns internally.
If required application has to explicitly compile pattern using
'compile' function.
* Searched patterns must comply with PCRE (Perl-compatible regular
expressions) standard.

Usage:

    import cre

    # search pattern
    cre.match('pattern', 'String containing pattern')

    # search using compiled pattern
    p = cre.compile('pattern')
    p.search(''String containing pattern'')

"""


# Include required definitions from GLib header file(s)
cdef extern from "glib.h" nogil:
    ctypedef int gboolean
    ctypedef char gchar
    ctypedef struct GRegex
    ctypedef struct GError
    ctypedef struct GMatchInfo
    ctypedef enum GRegexCompileFlags:
        G_REGEX_CASELESS,
        G_REGEX_MULTILINE,
        G_REGEX_DOTALL
    ctypedef enum GRegexMatchFlags:
        G_REGEX_MATCH_ANCHORED
    GRegex * g_regex_new(const gchar *pattern,
                         GRegexCompileFlags compile_options,
                         GRegexMatchFlags match_options,
                         GError **error)
    gboolean g_regex_match_simple(const gchar *pattern,
                                  const gchar *string,
                                  GRegexCompileFlags compile_options,
                                  GRegexMatchFlags match_options)
    gboolean g_regex_match(const GRegex *regex,
                           const gchar *string,
                           GRegexMatchFlags match_options,
                           GMatchInfo **match_info);
    void g_regex_unref(GRegex *regex)


# Map python regex compilation flags to GLib flags
IGNORECASE = <GRegexCompileFlags> G_REGEX_CASELESS
MULTILINE = <GRegexCompileFlags> G_REGEX_MULTILINE
DOTALL = <GRegexCompileFlags> G_REGEX_DOTALL

# Character encoding
CHAR_ENCODING = 'utf-8'


def _encode(string):
    """
    Encode string to bytes if provided string is unicode.
    @param: string: String to be encoded. (string/unicode/bytes)
    @return: Encoded string if provided string is unicode, otherwise
    same string is returned. (bytes)
    """
    if isinstance(string, unicode):
        return string.encode(CHAR_ENCODING)
    else:
        return string


cdef inline gboolean c_match_simple(
                char *pattern, char *string,
                GRegexCompileFlags c_flags=<GRegexCompileFlags> 0,
                GRegexMatchFlags m_flags=<GRegexMatchFlags> 0) nogil:
    """
    C wrapper around g_regex_match_simple function.
    """
    with nogil:
        return g_regex_match_simple(pattern, string, c_flags, m_flags)


cdef inline gboolean c_match(
                GRegex *regex, char *string,
                GRegexMatchFlags m_flags=<GRegexMatchFlags> 0) nogil:
    """
    C wrapper around g_regex_match function.
    """
    with nogil:
        return g_regex_match(regex, string, m_flags, NULL)


def search(pattern, string, flags=0):
    """
    Search through the string for pattern match.
    @param pattern: Pattern to search for. (string/unicode/bytes)
    @param string: String to be searched. (string/unicode/bytes)
    @param flags: Optional pattern compilation flags. (int)
    @return: MatchObject is case of pattern match,
    None otherwise. (object)
    """
    string = _encode(string)
    pattern = _encode(pattern)
    if c_match_simple(pattern, string, flags):
        return CRE_Match(pattern, string, flags)


def match(pattern, string, flags=0):
    """
    Match pattern at the start of the string.
    @param pattern: Pattern to search for. (string/unicode/bytes)
    @param string: String to be searched. (string/unicode/bytes)
    @param flags: Optional pattern compilation flags. (int)
    @return: MatchObject is case of pattern match,
    None otherwise. (object)
    """
    string = _encode(string)
    pattern = _encode(pattern)
    if c_match_simple(pattern, string, flags,
                      <GRegexMatchFlags> G_REGEX_MATCH_ANCHORED):
        return CRE_Match(pattern, string, flags)


def compile(pattern, flags=0):
    """
    Compile pattern to internal format for performance.
    @param pattern: Pattern to search for. (string/unicode/bytes)
    @param flags: Optional pattern compilation flags. (int)
    @return: Compiled RegEx object. (object)
    """
    pattern = _encode(pattern)
    return CRE_Pattern(pattern, flags)


cdef class CRE_Match:
    """
    Matched pattern object.
    """
    cdef readonly bytes pattern
    cdef readonly bytes string
    cdef readonly int flags

    def __cinit__(self, pattern, string, flags):
        """
        Set matched object attributes.
        @param pattern: Pattern matched. (bytes)
        @param string: String searched. (bytes)
        @param flags: Pattern compilation flags. (int)
        """
        self.pattern = pattern
        self.string = string
        self.flags = flags


cdef class CRE_Pattern:
    """
    Compiled pattern object.
    """
    cdef readonly bytes pattern
    cdef readonly int flags
    cdef GRegex *_compiled_regex

    def __cinit__(self, pattern, flags):
        """
        Compile pattern to internal format.
        @param pattern: Pattern to search for. (bytes)
        @param flags: Pattern compilation flags. (int)
        """
        self.pattern = pattern
        self.flags = flags
        self._compiled_regex = g_regex_new(pattern, flags,
                                           <GRegexMatchFlags> 0, NULL)
        if self._compiled_regex == NULL:
            raise SyntaxError('Compilaton failed, check regular' \
                              ' expression syntax.')

    def match(self, string):
        """
        Match pattern at the start of the string.
        @param string: String to be searched. (string/unicode/bytes)
        @return: MatchObject is case of pattern match,
        None otherwise. (object)
        """
        string = _encode(string)
        if c_match(self._compiled_regex, string,
                   <GRegexMatchFlags> G_REGEX_MATCH_ANCHORED):
            return CRE_Match(self.pattern, string, self.flags)

    def search(self, string):
        """
        Search through the string for pattern match.
        @param string: String to be searched. (string/unicode/bytes)
        @return: MatchObject is case of pattern match,
        None otherwise. (object)
        """
        string = _encode(string)
        if c_match(self._compiled_regex, string):
            return CRE_Match(self.pattern, string, self.flags)

    def __dealloc__(self):
        '''
        Free dynamic memory allocations.
        '''
        if self._compiled_regex != NULL:
            g_regex_unref(self._compiled_regex)
