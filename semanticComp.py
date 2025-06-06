import parser
import os

class FunctionDirectory:
    def __init__(self):
        self.functions = {}
        self.current_scope = 'global'
    
    def add_function(self, name, return_type, params=None):
        if name in self.functions:
            return False
        
        self.functions[name] = {
            'return_type': return_type,
            'params': params or [],
            'local_vars': SymbolTable(),
            'param_count': len(params) if params else 0,
            'start_quad': None
        }
        return True
    
    def exists(self, name):
        return name in self.functions
    
    def get_function(self, name):
        return self.functions.get(name)
    
    def set_start_quad(self, name, quad):
        if name in self.functions:
            self.functions[name]['start_quad'] = quad

class SymbolTable:
    def __init__(self):
        self.scopes = {'global': {}}
        self.current_scope = 'global'
    
    def add_symbol(self, name, symbol_type, value=None, scope=None):
        target_scope = scope or self.current_scope
        if target_scope not in self.scopes:
            self.scopes[target_scope] = {}
        
        if name in self.scopes[target_scope]:
            return False
            
        self.scopes[target_scope][name] = {
            'type': symbol_type,
            'value': value
        }
        return True
    
    def exists(self, name, scope=None):
        target_scope = scope or self.current_scope
        if target_scope in self.scopes and name in self.scopes[target_scope]:
            return True
        if target_scope != 'global' and name in self.scopes['global']:
            return True
        return False
    
    def get_type(self, name, scope=None):
        target_scope = scope or self.current_scope
        if target_scope in self.scopes and name in self.scopes[target_scope]:
            return self.scopes[target_scope][name]['type']
        if target_scope != 'global' and name in self.scopes['global']:
            return self.scopes['global'][name]['type']
        return None
    
    def create_scope(self, scope_name):
        if scope_name not in self.scopes:
            self.scopes[scope_name] = {}
            return True
        return False
    
    def set_current_scope(self, scope_name):
        if scope_name in self.scopes:
            self.current_scope = scope_name
            return True
        return False

class SemanticCube:
    def __init__(self):
        self.types = ['int', 'float', 'string', 'bool']
        
        self.operators = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=', 'and', 'or', 'not', '=']
        
        self.cube = {}
        
        self._initialize_cube()
    
    def _initialize_cube(self):
        self._set_rule('int', '+', 'int', 'int')
        self._set_rule('int', '+', 'float', 'float')
        self._set_rule('float', '+', 'int', 'float')
        self._set_rule('float', '+', 'float', 'float')
        self._set_rule('string', '+', 'string', 'string')
        self._set_rule('int', '-', 'int', 'int')
        self._set_rule('int', '-', 'float', 'float')
        self._set_rule('float', '-', 'int', 'float')
        self._set_rule('float', '-', 'float', 'float')
        self._set_rule('int', '*', 'int', 'int')
        self._set_rule('int', '*', 'float', 'float')
        self._set_rule('float', '*', 'int', 'float')
        self._set_rule('float', '*', 'float', 'float')
        self._set_rule('int', '/', 'int', 'float')
        self._set_rule('int', '/', 'float', 'float')
        self._set_rule('float', '/', 'int', 'float')
        self._set_rule('float', '/', 'float', 'float')
        
        for type1 in ['int', 'float']:
            for type2 in ['int', 'float']:
                for op in ['>', '<', '>=', '<=', '==', '!=']:
                    self._set_rule(type1, op, type2, 'bool')
        
        for op in ['==', '!=']:
            self._set_rule('string', op, 'string', 'bool')
        
        for op in ['and', 'or']:
            self._set_rule('bool', op, 'bool', 'bool')
        
        self._set_rule('bool', 'not', None, 'bool')
        self._set_rule('int', '=', 'int', 'int')
        self._set_rule('float', '=', 'int', 'float')
        self._set_rule('float', '=', 'float', 'float')
        self._set_rule('string', '=', 'string', 'string')
        self._set_rule('bool', '=', 'bool', 'bool')
    
    def _set_rule(self, left_type, operator, right_type, result_type):
        key = (left_type, operator, right_type)
        self.cube[key] = result_type
    
    def get_result_type(self, left_type, operator, right_type=None):
        key = (left_type, operator, right_type)
        if key in self.cube:
            return self.cube[key]
        else:
            return "error"

class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
        self.result_type = None

class TempManager:
    def __init__(self):
        self.counter = 0
    
    def get_next_temp(self):
        temp = f"t{self.counter}"
        self.counter += 1
        return temp

class SemanticAnalyzer:
    def __init__(self):
        self.function_directory = FunctionDirectory()
        self.symbol_table = SymbolTable()
        self.semantic_cube = SemanticCube()
        self.temp_manager = TempManager()
        
        self.operand_stack = []
        self.type_stack = []
        self.operator_stack = []
        self.scope_stack = ['global']
        
        self.quadruples = []
        self.jump_stack = []
        self.quad_counter = 0
        
        self.symbol_table.create_scope('global')
        self.current_scope = 'global'
        self.current_function = None
    
    def add_quadruple(self, operator, left_operand, right_operand, result):
        quad = Quadruple(operator, left_operand, right_operand, result)
        
        if isinstance(result, str) and result.startswith('t'):
            if left_operand is None:
                operand_type = self.get_operand_type(right_operand)
                if operator == 'not':
                    quad.result_type = self.semantic_cube.get_result_type(operand_type, operator, None)
                else:
                    quad.result_type = operand_type
            elif right_operand is None:
                operand_type = self.get_operand_type(left_operand)
                quad.result_type = operand_type
            else:
                left_type = self.get_operand_type(left_operand)
                right_type = self.get_operand_type(right_operand)
                quad.result_type = self.semantic_cube.get_result_type(left_type, operator, right_type)
        elif result:
            quad.result_type = self.get_operand_type(result)
        
        self.quadruples.append(quad)
        self.quad_counter += 1
        return self.quad_counter - 1
    
    def get_current_scope(self):
        return self.scope_stack[-1]
    
    def enter_scope(self, scope_name):
        self.scope_stack.append(scope_name)
        self.symbol_table.create_scope(scope_name)
        self.symbol_table.set_current_scope(scope_name)
    
    def exit_scope(self):
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.symbol_table.set_current_scope(self.scope_stack[-1])
    
    def process_function_definition(self, statement):
        if statement[0] != 'function_definition':
            return False

        func_name = statement[1]
        param_list = statement[2]
        return_type = statement[3]
        vars_and_body = statement[4]
        
        params = param_list if param_list else []
        if not self.function_directory.add_function(func_name, return_type, params):
            return False
        
        start_quad = self.quad_counter
        self.function_directory.set_start_quad(func_name, start_quad)
        
        self.enter_scope(func_name)
        self.current_function = func_name
        
        for param_name, param_type in params:
            if not self.symbol_table.add_symbol(param_name, param_type):
                print(f"Error semántico: El parámetro '{param_name}' ya está definido en la función '{func_name}'")
                return False
        
        body = None
        local_vars = None

        if isinstance(vars_and_body, tuple) and len(vars_and_body) == 2:
            if isinstance(vars_and_body[0], tuple) and vars_and_body[0][0] == 'vars':
                local_vars = vars_and_body[0][1]
            if isinstance(vars_and_body[1], tuple) and vars_and_body[1][0] == 'body':
                body = vars_and_body[1]

        if local_vars is not None:
            if not self.process_vars(local_vars):
                return False

        if isinstance(vars_and_body, tuple):
            if vars_and_body[0] == 'vars':
                if not self.process_vars(vars_and_body[1]):
                    return False
                for item in vars_and_body[1:]:
                    if isinstance(item, tuple) and item[0] == 'body':
                        body = item
                        break
            elif vars_and_body[0] == 'body':
                body = vars_and_body
        
        if body and body[0] == 'body':
            for var_name, var_details in self.symbol_table.scopes['global'].items():
                if not self.symbol_table.exists(var_name, func_name):
                    self.symbol_table.add_symbol(var_name, var_details['type'], scope=func_name)
            
            if not self.process_body(body[1]):
                return False
        
        self.add_quadruple('ENDFUN', None, None, None)
        
        self.exit_scope()
        self.current_function = None
        
        return True
    
    def process_function_call(self, statement):
        func_name = statement[1]
        args = statement[2]
        
        if not self.function_directory.exists(func_name):
            print(f"Error semántico: La función '{func_name}' no está definida")
            return False
        
        func_info = self.function_directory.get_function(func_name)
        
        if len(args) != func_info['param_count']:
            print(f"Error semántico: La función '{func_name}' espera {func_info['param_count']} argumentos, pero se proporcionaron {len(args)}")
            return False
        
        for i, (arg, (param_name, param_type)) in enumerate(zip(args, func_info['params'])):
            if isinstance(arg, tuple):
                if arg[0] == 'factor':
                    value = arg[1]
                else:
                    self.process_expression(arg)
                    value = self.operand_stack.pop()
                    self.type_stack.pop()
            else:
                value = arg
                
            arg_type = self.get_operand_type(value)
            if arg_type != param_type:
                print(f"Error semántico: El argumento {i+1} de la función '{func_name}' debe ser de tipo {param_type}, pero se proporcionó {arg_type}")
                return False
                
            self.add_quadruple('PARAM', value, None, param_name)
        
        start_quad = func_info['start_quad']
        if start_quad is None:
            print(f"Error semántico: La función '{func_name}' no tiene un punto de inicio definido")
            return False
            
        self.add_quadruple('GOSUB', func_name, None, start_quad + 1)
        
        return True
    
    def get_operand_type(self, operand):
        if operand is None:
            return None

        current_scope = self.get_current_scope()

        if isinstance(operand, str):
            if self.symbol_table.exists(operand, current_scope):
                return self.symbol_table.get_type(operand, current_scope)

            if operand.startswith('t'):
                for quad in reversed(self.quadruples):
                    if quad.result == operand:
                        return quad.result_type
                return None

            if operand.startswith('"') and operand.endswith('"'):
                return 'string'

            try:
                float(operand)
                if '.' in operand:
                    return 'float'
                return 'int'
            except ValueError:
                if operand in ('true', 'false'):
                    return 'bool'

        elif isinstance(operand, int):
            return 'int'
        elif isinstance(operand, float):
            return 'float'
        elif isinstance(operand, bool):
            return 'bool'

        return None
    
    def analyze_program(self, ast):
        if ast[0] == 'programa':
            if ast[2] and ast[2][0] == 'vars':
                if not self.process_vars(ast[2][1]):
                    return False
            
            main_jump_quad = self.add_quadruple('GOTOMAIN', None, None, None)
            
            funcs, main_section = ast[3]
            if funcs is not None:
                if isinstance(funcs, list):
                    for func in funcs:
                        if not self.process_function_definition(func):
                            return False
                else:
                    if not self.process_function_definition(funcs):
                        return False
            
            main_start = self.quad_counter + 1
            self.quadruples[main_jump_quad].result = main_start
            
            if main_section[0] == 'main' and isinstance(main_section[1], tuple) and main_section[1][0] == 'body':
                if not self.process_body(main_section[1][1]):
                    return False
            
            return True
        return False

    def process_vars(self, var_statements):
        for var_decl in var_statements:
            if var_decl[0] == 'var_decl':
                for id_list, var_type in var_decl[1]:
                    for var_id in id_list:
                        current_scope = self.get_current_scope()
                        if self.symbol_table.exists(var_id, current_scope) and not self.symbol_table.exists(var_id, 'global'):
                            print(f"Error semántico: Variable '{var_id}' redeclarada en el scope actual")
                            return False
                        
                        self.symbol_table.add_symbol(var_id, var_type, scope=current_scope)
                        
                        if current_scope != 'global' and self.current_function:
                            func_info = self.function_directory.get_function(self.current_function)
                            if func_info:
                                func_info['local_vars'].add_symbol(var_id, var_type)
        
        return True
    
    def process_body(self, statements):
        if not statements:
            return True
            
        for statement in statements:
            if isinstance(statement, tuple):
                if statement[0] == 'assign':
                    var_id = statement[1]
                    expr = statement[2]
                    
                    if isinstance(expr, tuple):
                        if not self.process_expression(expr):
                            return False
                        result = self.operand_stack.pop()
                        result_type = self.type_stack.pop()
                        
                        var_type = self.get_operand_type(var_id)
                        if var_type is None:
                            print(f"Error semántico: Variable '{var_id}' no está definida")
                            return False
                        
                        self.add_quadruple('=', result, None, var_id)
                    else:
                        var_type = self.get_operand_type(var_id)
                        if var_type is None:
                            print(f"Error semántico: Variable '{var_id}' no está definida")
                            return False
                            
                        value_type = self.get_operand_type(expr)
                        if value_type is None:
                            print(f"Error semántico: Valor inválido '{expr}'")
                            return False
                            
                        self.add_quadruple('=', expr, None, var_id)
                
                elif statement[0] == 'if_else_stmt':
                    if not self.process_if_statement(statement):
                        return False
                    
                elif statement[0] == 'print':
                    if isinstance(statement[1], str):
                        self.add_quadruple('PRINT', None, None, f'"{statement[1]}"')
                        self.add_quadruple('PRINT', None, None, '"\\n"')
                    else:
                        if not self.process_expression(statement[1]):
                            return False
                        result = self.operand_stack.pop()
                        self.type_stack.pop()
                        self.add_quadruple('PRINT', None, None, result)
                        self.add_quadruple('PRINT', None, None, '"\\n"')
                        
                elif statement[0] == 'function_call':
                    if not self.process_function_call(statement):
                        return False
                        
                elif statement[0] == 'return':
                    if statement[1] is not None:
                        if not self.process_expression(statement[1]):
                            return False
                        return_value = self.operand_stack.pop()
                        self.type_stack.pop()
                        self.add_quadruple('RETURN', None, None, return_value)
                    else:
                        self.add_quadruple('RETURN', None, None, None)
                        
                elif statement[0] == 'body':
                    if not self.process_body(statement[1]):
                        return False
                        
                elif statement[0] == 'exp':
                    if not self.process_expression(statement):
                        return False
                    if self.operand_stack:
                        self.operand_stack.pop()
                        self.type_stack.pop()

                elif statement[0] == 'do_while':
                    if not self.process_do_while(statement):
                        return False

                   
        return True
    
    def process_expression(self, expression):

        if isinstance(expression, tuple) and expression[0] == 'expresion':
            expression = ('exp', expression[1], expression[2], expression[3])

        if isinstance(expression, tuple):
            if expression[0] == 'exp':
                if len(expression) == 2:
                    return self.process_expression(expression[1])
                else:
                    operator = expression[1]
                    left_operand = expression[2]
                    right_operand = expression[3]
                    
                    if isinstance(left_operand, tuple):
                        if not self.process_expression(left_operand):
                            return False
                        left_value = self.operand_stack.pop()
                        left_type = self.type_stack.pop()
                    else:
                        left_value = left_operand
                        left_type = self.get_operand_type(left_value)
                    
                    if isinstance(right_operand, tuple):
                        if not self.process_expression(right_operand):
                            return False
                        right_value = self.operand_stack.pop()
                        right_type = self.type_stack.pop()
                    else:
                        right_value = right_operand
                        right_type = self.get_operand_type(right_value)
                    
                    result_type = self.semantic_cube.get_result_type(left_type, operator, right_type)
                    if result_type == "error":
                        print(f"Error semántico: Operación inválida {left_type} {operator} {right_type}")
                        return False
                    
                    temp = self.temp_manager.get_next_temp()
                    self.add_quadruple(operator, left_value, right_value, temp)
                    
                    self.operand_stack.append(temp)
                    self.type_stack.append(result_type)
            
            elif expression[0] == 'factor_paren':
                if not self.process_expression(expression[1]):
                    return False
                return True

            elif expression[0] == 'factor':
                value = expression[1]
                value_type = self.get_operand_type(value)
                self.operand_stack.append(value)
                self.type_stack.append(value_type)
                
            elif expression[0] == 'termino':
                if len(expression) == 2:
                    return self.process_expression(expression[1])
                else:
                    operator = expression[1]
                    left_operand = expression[2]
                    right_operand = expression[3]
                    
                    if isinstance(left_operand, tuple):
                        if not self.process_expression(left_operand):
                            return False
                        left_value = self.operand_stack.pop()
                        left_type = self.type_stack.pop()
                    else:
                        left_value = left_operand
                        left_type = self.get_operand_type(left_value)
                    
                    if isinstance(right_operand, tuple):
                        if not self.process_expression(right_operand):
                            return False
                        right_value = self.operand_stack.pop()
                        right_type = self.type_stack.pop()
                    else:
                        right_value = right_operand
                        right_type = self.get_operand_type(right_value)
                    
                    temp = self.temp_manager.get_next_temp()
                    self.add_quadruple(operator, left_value, right_value, temp)
                    
                    self.operand_stack.append(temp)
                    result_type = self.semantic_cube.get_result_type(left_type, operator, right_type)
                    self.type_stack.append(result_type)
                    
            elif expression[0] == 'expresion':
                if len(expression) == 2:
                    return self.process_expression(expression[1])
                else:
                    operator = expression[1]
                    left_operand = expression[2]
                    right_operand = expression[3]
                    
                    if isinstance(left_operand, tuple):
                        if not self.process_expression(left_operand):
                            return False
                        left_value = self.operand_stack.pop()
                        left_type = self.type_stack.pop()
                    else:
                        left_value = left_operand
                        left_type = self.get_operand_type(left_value)
                    
                    if isinstance(right_operand, tuple):
                        if not self.process_expression(right_operand):
                            return False
                        right_value = self.operand_stack.pop()
                        right_type = self.type_stack.pop()
                    else:
                        right_value = right_operand
                        right_type = self.get_operand_type(right_value)
                    
                    temp = self.temp_manager.get_next_temp()
                    self.add_quadruple(operator, left_value, right_value, temp)
                    
                    self.operand_stack.append(temp)
                    result_type = self.semantic_cube.get_result_type(left_type, operator, right_type)
                    self.type_stack.append(result_type)
                    
        else:
            value_type = self.get_operand_type(expression)
            self.operand_stack.append(expression)
            self.type_stack.append(value_type)
        
        return True
    
    def process_if_statement(self, statement):
        if not self.process_expression(statement[1]):
            return False

        condition_result = self.operand_stack.pop()
        condition_type = self.type_stack.pop()

        if condition_type != 'bool':
            print(f"Error semántico: La condición debe ser de tipo bool, se encontró {condition_type}")
            return False

        gotof_index = self.add_quadruple('GOTOF', condition_result, None, None)

        if not self.process_body(statement[2][1]):
            return False

        goto_index = self.add_quadruple('GOTO', None, None, None)

        self.quadruples[gotof_index].result = self.quad_counter + 1

        if statement[3] is not None:
            if not self.process_body(statement[3][1]):
                return False

        self.quadruples[goto_index].result = self.quad_counter + 1

        return True

    def process_do_while(self, statement):
        # Mark the beginning of the loop body
        loop_start = self.quad_counter + 1
        
        # Process the loop body first
        if not self.process_body(statement[1][1]):
            return False
        
        # Now process the condition
        if not self.process_expression(statement[2]):
            return False

        condition_result = self.operand_stack.pop()
        condition_type = self.type_stack.pop()

        if condition_type != 'bool':
            print(f"Error semántico: La condición debe ser de tipo bool, se encontró {condition_type}")
            return False

        # For do-while: if condition is true, jump back to loop start
        # If condition is false, continue to next instruction (exit loop)
        self.add_quadruple('GOTOF', condition_result, None, self.quad_counter + 2)
        self.add_quadruple('GOTO', None, None, loop_start)

        return True

def analyze_code(file_path):
    result, errors_by_line, input_program = parser.parse_file(file_path)

    if errors_by_line:
        parser.print_line_analysis(input_program, errors_by_line)
        return None
    
    analyzer = SemanticAnalyzer()
    if not analyzer.analyze_program(result):
        return None
    
    print("\n" + "="*50)
    print("DIRECTORIO DE FUNCIONES")
    print("="*50)
    for name, details in analyzer.function_directory.functions.items():
        print(f"\nFunción: {name}")
        print(f"Tipo de retorno: {details['return_type']}")
        print(f"Parámetros: {details['params']}")
        print(f"Cuádruplo inicial: {details['start_quad']}")
        print("\nVariables locales:")
        for var_name, var_details in details['local_vars'].scopes.get(name, {}).items():
            print(f"  {var_name}: {var_details['type']}")
    
    print("\n" + "="*50)
    print("TABLA DE SÍMBOLOS")
    print("="*50)
    for scope, symbols in analyzer.symbol_table.scopes.items():
        print(f"\nScope: {scope}")
        print("-"*30)
        print(f"{'Nombre':<15}{'Tipo':<15}")
        print("-"*30)
        for name, details in symbols.items():
            print(f"{name:<15}{details['type']:<15}")
    
    print("\n" + "="*80)
    print("LISTA DE CUÁDRUPLOS")
    print("="*80)
    print(f"{'num':<6}{'op':<15}{'argL':<15}{'argR':<15}{'res':<15}")
    print("-"*80)
    for i, quad in enumerate(analyzer.quadruples, 1):
        op = str(quad.operator) if quad.operator is not None else ''
        arg_l = str(quad.left_operand) if quad.left_operand is not None else ''
        arg_r = str(quad.right_operand) if quad.right_operand is not None else ''
        res = str(quad.result) if quad.result is not None else ''
        print(f"{i:<6}{op:<15}{arg_l:<15}{arg_r:<15}{res:<15}")
    
    return result, None

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "Tests", "prueba6.ld")
    analyze_code(file_path)