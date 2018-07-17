from .token import *
from .errors import SardineSyntaxError, error

class Tokenizer:
  def __init__(self, source):
    self.source = source
    self.line = 1
    self.start = 0
    self.current = 0
    self.source_length = len(source)
    self.tokens = []
    self.import_flag = False

    # symbol tables
    self.keywords = {
      'and': TokenType.AND,
      'or': TokenType.OR,
      'not': TokenType.NOT,
      'do': TokenType.DO,
      'end': TokenType.END,
      'None': TokenType.NONE,
      'True': TokenType.TRUE,
      'False': TokenType.FALSE,
      'while': TokenType.WHILE,
      'for': TokenType.FOR,
      'return': TokenType.RETURN,
      'print': TokenType.PRINT,
      'def': TokenType.DEF,
      'dec': TokenType.DEC,
      'if': TokenType.IF,
      'else': TokenType.ELSE,
    }

    self.newline_triggers = set([
      TokenType.IDENTIFIER,
      TokenType.STRING,
      TokenType.NUMBER,
      TokenType.TRUE,
      TokenType.FALSE,
      TokenType.RETURN,
      TokenType.RIGHT_PAREN,
    ])

  def tokenize(self):
    while not self._at_end():
      self.start = self.current
      self._scan_token()
    return self.tokens

  def _scan_token(self):
    c = self._consume_current()
    if c == '(': self._add_token(TokenType.LEFT_PAREN)
    elif c == ')': self._add_token(TokenType.RIGHT_PAREN)
    elif c == ',': self._add_token(TokenType.COMMA)
    elif c == '-': self._add_token(TokenType.MINUS)
    elif c == '+': self._add_token(TokenType.PLUS)
    elif c == '*': self._add_token(TokenType.STAR)
    elif c == '/': self._add_token(TokenType.SLASH)
    elif c == '=': self._add_token(TokenType.EQUAL_EQUAL) if self._match_and_consume('=') else self._add_token(TokenType.EQUAL)
    elif c == '<': self._add_token(TokenType.LESS_EQUAL) if self._match_and_consume('=') else self._add_token(TokenType.LESS)
    elif c == '>': self._add_token(TokenType.GREATER_EQUAL) if self._match_and_consume('=') else self._add_token(TokenType.GREATER)
    elif c == '!':
      if self._match_and_consume('='):
        self._add_token(TokenType.BANG_EQUAL)
      else:
        SardineLang.error(SardineSyntaxError('SyntaxError', self.line, self.source[self.current])) 
    elif c == '#':
      while self._peek() != '\n' and not self._at_end(): self._consume_current()
    elif c in [' ', '\r', '\t']:
      pass
    elif c == '\n':
      self.line += 1
      if len(self.tokens) > 0 and self.tokens[-1].type in self.newline_triggers:
        self._add_token(TokenType.NEWLINE)
    elif c == '"':
      self._consume_string()
    else:
      if self._isdigit(c):
        self._consume_number()
      elif self._isalpha(c):
        self._consume_identifier()
      else:
        SardineLang.error(SardineSyntaxError('SyntaxError', self.line, self.source[self.current])) 


  def _consume_identifier(self):
    while self._isalphanumeric(self._peek()): self._consume_current()

    text = self.source[self.start:self.current]

    if text == "import":
      self.import_flag = True
    elif self.import_flag:
      with open(text + '.sd', 'r') as f:
        tokenizer = Tokenizer(f.read() + '\n')
        tokens = tokenizer.tokenize()
        self.tokens += tokens
        self.import_flag = False
    else:
      token_type = self.keywords.get(text, TokenType.IDENTIFIER)
      self._add_token(token_type, text)

  def _isalphanumeric(self, c):
    return self._isalpha(c) or self._isdigit(c)

  def _isalpha(self, c):
    return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

  def _consume_number(self):
    while self._isdigit(self._peek()): self._consume_current()
    if self._match_and_consume('.'):
      while self._isdigit(self._peek()): self._consume_current()
    
    value = float(self.source[self.start:self.current])
    self._add_token(TokenType.NUMBER, value)

  def _isdigit(self, c):
    return c >= '0' and c <= '9'

  def _consume_string(self):
    while self._peek() != '"' and not self._at_end():
      if self._peek() == '\n': self.line += 1
      self._consume_current()
    
    if self._at_end():
      SardineLang.error(SardineSyntaxError('SyntaxError', self.line, self.source[self.current])) 
    
    self._consume_current()
    raw_string = self.source[self.start+1:self.current-1]
    self._add_token(TokenType.STRING, raw_string)

  def _peek(self):
    # returns current character without advancing current pointer
    if self._at_end(): return '\0'
    return self.source[self.current]

  def _match_and_consume(self, char):
    # returns True if current character equals char, and increments current pointer, else returns False
    if self._at_end():
      return False
    if self.source[self.current] != char:
      return False
    self.current += 1
    return True

  def _consume_current(self):
    # consumes the current character, advances current pointer, and returns the character
    current_char = self.source[self.current]
    self.current += 1
    return current_char

  def _at_end(self):
    return self.current >= self.source_length

  def _add_token(self, token_type, value=None):
    raw_token = self.source[self.start:self.current]
    self.tokens.append(Token(token_type, raw_token, value, self.line))