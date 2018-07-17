from src.tokenizer import Tokenizer
from src.token import TokenType


tokenizer1 = Tokenizer("this is a ( test ) string.")
assert(tokenizer1._at_end() == False)

tokenizer2 = Tokenizer("test")
tokenizer2.current = 4
assert(tokenizer2._at_end() == True)

source = "test"
tokenizer3 = Tokenizer(source)
for c in source:
  assert(tokenizer3._consume_current() == c)

t4 = Tokenizer(source)
assert(t4._isalpha('S'))
assert(t4._isalpha('a'))
assert(t4._isalpha('_'))
assert(t4._isalpha('c'))
assert(t4._isalpha('z'))
assert(t4._isalpha('Z'))
assert(t4._isalpha('A'))
assert(not t4._isalpha('!'))
assert(not t4._isalpha('-'))
assert(not t4._isalpha('@'))
assert(not t4._isalpha('`'))
assert(not t4._isalpha('~'))

assert(t4._isdigit('0'))
assert(t4._isdigit('9'))
assert(t4._isdigit('1'))
assert(not t4._isdigit('O'))
assert(not t4._isdigit('@'))
assert(not t4._isdigit('.'))


source = '''def  foo(a, b, c) do
  print "hello, world!"

end
foo()'''
t5 = Tokenizer(source)
tokens = t5.tokenize()
#for token in tokens: print(token) result: passed

source = "print  a   != b"
t6 = Tokenizer(source)
tokens = t6.tokenize()
expected_tokens = [TokenType.PRINT, TokenType.IDENTIFIER, TokenType.BANG_EQUAL, TokenType.IDENTIFIER]
for i, token in enumerate(tokens):
  assert(token.type == expected_tokens[i])


source = "if a or !b"
t7 = Tokenizer(source)
#t7.tokenize()


source = """dec a = 5
print a"""
t8 = Tokenizer(source)
tokens = [str(t) for t in t8.tokenize()]
# print(tokens)

source = """for a in b do
  dec x = 1
end"""
t9 = Tokenizer(source)
tokens = [str(t) for t in t9.tokenize()]
# print(tokens)

print("All tests passed.")