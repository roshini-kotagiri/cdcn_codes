def eliminate_left_recursion(production):
    lhs, rhs = production.split("->")
    lhs = lhs.strip()
    rhs = [p.strip() for p in rhs.split("|")]
 # Separate α (left-recursive) and β (non-recursive)
    alpha = []
    beta = []
    for prod in rhs:
        if prod.startswith(lhs): # Left-recursive part
            alpha.append(prod[len(lhs):].strip())
        else: # Non-recursive part
            beta.append(prod)
 # Check for left recursion
    if not alpha:
        print(f"No left recursion in the production: {production}")
        return
 # Generate new productions
    new_non_terminal = lhs + "'"
    print("Transformed Productions:")
    for b in beta:
        print(f"{lhs}-> {b}{new_non_terminal}")
    for a in alpha:
        print(f"{new_non_terminal}-> {a}{new_non_terminal}")
        print(f"{new_non_terminal}-> ε")
 # Example call
production = input("Enter a production (e.g., A-> Aα | β): ").strip()
eliminate_left_recursion(production)