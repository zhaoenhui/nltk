# Natural Language Toolkit: Tokenizers
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Edward Loper <edloper@gradient.cis.upenn.edu>
#         Steven Bird <sb@csse.unimelb.edu.au>
#         Trevor Cohn <tacohn@csse.unimelb.edu.au>
# URL: <http://nltk.sourceforge.net>
# For license information, see LICENSE.TXT

"""
Tokenizers that divide strings into substrings using regular
expressions that can match either tokens or separators between tokens.
"""

import re
import sre_constants

from nltk.internals import convert_regexp_to_nongrouping, Deprecated

from api import *

class RegexpTokenizer(TokenizerI):
    """
    A tokenizer that splits a string into substrings using a regular
    expression.  The regular expression can be specified to match
    either tokens or separators between tokens.

    Unlike C{re.findall()} and C{re.split()}, C{RegexpTokenizer} does
    not treat regular expressions that contain grouping parenthases
    specially.
    """
    def __init__(self, pattern, gaps=False, discard_empty=True,
                 flags=re.UNICODE | re.MULTILINE | re.DOTALL):
        """
        Construct a new tokenizer that splits strings using the given
        regular expression C{pattern}.  By default, C{pattern} will be
        used to find tokens; but if C{gaps} is set to C{False}, then
        C{patterns} will be used to find separators between tokens
        instead.

        @type pattern: C{str}
        @param pattern: The pattern used to build this tokenizer.
            This pattern may safely contain grouping parenthases.
        @type gaps: C{bool}
        @param gaps: True if this tokenizer's pattern should be used
            to find separators between tokens; False if this
            tokenizer's pattern should be used to find the tokens
            themselves.
        @type discard_empty: C{bool}
        @param discard_empty: True if any empty tokens (C{''})
            generated by the tokenizer should be discarded.  Empty
            tokens can only be generated if L{_gaps} is true.
        @type flags: C{int}
        @param flags: The regexp flags used to compile this
            tokenizer's pattern.  By default, the following flags are
            used: C{re.UNICODE | re.MULTILINE | re.DOTALL}.
        """
        # If they gave us a regexp object, extract the pattern.
        pattern = getattr(pattern, 'pattern', pattern)
        
        self._pattern = pattern
        """The pattern used to build this tokenizer."""
        
        self._gaps = gaps
        """True if this tokenizer's pattern should be used to find
        separators between tokens; False if this tokenizer's pattern
        should be used to find the tokens themselves."""

        self._discard_empty = discard_empty
        """True if any empty tokens (C{''}) generated by the tokenizer
        should be discarded.  Empty tokens can only be generated if
        L{_gaps} is true."""

        self._flags = flags
        """The flags used to compile this tokenizer's pattern."""
        
        self._regexp = None
        """The compiled regular expression used to tokenize texts."""
        
        # Remove grouping parentheses -- if the regexp contains any
        # grouping parentheses, then the behavior of re.findall and
        # re.split will change.
        nongrouping_pattern = convert_regexp_to_nongrouping(pattern)

        try: 
            self._regexp = re.compile(nongrouping_pattern, flags)
        except re.error, e:
            raise ValueError('Error in regular expression %r: %s' %
                             (pattern, e))

    def tokenize(self, text):
        # If our regexp matches gaps, use re.split:
        if self._gaps:
            if self._discard_empty:
                return [tok for tok in self._regexp.split(text) if tok]
            else:
                return self._regexp.split(text)

        # If our regexp matches tokens, use re.findall:
        else:
            return self._regexp.findall(text)

    def __repr__(self):
        return ('%s(pattern=%r, gaps=%r, discard_empty=%r, flags=%r)' %
                (self.__class__.__name__, self._pattern, self._gaps,
                 self._discard_empty, self._flags))

class WhitespaceTokenizer(RegexpTokenizer):
    r"""
    A tokenizer that divides a string into substrings by treating any
    sequence of whitespace characters as a separator.  Whitespace
    characters are space (C{' '}), tab (C{'\t'}), and newline
    (C{'\n'}).  If you are performing the tokenization yourself
    (rather than building a tokenizer to pass to some other piece of
    code), consider using the string C{split()} method instead:

        >>> words = s.split()
    """

    def __init__(self):
        RegexpTokenizer.__init__(self, r'\s+', gaps=True)

class BlanklineTokenizer(RegexpTokenizer):
    """
    A tokenizer that divides a string into substrings by treating any
    sequence of blank lines as a separator.  Blank lines are defined
    as lines containing no characters, or containing only space
    (C{' '}) or tab (C{'\t'}) characters.
    """
    def __init__(self):
        RegexpTokenizer.__init__(self, r'\s*\n\s*\n\s*', gaps=True)

class WordPunctTokenizer(RegexpTokenizer):
    r"""
    A tokenizer that divides a text into sequences of alphabetic and
    non-alphabetic characters.  E.g.:

        >>> WordPunctTokenizer().tokenize("She said 'hello'.")
        ['She', 'said', "'", 'hello', "'."]
    """
    def __init__(self):
        RegexpTokenizer.__init__(self, r'\w+|[^\w\s]+')

class WordTokenizer(RegexpTokenizer, Deprecated):
    """
    B{If you want to tokenize words, you should probably use
    TreebankWordTokenizer or word_tokenize() instead.}
    
    A tokenizer that divides a text into sequences of alphabetic
    characters.  Any non-alphabetic characters are discarded.  E.g.:

        >>> WordTokenizer().tokenize("She said 'hello'.")
        ['She', 'said', 'hello']
    """
    def __init__(self):
        RegexpTokenizer.__init__(self, r'\w+')

######################################################################
#{ Tokenization Functions
######################################################################

def regexp_tokenize(text, pattern, gaps=False, discard_empty=True,
                    flags=re.UNICODE | re.MULTILINE | re.DOTALL):
    """
    Split the given text string, based on the given regular expression
    pattern.  See the documentation for L{RegexpTokenizer.tokenize()}
    for descriptions of the arguments.
    """
    tokenizer = RegexpTokenizer(pattern, gaps, discard_empty, flags)
    return tokenizer.tokenize(text)

blankline_tokenize = BlanklineTokenizer().tokenize
wordpunct_tokenize = WordPunctTokenizer().tokenize
