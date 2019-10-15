from misaka import Markdown, HtmlRenderer
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

class HighlightRenderer(HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            # To not require <?php for php highlighting
            lexer.startinline = True
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        return '\n<pre><code>{}</code></pre>\n'.format(text.strip())

md = Markdown(HighlightRenderer(), extensions=('fenced-code',))
