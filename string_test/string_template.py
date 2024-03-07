# coding: utf-8


import string
import unittest


# PEP 292 - Simpler String Substitutions
# https://peps.python.org/pep-0292/


values = {'var': 'foo'}

t = string.Template("""
Variable            : $var
Escaped             : $$
Variable in text    : ${var}iable
""")

print('TEMPLATE: ', t.substitute(values))

s = """
Variable : %(var)s
Escaped : %%
Variable in text: %(var)siable
"""

print('INTERPOLATION: ', s % values)

s = """
Variable : {var}
Escape : {{}}
Variable in text: {var}iable
"""

print('FORMAT: ', s.format(**values))

t = string.Template("$var is here but $missing is not provided.")

try:
    print('substitute()  : ', t.substitute(values))
except KeyError as err:
    print('ERROR: ', str(err))

print('safe_substitute() : ', t.safe_substitute(values))


# Advanced Usage --- using Regex in string templates


class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = '[a-z]+_[a-z]+'


template_text = '''
Delimiter: %%
Replaced: %with_underscore
Ignored: %notunderscored
'''

d = {
    'with_underscore': 'replaced',
    'notunderscored': 'not replaced'
}

t = MyTemplate(template_text)
print('Modified ID pattern: ')
print(t.safe_substitute(d))

t = string.Template('$var')
print(t.pattern.pattern)

# The value of t.pattern is a compiled regular expression, but the original string is available via its pattern
# attribute.

# The result of the t.pattern.pattern is as follows:
"""
            \$(?:
              (?P<escaped>\$)  |   # Escape sequence of two delimiters
              (?P<named>(?a:[_a-z][_a-z0-9]*))       |   # delimiter and a Python identifier
              {(?P<braced>(?a:[_a-z][_a-z0-9]*))} |   # delimiter and a braced identifier
              (?P<invalid>)             # Other ill-formed delimiter exprs
            )
"""

# The default syntax for string.Template can be changed by adjusting the regular expression patterns it uses to find the
# variable names in the template body.
# For even more complex changes, it is possible to override the pattern attribute and define an entirely new regular
# expression. The pattern provided must contain four named groups for capturing:
# * the escaped delimiter;
# * the named variable;
# * a braced version of the variable name;
# * invalid delimiter patterns.


# This example defines a new pattern to create a new type of template, using {{var}} as the variable syntax


class MyTemplate2(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z09]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''

# Escaped Placeholder:
# * An escaped placeholder is represented by `$$.`
# * When the template contains `$$`, it doesn't get substituted; instead, it remains as it is in the output.
#   ```python3
#   from string import Template
#   t = Template('Escape this: $$')
#   print(t.substitute()) # Output: Escape this: $
#   ```
#
# Named Placeholder:
# * Named placeholders are identified by a name surrounded by `$` signs.
# * The names can consist of letters, digits, and underscores, but must start with a letter or an underscore.
#   ```python3
#   from string import Template
#   t = Template("Hello, $name!")
#   print(t.substitute(name="Alice")) # Output: Hello, Alice!
#   ```
#
# Braced Placeholder:
# * Braced placeholders are identified by names surrounded by `${}`.
# * They can include arbitrary expressions enclosed in braces, making them more versatile than simple named
#   placeholders.
#   ```python3
#   from string import Template
#   t = Template("Total cost: ${price * quantity}")
#   print(t.substitute(price=10, quantity=5)) # Output: Total cost: 50
#   ```
#
# Invalid Placeholder:
# * An invalid placeholder occurs when a placeholder cannot be successfully substituted due to missing values or
#   incorrect format.
# * If a named placeholder cannot be matched with a provided value, a `KeyError` is raised during the substitution
#   process.
#   ```python3
#   from string import Template
#   t = Template("Hello, $name!")
#   print(t.substitute()) # Raises KeyError: 'name' since no value is provided for the 'name' placeholder.
#   ```
# These different placeholder types provide flexibility and ease of use when working with string templates in Python,
# allowing developers to create dynamic stirngs with ease while maintaining readability and simplicity.


# Both the **named** and **braced** patterns must be provided separately, even though they are the same.


t = MyTemplate2('''
{{{{
{{var}}
''')

print('MATCHES: ', t.pattern.findall(t.template))
# MATCHES:  [('{{', '', '', ''), ('', 'var', '', '')]

print('SUBSTITUTED: ', t.safe_substitute(var='replacement'))

# SUBSTITUTED:
# {{
# replacement

# Formatter
# The **Formatter** class implements the same layout specification language as the format() method of str. Its features
# include type coersion, alignment, attribute and field references, named and positional template arguments, and
# type-specific formatting options.


import inspect
import string


def is_str(value_):
    return isinstance(value_, str)


for name, value in inspect.getmembers(string, is_str):
    if name.startswith('_'):
        continue
    print('%s=%r\n' % (name, value))

# These are all string constants:
"""
ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

ascii_lowercase='abcdefghijklmnopqrstuvwxyz'

ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

digits='0123456789'

hexdigits='0123456789abcdefABCDEF'

octdigits='01234567'

printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'

punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

whitespace=' \t\n\r\x0b\x0c'
"""


# textwrap: Formatting Text Paragraphs

simple_text = '''
The textwrap module can be used to format text for output in
situations where pretty-printing is desired.  It offers      
programmatic functionality similar to the paragraph wrapping
or filling features found in many text editors.
'''

import textwrap


# The **fill()** function takes text as input and produces formatted text as output.
print(textwrap.fill(simple_text, width=50))

# The **dedent()** function produces better results and allows the use of docstrings or embedded multiline strings
# straight from Python code while removing the formatting of the code itself. The sample string has an artificial indent
# level introduced for illustrating this feature.
dedented_text = textwrap.dedent(simple_text)
print('Dedented:')
print(dedented_text)


dedented_text = textwrap.dedent(simple_text).strip()
for width in [45, 60]:
    print('{} Columns: \n'.format(width))
    print(textwrap.fill(dedented_text, width=width))
    print()


# Using the **indent()** function to add consistent prefix text to all the lines in a string.
dedented_text = textwrap.dedent(simple_text)
wrapped = textwrap.fill(dedented_text, width=50)
wrapped += '\n\nSecond paragraph after a blank line.'
final = textwrap.indent(wrapped, '> ')
print('Quoted block:\n')
print(final)


# To control which lines receive the new prefix, pass a callable as the **predicate** argument to **indent**. The
# callable will be invoked for each line of text in turn and the prefix will be added for lines where the return value
# is true.

def should_indent(line):
    print('Indent {!r}?'.format(line))
    # `{!r}` is a placeholder that will be replaced by the value of the variable `line`. The `!r` conversion flag
    # specifies that `repr()` should be used to represent the value.
    # The `!r` conversion flag ensures that the output is the "official" string representation of the variable `line`,
    # as returned by the `repr()` function. This representation is often more verbose and explicit than the one provided
    # by `str()`, making it useful for debugging and displaying the exact content of variables.
    return len(line.strip()) % 2 == 0


dedented_text = textwrap.dedent(simple_text)
wrapped = textwrap.fill(dedented_text, width=50)
final = textwrap.indent(wrapped, 'EVEN ', predicate=should_indent)
print('\nQuoted block:\n')
print(final)

# Hanging Indents
# It is possible to set the width of the output, the indent of the first line can be controlled independently of
# subsequent lines.

dedented_text = textwrap.dedent(simple_text).strip()
print(textwrap.fill(dedented_text,
                    initial_indent='',
                    subsequent_indent=' ' * 4,
                    width=50,))


# re --- Regular Expressions
# Regular expressions are text matching patterns described with a formal syntax. Python's **re** module is based on the
# syntax used for regular expressions in Perl, with a few Python-specific enhancements.

import re


pattern = 'this'
text = 'Does this text match the pattern?'

match = re.search(pattern, text)

# The **start()** and **end()** methods give the indexes into the string showing where the text matched by the pattern
# occurs.
s = match.start()
e = match.end()

print('Found "{}"\nin "{}"\nfrom {} to {} ("{}")'.format(
    match.re.pattern, match.string, s, e, text[s:e]))

"""
Found "this"
in "Does this text match the pattern?"
from 5 to 9 ("this")
"""


# Pre-compile the patterns
# The module-level functions maintain a cache of compiled expressions, but the size of the cache is limited and using
# compiled expressions directly avoids the overhead associated with cache lookup. Another advantage of using compiled
# expressions is that by pre-compiling all the expressions when the module is loaded, the compilation work is shifted
# to application start time, instead of occurring at a point where the program may be responding to a user action.
regexes = [re.compile(p) for p in ['this', 'that']]
text = 'Does this text match the pattern?'

print('Text: {!r}\n'.format(text))

for regex in regexes:
    print('Seeking "{}" -> '.format(regex.pattern), end=' ')

    if regex.search(text):
        print('match!')
    else:
        print('no match')


# Multiple Matches
# The **findall()** function returns all the substrings of the input that match the pattern without overlapping.

text = 'abbaaabbbbaaaaa'

pattern = 'ab'

for match in re.findall(pattern, text):
    print('Found {!r}'.format(match))

# **finditer()** returns an iterator that produces **Match** instances instead of the strings returned by **findall()**.

for match in re.finditer(pattern, text):
    s, e = match.start(), match.end()
    print('Found {!r} at {:d}:{:d}'.format(text[s:e], s, e))


# Pattern Syntax
# Regular expressions support more powerful patterns than simple literal text strings. Patterns can repeat, can be
# anchored to different logical locations within the input, and can be expressed in compact forms that do not require
# every literal character to be present in the pattern. All of these features are used by combining literal text values
# with meta-characters that are part of the regular expression pattern syntax implemented by re.

def test_patterns(text, patterns):
    """
    Given source text and a list of patterns, look for matches for each pattern within the text and print them to
    stdout.
    :param text:
    :param patterns:
    :return:
    """
    # Look for each pattern in the text and print the results.
    for pattern, desc in patterns:
        print("'{!r}' ({})\n".format(pattern, desc))
        print('  {!r}'.format(text))
        for match in re.finditer(pattern, text):
            s, e = match.start(), match.end()
            prefix = ' ' * (s)
            print('  {}{!r}{} '.format(prefix, text[s:e], ' ' * (len(text) - e)), end=' ',)
            print(match.groups())

            if match.groupdict():
                print('{}{}'.format(' ' * (len(text) - s), match.groupdict()),)
        print()


test_patterns('abbaaabbbbaaaaa',
              [
                  ('ab*', "'a' followed by zero or more 'b'"),
                  ('ab+', "'a' followed by one or more 'b'"),
                  ('ab?', "'a' followed by zero or one 'b'"),
                  ('ab{3}', "'a' followed by three 'b'"),
                  ('ab{2,3}', "'a' followed by two to three 'b'"),
              ])


# When processing a repetition instruction, **re** will usually consume as much of the input as possible while matching
# the pattern. This so-called greedy behavior may result in fewer individual matches, or the matches may include more of
# the input text than intended. Greediness can be turned off by following the repetition instruction with ?.
# Example:

test_patterns('abbaaabbbbaaaaa',
              [
                  ('ab*?', "'a' followed by zero or more 'b'"),
                  ('ab+?', "'a' followed by one or more 'b'"),
                  ('ab??', "'a' followed by zero or one 'b'"),
                  ('ab{3}?', "'a' followed by three 'b'"),
                  ('ab{2,3}?', "'a' followed by two to three 'b'"),
              ])


# The carat (^) means to look for characters that are not in the set following the carat.

test_patterns(
    'This is some text -- with punctuation.',
    [('[^-. ]+', 'sequences without -, ., or space')]
)


test_patterns(
    'A prime #1 example!',
    [
        (r'\d+', 'sequence of digits'),
        (r'\D+', 'sequence of non-digits'),
        (r'\s+', 'sequence of whitespace'),
        (r'\S+', 'sequence of non-whtespace'),
        (r'\w+', 'alphanumeric characters'),
        (r'\W+', 'non-alphanumeric'),
    ])


# Anchoring
# In addition to describing the content of a pattern to match, the relative location can be specified in the input text
# where the pattern should appear by using anchoring instructions.

# Regular Expression Anchoring Codes
# -------------------------------------------------------------------------------
# | Code   | Meaning                                                            |
# |--------+--------------------------------------------------------------------|
# | ^      | Start of string, or line                                           |
# | $      | End of string, or line                                             |
# | \A     | Start of string                                                    |
# | \Z     | End of string                                                      |
# | \b     | Empty string at the beginning or end of a word                     |
# | \B     | Empty string not at the beginning or end of a word                 |
# -------------------------------------------------------------------------------

test_patterns(
    'This is some text -- with punctuation.',
    [
        (r'^\w+', 'word at start of string'),
        (r'\A\w+', 'word at start of string'),
        (r'\w+\S*$', 'word near end of string'),
        (r'\w+\S*\Z', 'word near end of string'),
        (r'\w*t\w*', 'word containing t'),
        (r'\bt\w|', 't at start of word'),
        (r'\w+t\b', 't at end of word'),
        (r'\Bt\B', 't, not start or end of word'),
    ])


# Constraining the Search
# If the pattern must appear at the front of the input, then using **match()** will anchor the search without having to
# explicitly include an anchor in the search pattern.
text = 'This is some text -- with punctuation.'
pattern = 'is'

print('Text : ', text)
print('Pattern: ', pattern)

m = re.match(pattern, text)
print('Match : ', m)
s = re.search(pattern, text)
print('Search: ', s)

# The **fullmatch()** method requires that the entire input string match the pattern.
s = re.fullmatch(pattern, text)
print('Full match: ', s)

# Here **search()** method of a compiled regular expression accepts optional start and end position parameters to limit
# the search to a substring of the input.

pattern = re.compile(r'\b\w*is\w*\b')
print('Text: ', text)
print()

pos = 0
while True:
    match = pattern.search(text, pos)
    if not match:
        break
    s = match.start()
    e = match.end()

    print('  {:>2d} : {:>2d} = "{}"'.format(s, e - 1, text[s:e]))
    # move forward in text for the next search
    pos = e


# Searching for pattern matches is the basis of the powerful capabilities provided by regular expressions. Adding groups
# to a pattern isolates parts of the matching text, expanding those capabilities to create a parser. Groups are defined
# by enclosing patterns in parentheses.

test_patterns(
    'abbaaabbbbaaaaa',
    [('a(ab)', 'a followed by literal ab'),
     ('a(a*b*)', 'a followed by 0-n a and 0-n b'),
     ('a(ab)*', 'a followed by 0-n ab'),
     ('a(ab)+', 'a followed by 1-n ab')]
)

# To acces the substrings matched by the individual groups within a pattern, use the **groups()** method of the Match
# object.

text = 'This is some text -- with punctuation.'

print(text)
print()

patterns = [
    (r'^(\w+)', 'word at start of string'),
    (r'(\w+)\S*$', 'word at end, with optional punctuation'),
    (r'(\bt\w+)\W+(\w+)', 'word starting with t, another word'),
    (r'(\w+t)\b', 'word ending with t')
]

for pattern, desc in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}' ({})\n".format(pattern, desc))
    print('  ', match.groups())
    # type(match.groups()) --- string of tuple
    print('type(match.group(): ', type(match.groups()))
    print()


# To ask for the match of a single group, use the **group()** method. This is useful when grouping is being used to find
# parts of the string, but some parts matched by groups are not needed in the results.

text = 'This is some text -- with punctuation.'
print('Input text: ', text)

# Word starting with 't' then another word
regex = re.compile(r'(\bt\w)\W+(\w+)')
print('Pattern: ', regex.pattern)

match = regex.search(text)
if match:
    print('Entire match: ', match.group(0))
    print('Word starting with "t": ', match.group(1))
    print('Word after "t" word: ', match.group(2))

# Group o represents the string matched by the entire expression, and subgroups are numbered starting with 1 in the
# order that their left parenthesis appears in the expression.

# Python extends the basic grouping syntax to add named groups. Using names to refer to groups makes it easier to modify
# the pattern over time, without having to also modify the code using the match results.
# To set the name of a group, use the syntax (?P<name>pattern).

text = 'This is some text -- with punctuation.'

print(text)
print()

patterns = [
    r'^(?P<first_word>\w+)',
    r'(?P<last_word>\w+)\S*$',
    r'(?P<t_word>\bt\w+)\W+(?P<other_word>\w)',
    r'(?P<ends_with_t>\w+t)\b',
]

for pattern in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}'".format(pattern))
    print('  ', match.groups())
    # Use **groupdict()** to retrieve the dictionary mapping group names to substrings from the match. Named patterns
    # are included in the ordered sequence returned by groups as well.
    print('  ', match.groupdict())
    print()


# Since a group is itself a complete regular expression, groups can be nested within other groups to build even more
# complicated expressions.

test_patterns(
    'abbaabbba',
    [(r'a((a*)(b*))', 'a followed by 0-n a and 0-n b')],
)


# Groups are also useful for specifying alternative patterns. Use the pipe symbol (|) to indicate that either pattern
# should match. Consider the placement of the pipe carefully, though. The first expression in this example matches a
# sequence of a followed by a sequence consisting entirely of a single letter, a or b. The second pattern matches a
# followed by a sequence that may include either a or b. The patterns are similar, but the resulting matches are
# completely different.

# Defining group containing a subpattern is also useful in cases where the string matching the subpattern is not part
# of what should be extracted from the full text. These kinds of groups are called non-capturing.
# To create a non-capturing group, use the syntax: (?:pattern)

test_patterns(
    'abbaabbba',
    [(r'a((a+)|(b+))', 'capturing form'),
     (r'a((?:a+)|(?:b+))', 'non-capturing')]
)

# Search Options
# Option flags are used to change the way the matching engine process an expression. The flags can be combined using a
# bitwise OR operation, then passed to compile(), search(), match(), and other functions that accept a pattern for
# searching.

# Case-Insensitive Matching
# IGNORECASE

text = 'This is some text -- with punctuation.'
pattern = r'\bT\w+'
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print('Text:\n {!r}'.format(text))
print('Pattern:\n {}'.format(pattern))
print('Case-sensitive: ')
for match in with_case.findall(text):
    print('  {!r}'.format(match))
print('Case-insensitive: ')
for match in without_case.findall(text):
    print('  {!r}'.format(match))


# Input with Multiple Lines
# Two flags affect how searching in multiline input works: MULTILINE and DOTALL.
#
# MULTILINE
# MULTILINE flag controls how the pattern matching code proceses anchoring instructions for text containing newline
# characters. When multiline mode is turned on, the anchor rules for ^ and $ apply at the beginning and end of each
# line, in addition to the entire string.

text = 'This is some text -- with punctuation.\nA second line'
pattern = r'(^\w+)|(\w+\S*$)'
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

print('Text:\n {!r}'.format(text))
print('Pattern:\n {}'.format(pattern))
print('Single Line: ')
for match in single_line.findall(text):
    print('  {!r}'.format(match))
print('Multiline: ')
for match in multiline.findall(text):
    print('  {!r}'.format(match))


# DOTALL
# DOTALL is the other flag related to multiline text. Normally, the dot character(.) matches everything in the input
# text except a newline character. The flag allows the dot to match newlines as well.

text = 'This is some text -- with punctuation.\nA second line.'
pattern = r'.+'
no_newlines = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print('Text:\n {!r}'.format(text))
print('Pattern:\n {}'.format(pattern))
print('No newlines:')
for match in no_newlines.findall(text):
    print('  {!r}'.format(match))
print('Dotall:')
for match in dotall.findall(text):
    print('  {!r}'.format(match))

# A pattern to validate email addresses will illustrate how verbose mode makes working with regular expressions eaiser.

address = re.compile('[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)')
candidates = [
    r'first.last@example.com',
    r'first.last+category@gmail.com',
    r'valid-address@mail.example.com',
    r'not-valid@example.foo',
]

for candidate in candidates:
    match = address.search(candidate)
    print('{:<30} {}'.format(
        candidate, 'Matches' if match else 'No match'))


# Converting the expression to a more verbose format will make it easier to extend.

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
        ([\w.,]+\s+)*[\w.,]+)
        \s*
        # Email addresses are wapped in angle
        # brackets < >, but only ifa name is
        # found, so keep the start bracket in
        # this group.
        <
    )? # The entire name is optional.
    
    # The address itself: username@domain.tld
    (?P<email>
        [\w\d.+-]+      # Username
        @
        ([\w\d.]+\.)+   # Domain name prefix
        (com|org|edu)   # Limit the allowed top-level domains.
    )
    >? # Optional closing angle bracket.
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid-address@example.foo',
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'First Last',
    u'First Middle Last <first.last@example.com>',
    u'First M. Lst <first.last@example.com>',
    u'<first.last@example.com>'
]

for candidate in candidates:
    match = address.search(candidate)
    if match:
        print('  Name: ', match.groupdict()['name'])
        print('  Email: ', match.groupdict()['email'])
    else:
        print('  No Match')

# Embedding Flags in Patterns
# Turn case-insensitive matching on, add (?i) to the beginning of the expression.

text = 'This is some text -- with punctuation.'
pattern = r'(?i)\bT\w+'
regex = re.compile(pattern)

print('Text: ', text)
print('Pattern: ', pattern)
print('Matches: ', regex.findall(text))


# Looking Ahead or Behind
# Positive look ahead assertion syntax: (?=pattern)


print("Looking Ahead or Behind")

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
        ([\w.,]+\s+)*[\w.,]+
      )
      \s+
    ) # The name is no longer optional
    
    # LOOKAHEAD
    # Email addresses are wrapped in angle brackets, but only if both
    # are present or neither is.
    (?= (<.*>$)         # Remainder wrapped in angle brackets
        |
        ([^<].*[^>]$)   # Remainder *not* wrapped in angle brackets
    )
    <? # Optional opening angle bracket
    
    # The address itself: username@domain.tld
    (?P<email>
        [\w\d.+-]+      # Username
        @
        ([\w\d.]+\.)+   # Domain name prefix
        (com|org|edu)   # Limit the allowed top-level domains.
    )
    >?  # Optional closing angle bracket
    ''',
    re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket <first.last@example.example>',
]

for candidate in candidates:
    print('Candidate: ', candidate)
    match = address.search(candidate)
    if match:
        print('  Name: ', match.groupdict()['name'])
        print('  Email: ', match.groupdict()['email'])
    else:
        print('  No Match')


# The negative look ahead assertion (?!pattern) says that the pattern does not match the text following the current
# point.
print("Negative Look Ahead Assertion")

address = re.compile(
    '''
    ^
    # An address: username@domain.tld
    
    # Ignore noreply addresses.
    (?!noreply@.*$)
    [\w\d.+-]+      # Username
    @
    ([\w\d.]+\.)+   # Domain name prefix
    (com|org|edu)   # Limit the allowed top-level domains.
    
    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate: ', candidate)
    match = address.search(candidate)

    if match:
        print('  Match: ', candidate[match.start():match.end()])
    else:
        print('  No match')


# The negative look behind assertion after the username is matched using the syntax (?<!pattern).

print('Negative Look behind Assertion:')

address = re.compile(
    '''
    ^
    # An address: username@domain.tld
    [\w\d.+-]+  # Username
    
    # Ignore noreply addresses.
    (?<!noreply)
    
    @
    ([\w\d.]+\.)+   # Domain name prefix
    (com|org|edu)   # Limit the allowed top-level domains
    
    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate: ', candidate)
    match = address.search(candidate)
    if match:
        print('  Match: ', candidate[match.start():match.end()])
    else:
        print('  No match')


# Positive Look Ahead Assertion
# The positive look ahead assertion can be used to find text following a pattern using the syntax (?<=pattern).

twitter = re.compile(
    '''
    # A twitter handle: @username
    (?<=@)
    ([\w\d_]+)  # Username
    ''',
    re.VERBOSE)

text = '''This text includes two Twitter handles.
One for @ThePSF, and one for the author, @doughellmann.
'''

print(text)
for match in twitter.findall(text):
    print('Handle: ', match)


# Self-Referencing Expressions
# Matched values can be used in later parts of an expression. The easiest way to achieve this is by referring to the
# previously matched group by ID number, using \num.

address = re.compile(
    r'''
    # The regular name
    (\w+)   # First name
    \s+
    (([\w.]+)\s+)?  # Optional middle name or initial
    (\w+)           # Last name
    
    \s+
    
    <
    
    # The address: first_name.last_name@domain.tld
    (?P<email>
        \1      # First name
        \.
        \4      # Last name
        @
        ([\w\d.]+\.)+   # Domain name prefix
        (com|org|edu)   # Limit the allowed top-level domains.
    )
    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate: ', candidate)
    match = address.search(candidate)
    if match:
        print('  Match name: ', match.group(1), match.group(4))
        print('  Match email: ', match.group(5))
    else:
        print('  No Match')

# Although the syntax is simple, creating back-references by numerical ID has a few disadvantages. From a practical
# standpoint, as the expression changes, the groups must be counted again and every reference may need to be updated.
# Another disadvantage is that ony 99 references can be made using the standard back-reference syntax \n, because
# if the ID number is three digits long, it will be interpreted as an octal character value instead of a group
# reference. Of course, if there are more than 99 groups in an expression, there will be more serious maintenance
# challenges than simply not being able to refer to all of them.
#
# Python's expression parser includes an extension that uses (?P=name) to refer to the value of a named group matched
# earlier in the expression.

address = re.compile(
    '''
    # The regular name
    (?P<first_name>\w+)
    \s+
    (([\w.]+)\s)?   # Optinal middle name or initial
    (?P<last_name>\w_)
    
    \s+
    
    <
    
    # The address: first_name.last_name@domain.tld
    (?P<email>
        (?P=first_name)
        \.
        (?P=last_name)
        @
        ([\w\d.]+\.)+   # Domain name prefix
        (com|org|edu)   # Limit the allowed top-level domains.
    )
    ''',
    re.VERBOSE | re.IGNORECASE)




