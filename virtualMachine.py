class VirtualMachine:
    def __init__(self, quadruples):
        self.quadruples = quadruples
        self.global_memory = {}
        self.memory_stack = []       # Stack for function activation records
        self.return_stack = []       # Stack for return addresses
        self.current_parameters = [] # Parameters for next function call
        self.ip = 0                  # Instruction pointer
        self.last_return_value = None

    def get_value(self, operand):
        if operand is None:
            return None
            
        # Handle string literals
        if isinstance(operand, str) and operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1].replace('\\n', '\n')
            
        # Handle booleans
        if operand == 'true':
            return True
        if operand == 'false':
            return False
            
        # Handle integers
        try:
            return int(operand)
        except (ValueError, TypeError):
            pass
            
        # Handle floats
        try:
            return float(operand)
        except (ValueError, TypeError):
            pass
            
        # Lookup in current activation record
        if self.memory_stack and operand in self.memory_stack[-1]:
            return self.memory_stack[-1][operand]
            
        # Lookup in global memory
        if operand in self.global_memory:
            return self.global_memory[operand]
            
        return operand

    def set_value(self, address, value):
        if self.memory_stack:
            self.memory_stack[-1][address] = value
        else:
            self.global_memory[address] = value

    def run(self):
        while self.ip < len(self.quadruples):
            quad = self.quadruples[self.ip]
            op = quad.operator
            left = quad.left_operand
            right = quad.right_operand
            res = quad.result

            # Arithmetic and logical operations
            if op in ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=', 'and', 'or']:
                left_val = self.get_value(left)
                right_val = self.get_value(right)
                result_val = None

                if op == '+': result_val = left_val + right_val
                elif op == '-': result_val = left_val - right_val
                elif op == '*': result_val = left_val * right_val
                elif op == '/': result_val = left_val / right_val
                elif op == '>': result_val = left_val > right_val
                elif op == '<': result_val = left_val < right_val
                elif op == '>=': result_val = left_val >= right_val
                elif op == '<=': result_val = left_val <= right_val
                elif op == '==': result_val = left_val == right_val
                elif op == '!=': result_val = left_val != right_val
                elif op == 'and': result_val = left_val and right_val
                elif op == 'or': result_val = left_val or right_val

                self.set_value(res, result_val)
                self.ip += 1

            # Assignment
            elif op == '=':
                value = self.get_value(left)
                self.set_value(res, value)
                self.ip += 1

            # Print statements
            elif op == 'PRINT':
                value = self.get_value(res)
                print(value, end='')
                self.ip += 1

            # Unconditional jump
            elif op == 'GOTO':
                self.ip = int(res) - 1  # Convert quad number to index

            # Jump if false
            elif op == 'GOTOF':
                cond = self.get_value(left)
                if not cond:
                    self.ip = int(res) - 1
                else:
                    self.ip += 1

            # Jump if true (GOTOV)
            elif op == 'GOTOV':
                cond = self.get_value(left)
                if cond:
                    self.ip = int(res) - 1
                else:
                    self.ip += 1

            # Jump to main program
            elif op == 'GOTOMAIN':
                self.ip = int(res) - 1

            # Function parameter setup
            elif op == 'PARAM':
                value = self.get_value(left)
                self.current_parameters.append((res, value))
                self.ip += 1

            # Function call
            elif op == 'GOSUB':
                # Create new activation record
                new_ar = {}
                for param_name, value in self.current_parameters:
                    new_ar[param_name] = value
                self.current_parameters = []
                
                # Save return address (next instruction)
                self.return_stack.append(self.ip + 1)
                
                # Activate new function context
                self.memory_stack.append(new_ar)
                
                # Jump to function start
                self.ip = int(res) - 1

            # Function return
            elif op == 'RETURN':
                if res is not None:
                    self.last_return_value = self.get_value(res)
                self.ip += 1

            # Function cleanup
            elif op == 'ENDFUN':
                if self.memory_stack:
                    self.memory_stack.pop()
                if self.return_stack:
                    return_ip = self.return_stack.pop()
                    self.ip = return_ip
                else:
                    self.ip += 1

            # Handle not operation
            elif op == 'not':
                value = self.get_value(left)
                self.set_value(res, not value)
                self.ip += 1

            # Handle other operations
            else:
                self.ip += 1

# Modify analyze_code to return quadruples for VM execution
def analyze_code(file_path):
    from semanticComp import analyze_code
    return analyze_code(file_path)

# Main execution
if __name__ == "__main__":
    import os
    import parser
    
    # Parse and analyze the code
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "Tests", "prueba6.ld")
    quadruples = analyze_code(file_path)
    
    # Execute the quadruples in VM
    vm = VirtualMachine(quadruples)
    vm.run()