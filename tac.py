import re 
 
class ThreeAddressCode: 
    def __init__(self): 
        self.temp_count = 0 
        self.instructions = [] 
 
    def new_temp(self): 
        """Generate a new temporary variable.""" 
        self.temp_count += 1 
        return f't{self.temp_count}' 
 
    def precedence(self, op): 
        """Return the precedence of the operator.""" 
        if op in ('+', '-'): 
            return 1 
        if op in ('*', '/'): 
            return 2 
        return 0 
 
    def tokenize(self, expression): 
        """ 
        Tokenize the input expression. 
        Handles operands, operators, and parentheses. 
        """ 
        return re.findall(r'[a-zA-Z0-9]+|[-+*/=()]', 
expression) 
 
    def generate_tac(self, expression): 
        """ 
        Generate three address code for a given 
arithmetic expression. 
        Handles assignment operations and operator 
precedence. 
        """ 
        tokens = self.tokenize(expression) 
        if '=' in tokens: 
            # Separate the left-hand side and right-hand 
            lhs = tokens[0] 
            rhs = tokens[2:] 
        else: 
            lhs = None 
            rhs = tokens 
 
        operators = [] 
        output = [] 
 
        # Convert infix to postfix (RPN) for the right-hand 
        for token in rhs: 
            if token.isalnum():  # Operand 
                output.append(token) 
            elif token in "+-*/":  # Operator 
                while (operators and 
                       operators[-1] != '(' and 
                       self.precedence(operators[-1]) >= 
self.precedence(token)): 
                    output.append(operators.pop()) 
                operators.append(token) 
            elif token == '(': 
                operators.append(token) 
            elif token == ')': 
                while operators and operators[-1] != '(': 
                    output.append(operators.pop()) 
                operators.pop() 
 
        while operators: 
            output.append(operators.pop()) 
 
        # Generate TAC for the postfix expression 
        stack = [] 
        for token in output: 
            if token.isalnum(): 
                stack.append(token) 
            elif token in "+-*/": 
                op2 = stack.pop() 
                op1 = stack.pop() 
                temp = self.new_temp() 
                self.instructions.append(f"{temp} = {op1} 
{token} {op2}") 
                stack.append(temp) 
 
        # Handle assignment to the left-hand side 

        if lhs: 
            final_result = stack.pop() 
            self.instructions.append(f"{lhs} = {final_result}") 
        return lhs if lhs else stack[-1] 
 
    def display_instructions(self): 
        """Print all generated TAC instructions.""" 
        print("Three Address Code Instructions:") 
        for instruction in self.instructions: 
            print(instruction) 
 
 
# Example usage 
if __name__ == "__main__": 
    expression = input("Enter the expression :- ") 
    tac_generator = ThreeAddressCode() 
    try: 
        final_result = tac_generator.generate_tac(expression) 
        tac_generator.display_instructions() 
        print(f"Final result is stored in: {final_result}") 
    except IndexError: 
        print("Error: Invalid expression!")