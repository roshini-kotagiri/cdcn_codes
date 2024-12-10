def longest_common_prefix(strings):
    if not strings:
        return ""
    prefix = strings[0]
    for string in strings[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def left_factoring(productions):
    factored_productions = []
    for lhs, rhs_list in productions.items():
        # Find the longest common prefix
        common_prefix = longest_common_prefix(rhs_list)
        if common_prefix:
            new_rhs = [rhs[len(common_prefix):] if rhs.startswith(common_prefix) else rhs for rhs in rhs_list]
            new_lhs = lhs + "'"
            factored_productions.append(f"{lhs}-> {common_prefix}{new_lhs}")
            # Exclude the common prefix and handle epsilon if needed
            non_empty_rhs = [rhs if rhs else 'ε' for rhs in new_rhs]
            factored_productions.append(f"{new_lhs}-> " + " | ".join(non_empty_rhs))
        else:
            # No common prefix found
            factored_productions.append(f"{lhs}-> " + " | ".join(rhs_list))
    return factored_productions

def main():
    productions = {}
    print("Enter grammar productions (one by one):")
    print("Format: <Non-terminal>-> <Production1> | <Production2> ...")
    print("Type 'done' when you're finished.\n")

    while True:
        line = input("Enter production: ").strip()
        if line.lower() == 'done':
            break
        try:
            lhs, rhs = line.split("->")
            lhs = lhs.strip()
            rhs = [prod.strip() for prod in rhs.split('|')]
            productions[lhs] = rhs
        except ValueError:
            print("Invalid format. Use the format '<Non-terminal>-> <Production1> | <Production2>'")
            continue

    factored = left_factoring(productions)
    print("\nLeft Factored Productions:")
    for line in factored:
        print(line)

main()
