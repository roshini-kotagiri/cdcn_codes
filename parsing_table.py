from collections import defaultdict

# Function to build the predictive parsing table
def build_parse_table(gram):
    parse_table = {}
    for nt, productions in gram.items():
        for production in productions:
            if not production[0].isupper() and production[0] != '#':
                parse_table[(nt, production[0])] = production
            else:
                first_set = calc_first(production[0], gram, {})
                for terminal in first_set:
                    if terminal != '#':
                        parse_table[(nt, terminal)] = production
                if '#' in first_set or production[0] == '#':
                    follow_set = calc_follow(nt, gram, {}, {})
                    for follow_symbol in follow_set:
                        if follow_symbol not in {'$', '\0'}:
                            parse_table[(nt, follow_symbol)] = '#'
    return parse_table

# Function to parse a string using the predictive parsing table
def parse_string(input_str, parse_table, start_symbol):
    stack = ['$']
    stack.append(start_symbol)
    i = 0
    while stack:
        top = stack[-1]
        current = input_str[i] if i < len(input_str) else '$'
        if top == current:
            stack.pop()
            i += 1
        elif not top.isupper():  # Mismatch, parsing fails
            return False
        elif (top, current) in parse_table:
            stack.pop()
            production = parse_table[(top, current)]
            if production != "#":
                stack.extend(reversed(production))  # Push production in reverse order
        else:
            return False  # No matching entry in the parse table
    return i == len(input_str)

def display_parse_table(parse_table):
    print("\nPredictive Parsing Table:")
    for (nt, terminal), production in parse_table.items():
        print(f"M[{nt}, {terminal}] = {production}")

def main():
    n = int(input("Enter the number of lines in the grammar: "))
    gram = defaultdict(list)
    print("Enter the different lines of grammar:")
    for _ in range(n):
        s = input().strip()
        lhs = s[0]
        productions = s[3:].split('/')  # Split productions
        gram[lhs].extend(productions)

    # Initialize caches
    first_cache = {}
    follow_cache = {}

    # Compute First and Follow sets
    first = {lhs: calc_first(lhs, gram, first_cache) for lhs in gram.keys()}
    follow = {lhs: calc_follow(lhs, gram, first_cache, follow_cache) for lhs in gram.keys()}

    # Display First and Follow sets
    for lhs, first_set in first.items():
        print(f"First of {lhs} {{{', '.join(first_set)}}}")
    for lhs, follow_set in follow.items():
        print(f"Follow of {lhs} {{{', '.join(follow_set)}}}")

    # Build the predictive parsing table
    parse_table = build_parse_table(gram)

    # Display the parsing table
    display_parse_table(parse_table)

    # Parse the input string
    input_str = input("Enter the string to parse (end with $): ")
    if parse_string(input_str, parse_table, list(gram.keys())[0]):
        print("The string is accepted by the grammar.")
    else:
        print("The string is rejected by the grammar.")

main()
