import re

# Define the keywords, operators, and logical operators
keywords = {"if", "while", "else", "return", "int", "float", "void", "for", "switch", "case"}
operators = {'+', '-', '*', '/', '=', '%'}
logical_ops = {'&', '|', '!', '^'}

# Function to identify the type of token
def identify(token):
    if token in keywords:
        return "keyword"
    elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", token):
        return "identifier"
    elif token in operators:
        return "arithmetic operator"
    elif token in logical_ops:
        return "logical operator"
    elif re.match(r"[0-9]+", token):
        return "number"
    else:
        return "unknown"

# Function to parse and tokenize the code
def parse(code):
    # Tokenize the input code using regular expressions to capture keywords, operators,
    # numbers, and other symbols
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|[+\-/=(),;{}[\]<>!&|^]", code)
    for token in tokens:
        token_type = identify(token)
        print(f"Token: {token} - Type: {token_type}")

# Main function to test the program
def main():
    code = "int main() { int a = 10; }"  # Sample code
    parse(code)

# Run the program
main()
