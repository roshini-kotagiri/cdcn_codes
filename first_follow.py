from collections import defaultdict
def calc_first(nt, gram, first_cache):
    if nt in first_cache: # Use cached result if available
        return first_cache[nt]
    ff = set()
    productions = gram[nt]
    for production in productions:
        for symbol in production:
            if not symbol.isupper(): # Terminal
                ff.add(symbol)
                break
            else: # Non-terminal
                first_set = calc_first(symbol, gram, first_cache)
                ff.update(first_set- {'#'}) # Add non-epsilon symbols
                if '#' not in first_set: # Stop if epsilon is not in First(symbol)
                    break
        else:
            ff.add('#') # Add epsilon if all symbols can lead to epsilon
    first_cache[nt] = ff # Cache the result
    return ff
 # Function to calculate the Follow set
def calc_follow(nt, gram, first_cache, follow_cache):
    if nt in follow_cache: # Use cached result if available
        return follow_cache[nt]
    fl = set()
    if nt == list(gram.keys())[0]: # Start symbol
        fl.add('$')
    for lhs, productions in gram.items():
        for production in productions:
            for i in range(len(production)):
                if production[i] == nt:
                    if i + 1 < len(production): # There is a symbol after nt
                        next_symbol = production[i + 1]
                        if not next_symbol.isupper(): # Terminal
                            fl.add(next_symbol)
                        else: # Non-terminal
                            first_set = calc_first(next_symbol, gram, first_cache)
                            fl.update(first_set- {'#'})
                        if '#' in first_set: # If epsilon is in First(next_symbol)
                            fl.update(calc_follow(lhs, gram, first_cache, follow_cache))
                    else: # nt is at the end of the production
                        if lhs != nt: # Avoid self-recursion
                            fl.update(calc_follow(lhs, gram, first_cache, follow_cache))
    follow_cache[nt] = fl # Cache the result
    return fl

def main():
    grammar = defaultdict(list)
    print("Enter the grammar (use '#' for epsilon, 'exit' to stop):")
    while True:
        rule = input("Enter a production (e.g., E-> TX or X-> +TX | #): ").strip()
        if rule.lower() == "exit":
            break
        if '->' not in rule:
            print("Invalid input. Ensure productions are in the form 'A-> B'.")
            continue
        lhs, rhs = rule.split('->')
        lhs = lhs.strip()
        productions = [p.strip() for p in rhs.split('|')]
        grammar[lhs].extend(productions)
    if not grammar:
        print("No grammar provided. Exiting.")
        return
 # Calculate First and Follow sets
    first_cache = {}
    follow_cache = {}
    first_sets = {nt: calc_first(nt, grammar, first_cache) for nt in grammar}
    follow_sets = {nt: calc_follow(nt, grammar, first_cache, follow_cache) for nt in grammar}
    print("\nFirst Sets:")
    for nt, first in first_sets.items():
        print(f"First({nt}) = {first}")
    print("\nFollow Sets:")
    for nt, follow in follow_sets.items():
        print(f"Follow({nt}) = {follow}")
    main()