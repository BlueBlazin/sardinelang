from src.tokenizer import Tokenizer
from src.parser import Parser

def get_stmts(source):
  tokenizer = Tokenizer(source)
  tokens = tokenizer.tokenize()
  parser = Parser(tokens)
  return parser.parse()

# source = "(1 + 3) * 2"
# print(print_ast(source))
# print("")

# source = "10 / (3 + 7)   + 4"
# print(print_ast(source))


source = '''

dec a = 5
dec b = 2

print "Lucky number: "
a * b

'''

statements = get_stmts(source)

for stmt in statements:
  print(stmt)