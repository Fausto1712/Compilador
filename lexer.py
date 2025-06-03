import ply.lex as lex

errors_by_line = {}

reserved = {
    'while': 'WHILE',
    'program': 'PROGRAM',
    'var': 'VAR',
    'void': 'VOID',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'do': 'DO',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'main': 'MAIN',
    'end': 'END',
    'print': 'PRINT',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE'
}

tokens = [
    'ID',
    'CONST_INT', 'CONST_FLOAT', 'CONST_STRING',
    'SEMICOLON', 'COLON', 'COMMA', 'ASSIGN_OP',
    'OP_SUMA', 'OP_RESTA', 'OP_MULT', 'OP_DIV',
    'OP_REL',
    'DEL_PAR_OPEN', 'DEL_PAR_CLOSE',
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET'
] + list(reserved.values())

t_SEMICOLON      = r';'
t_COLON          = r':'
t_COMMA          = r','
t_ASSIGN_OP      = r'='
t_OP_SUMA        = r'\+'
t_OP_RESTA       = r'-'
t_OP_MULT        = r'\*'
t_OP_DIV         = r'/'
t_OP_REL         = r'>=|<=|==|!=|>|<'
t_DEL_PAR_OPEN   = r'\('
t_DEL_PAR_CLOSE  = r'\)'
t_LBRACE         = r'\{'
t_RBRACE         = r'\}'
t_LBRACKET       = r'\['
t_RBRACKET       = r'\]'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CONST_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CONST_STRING(t):
    r'"[^"\\]*"'
    return t

def t_comment(t):
    r'\#.*'
    pass

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    line = t.lexer.lineno
    if line not in errors_by_line:
        errors_by_line[line] = []
    errors_by_line[line].append(f"Lexical error: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()