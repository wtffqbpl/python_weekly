#! coding: utf-8

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

class MyDocument(Document):
    def __init__(self):
        super().__init__()

        self.preamble.append(Command('title', 'Awesome Title'))
        self.preamble.append(Command('author', 'Anonymous Author'))
        self.preamble.append(Command('date', NoEscape(r'\today')))
        self.append(NoEscape(r'\maketitle'))

    def fill_document(self):
        """Add a section, a subsection and some text to the document."""
        with self.create(Section('A section')):
            self.append('Some regular text and some ')
            self.append(italic('italic text. '))

        with self.create(Subsection('A subsection')):
            self.append('Also some crazy characters: $&#{}')


if __name__ == '__main__':
    # Document
    doc = MyDocument()

    # Call function to add text
    doc.fill_document()

    # Second section
    doc.fill_document()

    # Third section
    doc.fill_document()

    doc.generate_pdf('basic_inheritance', clean_tex=False)
    tex = doc.dumps()
    print(tex)