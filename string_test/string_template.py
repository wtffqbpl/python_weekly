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
        print("'{}' ({})\n".format(pattern, desc))
        print("  '{}".format(text))
        for match in re.finditer(pattern, text):
            s, e = match.start(), match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\')
            prefix = '.' * (s + n_backslashes)
            print("  {}'{}'".format(prefix, substr))
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
