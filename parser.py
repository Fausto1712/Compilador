import ply.yacc as yacc
import lexer
import os

tokens = lexer.tokens
errors_by_line = {}

tokens = lexer.tokens

def p_programa(p):
    """programa : PROGRAM ID SEMICOLON vars_opt funcs_opt MAIN body END"""
    p[0] = ('programa', p[2], p[4], (p[5], ('main', p[7])))

def p_vars_opt(p):
    """vars_opt : vars_list
                | empty"""
    p[0] = p[1]

def p_vars_list(p):
    """vars_list : vars
                 | vars_list vars"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('vars', p[1][1] + p[2][1])

def p_vars(p):
    """vars : VAR var_decl_list"""
    p[0] = ('vars', p[2])

def p_function_list(p):
    """function_list : function
                     | function_list function"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_funcs_opt(p):
    """funcs_opt : function_list
                 | empty"""
    p[0] = p[1]

def p_function(p):
    """function : type ID DEL_PAR_OPEN param_list DEL_PAR_CLOSE LBRACKET vars_opt body RBRACKET SEMICOLON"""
    p[0] = ('function_definition', p[2], p[4], p[1], (p[7], p[8]))

def p_param_list(p):
    """param_list : param
                 | param_list COMMA param
                 | empty"""
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    """param : ID COLON type"""
    p[0] = (p[1], p[3])

def p_type(p):
    """type : VOID
            | INT
            | FLOAT
            | STRING
            | BOOL"""
    p[0] = p[1]

def p_atomic_factor(p):
    """atomic_factor : ID
                     | CONST_INT
                     | CONST_FLOAT
                     | CONST_STRING
                     | TRUE
                     | FALSE
                     | DEL_PAR_OPEN expresion DEL_PAR_CLOSE"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_var_decl_list(p):
    """var_decl_list : var_decl
                     | var_decl_list var_decl"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_var_decl(p):
    """var_decl : id_list COLON type SEMICOLON"""
    p[0] = ('var_decl', [(p[1], p[3])])

def p_id_list(p):
    """id_list : ID
               | id_list COMMA ID"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_body(p):
    """body : LBRACE statement_list RBRACE"""
    p[0] = ('body', p[2])

def p_statement_list(p):
    """statement_list : statement
                      | statement_list statement
                      | empty"""
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    """statement : assign
                 | print_stmt
                 | condition
                 | cycle
                 | function_call SEMICOLON
                 | return_stmt
                 | if_stmt"""
    p[0] = p[1]

def p_if_stmt(p):
    """if_stmt : IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body SEMICOLON
               | IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body ELSE body SEMICOLON"""
    if len(p) == 7:
        p[0] = ('if_stmt', p[3], p[5])
    else:
        p[0] = ('if_else_stmt', p[3], p[5], p[7])

def p_return_stmt(p):
    """return_stmt : RETURN expresion SEMICOLON
                   | RETURN SEMICOLON"""
    p[0] = ('return', None) if len(p) == 3 else ('return', p[2])

def p_print_stmt(p):
    """print_stmt : PRINT DEL_PAR_OPEN print_arguments DEL_PAR_CLOSE SEMICOLON"""
    p[0] = ('print', p[3])

def p_print_arguments(p):
    """print_arguments : expresion
                       | print_arguments COMMA expresion"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_assign(p):
    """assign : ID ASSIGN_OP expresion SEMICOLON"""
    p[0] = ('assign', p[1], p[3])

def p_cycle(p):
    """cycle : DO body WHILE DEL_PAR_OPEN expresion DEL_PAR_CLOSE SEMICOLON"""
    p[0] = ('do_while', p[2], p[5])

def p_condition(p):
    """condition : IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body else_part SEMICOLON"""
    p[0] = ('if', p[3], p[5], p[6])

def p_else_part(p):
    """else_part : ELSE body
                 | empty"""
    p[0] = p[2] if p[1] else None

def p_exp(p):
    """exp : termino
           | exp OP_SUMA termino
           | exp OP_RESTA termino"""
    p[0] = p[1] if len(p) == 2 else ('exp', p[2], p[1], p[3])

def p_termino(p):
    """termino : factor
               | termino OP_MULT factor
               | termino OP_DIV factor"""
    p[0] = p[1] if len(p) == 2 else ('termino', p[2], p[1], p[3])

def p_factor(p):
    """factor : DEL_PAR_OPEN expresion DEL_PAR_CLOSE
              | OP_SUMA atomic_factor
              | OP_RESTA atomic_factor
              | atomic_factor"""
    if len(p) == 4:
        p[0] = ('factor_paren', p[2])
    elif len(p) == 3:
        p[0] = ('factor', p[1], p[2])
    else:
        p[0] = ('factor', p[1])

def p_function_call(p):
    """function_call : ID DEL_PAR_OPEN argument_list DEL_PAR_CLOSE"""
    p[0] = ('function_call', p[1], p[3])

def p_argument_list(p):
    """argument_list : expresion
                     | argument_list COMMA expresion
                     | empty"""
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_empty(p):
    """empty :"""
    p[0] = None

def p_error(p):
    if p:
        line = p.lineno if hasattr(p, 'lineno') else 0
        if line not in errors_by_line:
            errors_by_line[line] = []
        errors_by_line[line].append(f"Error de sintaxis en '{p.value}'")
    else:
        if 0 not in errors_by_line:
            errors_by_line[0] = []
        errors_by_line[0].append("Error de sintaxis al final del archivo")

def p_expresion(p):
    """expresion : exp
                 | exp OP_REL exp"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('expresion', p[2], p[1], p[3])

parser = yacc.yacc()

def analyze_line_by_line(input_text):
    global errors_by_line
    errors_by_line = {}
    result = parser.parse(input_text, lexer=lexer.lexer)
    return result, errors_by_line, input_text

def print_line_analysis(input_text, errors_by_line):
    lines = input_text.split('\n')
    print("\n" + "="*60)
    print("Analisis por linea")
    print("="*60)
    for i, line in enumerate(lines, 1):
        line_errors = errors_by_line.get(i, [])
        if line.strip() == '':
            continue
        print(f"\nLine {i}: {line}")
        if line_errors:
            print("  ERRORES:")
            for error in line_errors:
                print(f"  - {error}")
        else:
            print("  OK")

def parse_file(file_path):
    try:
        with open(file_path, 'r') as f:
            input_program = f.read()
    except FileNotFoundError:
        print(f"Archivo {file_path} no encontrado.")
        return None, None, None

    result, errors_by_line, input_program = analyze_line_by_line(input_program)
    return result, errors_by_line, input_program

def main():
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "Tests", "prueba5.ld")
    result, errors_by_line, input_program = parse_file(file_path)
    print(result)
    print_line_analysis(input_program, errors_by_line)

if __name__ == "__main__":
    main()