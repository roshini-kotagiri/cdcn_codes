class ASTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value  # Operator or Operand (variable or constant)
        self.left = left    # Left child (could be operand or another operator)
        self.right = right  # Right child (could be operand or another operator)


# Code generator for Three-Address Code (TAC)
class CodeGenerator:
    def __init__(self):
        self.temp_count = 1  # To create unique temporary variables (t1, t2, etc.)
        self.tac = []        # List to store Three-Address Code (TAC)

    def generate_TAC(self, node):
        """Recursively generate TAC from AST."""
        if node is None:
            return

        if node.value == '=':
            # Assignment operation: lhs = rhs
            lhs = node.left.value
            rhs = self.generate_TAC(node.right)
            self.tac.append(f"{lhs} = {rhs}")
            return lhs

        elif node.value == '+':
            # Addition operator
            left = self.generate_TAC(node.left)
            right = self.generate_TAC(node.right)
            temp_var = f"t{self.temp_count}"
            self.tac.append(f"{temp_var} = {left} + {right}")
            self.temp_count += 1
            return temp_var

        elif node.value == '*':
            # Multiplication operator
            left = self.generate_TAC(node.left)
            right = self.generate_TAC(node.right)
            temp_var = f"t{self.temp_count}"
            self.tac.append(f"{temp_var} = {left} * {right}")
            self.temp_count += 1
            return temp_var

        else:
            # Leaf node (variable or constant)
            return node.value

    def get_TAC(self):
        return self.tac


# Code generator for Assembly Code
class AssemblyCodeGenerator:
    def __init__(self):
        self.assembly_code = []  # List to store the generated assembly code

    def generate_assembly(self, tac):
        """Generate assembly code from TAC."""
        for instruction in tac:
            lhs, rhs = instruction.split(" = ")
            lhs = lhs.strip()
            rhs = rhs.strip()

            if "+" in rhs:
                # Handle addition
                operand1, operand2 = rhs.split(" + ")
                self.assembly_code.append(f"LOAD {operand1}")
                self.assembly_code.append(f"ADD {operand2}")
                self.assembly_code.append(f"STORE {lhs}")
            elif "*" in rhs:
                # Handle multiplication
                operand1, operand2 = rhs.split(" * ")
                self.assembly_code.append(f"LOAD {operand1}")
                self.assembly_code.append(f"MUL {operand2}")
                self.assembly_code.append(f"STORE {lhs}")
            else:
                # Handle assignment
                self.assembly_code.append(f"LOAD {rhs}")
                self.assembly_code.append(f"STORE {lhs}")

        return self.assembly_code


# Simple parser to convert the input expression to AST
def parse_expression(expression):
    """Simple function to create an AST for basic expressions like a = b + c * d."""
    # Clean up the expression
    expression = expression.replace(" ", "")

    # Find assignment operator
    if '=' in expression:
        lhs, rhs = expression.split('=')
        lhs = lhs.strip()

        # Handle operators in the right-hand side
        if '+' in rhs:
            if '*' in rhs:
                # Handle a = b + c * d
                parts = rhs.split('+')
                left = parts[0].strip()
                right = parts[1].strip()
                mult_left, mult_right = right.split('*')
                return ASTNode('=',
                               ASTNode(lhs),
                               ASTNode('+',
                                       ASTNode(left),
                                       ASTNode('*',
                                               ASTNode(mult_left.strip()),
                                               ASTNode(mult_right.strip()))))
            else:
                # Handle a = b + c
                left, right = rhs.split('+')
                return ASTNode('=',
                               ASTNode(lhs),
                               ASTNode('+',
                                       ASTNode(left.strip()),
                                       ASTNode(right.strip())))

        elif '*' in rhs:
            # Handle a = b * c
            left, right = rhs.split('*')
            return ASTNode('=',
                           ASTNode(lhs),
                           ASTNode('*',
                                   ASTNode(left.strip()),
                                   ASTNode(right.strip())))

        else:
            # Handle a = b
            return ASTNode('=',
                           ASTNode(lhs),
                           ASTNode(rhs.strip()))

    return None


# Main program to handle user input and generate the code
def main():
    # Get input from the user
    expression = input("Enter an expression (e.g., a = b + c * d): ")
    
    # Parse the input expression into an AST
    ast = parse_expression(expression)
    if not ast:
        print("Invalid expression!")
        return
    
    # Generate Three-Address Code (TAC)
    code_generator = CodeGenerator()
    code_generator.generate_TAC(ast)
    tac = code_generator.get_TAC()
    
    print("\nThree-Address Code (TAC):")
    for line in tac:
        print(line)
    
    # Generate Assembly Code from TAC
    assembly_generator = AssemblyCodeGenerator()
    assembly_code = assembly_generator.generate_assembly(tac)
    
    print("\nAssembly Code:")
    for line in assembly_code:
        print(line)


if __name__ == "__main__":
    main()
