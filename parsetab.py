
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ASSIGN_OP BOOL COLON COMMA CONST_FLOAT CONST_INT CONST_STRING DEL_PAR_CLOSE DEL_PAR_OPEN DO ELSE END FALSE FLOAT ID IF INT LBRACE LBRACKET MAIN OP_DIV OP_MULT OP_REL OP_RESTA OP_SUMA PRINT PROGRAM RBRACE RBRACKET RETURN SEMICOLON STRING TRUE VAR VOID WHILEprograma : PROGRAM ID SEMICOLON vars_opt funcs_opt MAIN body ENDvars_opt : vars_list\n                | emptyvars_list : vars\n                 | vars_list varsvars : VAR var_decl_listfunction_list : function\n                     | function_list functionfuncs_opt : function_list\n                 | emptyfunction : type ID DEL_PAR_OPEN param_list DEL_PAR_CLOSE LBRACKET vars_opt body RBRACKET SEMICOLONparam_list : param\n                 | param_list COMMA param\n                 | emptyparam : ID COLON typetype : VOID\n            | INT\n            | FLOAT\n            | STRING\n            | BOOLvar_decl_list : var_decl\n                     | var_decl_list var_declvar_decl : id_list COLON type SEMICOLONid_list : ID\n               | id_list COMMA IDbody : LBRACE statement_list RBRACEstatement_list : statement\n                      | statement_list statement\n                      | emptystatement : assign\n                 | print_stmt\n                 | condition\n                 | cycle\n                 | function_call SEMICOLON\n                 | return_stmt\n                 | if_stmtif_stmt : IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body SEMICOLON\n               | IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body ELSE body SEMICOLONreturn_stmt : RETURN expresion SEMICOLON\n                   | RETURN SEMICOLONprint_stmt : PRINT DEL_PAR_OPEN print_arguments DEL_PAR_CLOSE SEMICOLONprint_arguments : expresion\n                       | print_arguments COMMA expresionassign : ID ASSIGN_OP expresion SEMICOLONcycle : DO body WHILE DEL_PAR_OPEN expresion DEL_PAR_CLOSE SEMICOLONcondition : IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body else_part SEMICOLONelse_part : ELSE body\n                 | emptyexp : termino\n           | exp OP_SUMA termino\n           | exp OP_RESTA terminotermino : factor\n               | termino OP_MULT factor\n               | termino OP_DIV factorfactor : DEL_PAR_OPEN expresion DEL_PAR_CLOSE\n              | OP_SUMA atomic_factor\n              | OP_RESTA atomic_factor\n              | atomic_factoratomic_factor : ID\n                     | CONST_INT\n                     | CONST_FLOAT\n                     | CONST_STRING\n                     | TRUE\n                     | FALSE\n                     | DEL_PAR_OPEN expresion DEL_PAR_CLOSEfunction_call : ID DEL_PAR_OPEN argument_list DEL_PAR_CLOSEargument_list : expresion\n                     | argument_list COMMA expresion\n                     | emptyempty :expresion : exp\n                 | exp OP_REL exp'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,36,],[0,-1,]),'ID':([2,9,14,15,16,17,18,19,21,22,28,30,32,33,37,38,39,40,41,42,43,45,46,51,56,58,59,60,61,62,63,66,69,70,72,82,91,92,93,94,95,96,98,104,106,108,110,120,127,132,134,136,],[3,24,27,-16,-17,-18,-19,-20,24,-21,-22,35,47,52,47,-27,-29,-30,-31,-32,-33,-35,-36,74,-23,-28,-34,74,74,74,74,-40,74,74,74,52,-39,74,74,74,74,74,74,-44,74,74,74,-41,-37,-46,-45,-38,]),'SEMICOLON':([3,15,16,17,18,19,34,44,51,57,65,67,68,71,73,74,75,76,77,78,79,83,97,99,105,107,111,112,113,114,115,117,122,124,126,129,130,131,133,],[4,-16,-17,-18,-19,-20,56,59,66,-26,91,-71,-49,-52,-58,-59,-60,-61,-62,-63,-64,104,-56,-57,-66,120,-72,-50,-51,-53,-54,-55,127,-65,132,-48,134,135,136,]),'VOID':([4,5,6,7,8,11,13,20,21,22,26,28,29,56,80,135,],[-70,15,-2,-3,-4,15,-7,-5,-6,-21,-8,-22,15,-23,15,-11,]),'INT':([4,5,6,7,8,11,13,20,21,22,26,28,29,56,80,135,],[-70,16,-2,-3,-4,16,-7,-5,-6,-21,-8,-22,16,-23,16,-11,]),'FLOAT':([4,5,6,7,8,11,13,20,21,22,26,28,29,56,80,135,],[-70,17,-2,-3,-4,17,-7,-5,-6,-21,-8,-22,17,-23,17,-11,]),'STRING':([4,5,6,7,8,11,13,20,21,22,26,28,29,56,80,135,],[-70,18,-2,-3,-4,18,-7,-5,-6,-21,-8,-22,18,-23,18,-11,]),'BOOL':([4,5,6,7,8,11,13,20,21,22,26,28,29,56,80,135,],[-70,19,-2,-3,-4,19,-7,-5,-6,-21,-8,-22,19,-23,19,-11,]),'MAIN':([4,5,6,7,8,10,11,12,13,20,21,22,26,28,56,135,],[-70,-70,-2,-3,-4,25,-9,-10,-7,-5,-6,-21,-8,-22,-23,-11,]),'VAR':([4,6,8,20,21,22,28,56,102,],[9,9,-4,-5,-6,-21,-22,-23,9,]),'LBRACE':([6,7,8,20,21,22,25,28,50,56,102,109,118,128,],[-2,-3,-4,-5,-6,-21,32,-22,32,-23,-70,32,32,32,]),'DEL_PAR_CLOSE':([15,16,17,18,19,33,53,54,55,61,67,68,71,73,74,75,76,77,78,79,84,85,86,87,88,89,97,99,100,101,103,111,112,113,114,115,116,117,119,121,123,124,],[-16,-17,-18,-19,-20,-70,81,-12,-14,-70,-71,-49,-52,-58,-59,-60,-61,-62,-63,-64,105,-67,-69,107,-42,109,-56,-57,117,-15,-13,-72,-50,-51,-53,-54,124,-55,-68,-43,130,-65,]),'COMMA':([15,16,17,18,19,23,24,33,35,53,54,55,61,67,68,71,73,74,75,76,77,78,79,84,85,86,87,88,97,99,101,103,111,112,113,114,115,117,119,121,124,],[-16,-17,-18,-19,-20,30,-24,-70,-25,82,-12,-14,-70,-71,-49,-52,-58,-59,-60,-61,-62,-63,-64,106,-67,-69,108,-42,-56,-57,-15,-13,-72,-50,-51,-53,-54,-55,-68,-43,-65,]),'COLON':([23,24,35,52,],[29,-24,-25,80,]),'DEL_PAR_OPEN':([27,47,48,49,51,60,61,62,63,69,70,72,90,92,93,94,95,96,98,106,108,110,],[33,61,62,63,72,72,72,72,72,98,98,72,110,72,72,72,72,72,72,72,72,72,]),'END':([31,57,],[36,-26,]),'RBRACE':([32,37,38,39,40,41,42,43,45,46,58,59,66,91,104,120,127,132,134,136,],[-70,57,-27,-29,-30,-31,-32,-33,-35,-36,-28,-34,-40,-39,-44,-41,-37,-46,-45,-38,]),'PRINT':([32,37,38,39,40,41,42,43,45,46,58,59,66,91,104,120,127,132,134,136,],[48,48,-27,-29,-30,-31,-32,-33,-35,-36,-28,-34,-40,-39,-44,-41,-37,-46,-45,-38,]),'IF':([32,37,38,39,40,41,42,43,45,46,58,59,66,91,104,120,127,132,134,136,],[49,49,-27,-29,-30,-31,-32,-33,-35,-36,-28,-34,-40,-39,-44,-41,-37,-46,-45,-38,]),'DO':([32,37,38,39,40,41,42,43,45,46,58,59,66,91,104,120,127,132,134,136,],[50,50,-27,-29,-30,-31,-32,-33,-35,-36,-28,-34,-40,-39,-44,-41,-37,-46,-45,-38,]),'RETURN':([32,37,38,39,40,41,42,43,45,46,58,59,66,91,104,120,127,132,134,136,],[51,51,-27,-29,-30,-31,-32,-33,-35,-36,-28,-34,-40,-39,-44,-41,-37,-46,-45,-38,]),'ASSIGN_OP':([47,],[60,]),'OP_SUMA':([51,60,61,62,63,67,68,71,72,73,74,75,76,77,78,79,92,93,94,95,96,97,98,99,106,108,110,111,112,113,114,115,117,124,],[69,69,69,69,69,93,-49,-52,69,-58,-59,-60,-61,-62,-63,-64,69,69,69,69,69,-56,69,-57,69,69,69,93,-50,-51,-53,-54,-55,-65,]),'OP_RESTA':([51,60,61,62,63,67,68,71,72,73,74,75,76,77,78,79,92,93,94,95,96,97,98,99,106,108,110,111,112,113,114,115,117,124,],[70,70,70,70,70,94,-49,-52,70,-58,-59,-60,-61,-62,-63,-64,70,70,70,70,70,-56,70,-57,70,70,70,94,-50,-51,-53,-54,-55,-65,]),'CONST_INT':([51,60,61,62,63,69,70,72,92,93,94,95,96,98,106,108,110,],[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,]),'CONST_FLOAT':([51,60,61,62,63,69,70,72,92,93,94,95,96,98,106,108,110,],[76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,]),'CONST_STRING':([51,60,61,62,63,69,70,72,92,93,94,95,96,98,106,108,110,],[77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,]),'TRUE':([51,60,61,62,63,69,70,72,92,93,94,95,96,98,106,108,110,],[78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,]),'FALSE':([51,60,61,62,63,69,70,72,92,93,94,95,96,98,106,108,110,],[79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,]),'WHILE':([57,64,],[-26,90,]),'ELSE':([57,122,],[-26,128,]),'RBRACKET':([57,125,],[-26,131,]),'OP_REL':([67,68,71,73,74,75,76,77,78,79,97,99,112,113,114,115,117,124,],[92,-49,-52,-58,-59,-60,-61,-62,-63,-64,-56,-57,-50,-51,-53,-54,-55,-65,]),'OP_MULT':([68,71,73,74,75,76,77,78,79,97,99,112,113,114,115,117,124,],[95,-52,-58,-59,-60,-61,-62,-63,-64,-56,-57,95,95,-53,-54,-55,-65,]),'OP_DIV':([68,71,73,74,75,76,77,78,79,97,99,112,113,114,115,117,124,],[96,-52,-58,-59,-60,-61,-62,-63,-64,-56,-57,96,96,-53,-54,-55,-65,]),'LBRACKET':([81,],[102,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'vars_opt':([4,102,],[5,118,]),'vars_list':([4,102,],[6,6,]),'empty':([4,5,32,33,61,102,122,],[7,12,39,55,86,7,129,]),'vars':([4,6,102,],[8,20,8,]),'funcs_opt':([5,],[10,]),'function_list':([5,],[11,]),'function':([5,11,],[13,26,]),'type':([5,11,29,80,],[14,14,34,101,]),'var_decl_list':([9,],[21,]),'var_decl':([9,21,],[22,28,]),'id_list':([9,21,],[23,23,]),'body':([25,50,109,118,128,],[31,64,122,125,133,]),'statement_list':([32,],[37,]),'statement':([32,37,],[38,58,]),'assign':([32,37,],[40,40,]),'print_stmt':([32,37,],[41,41,]),'condition':([32,37,],[42,42,]),'cycle':([32,37,],[43,43,]),'function_call':([32,37,],[44,44,]),'return_stmt':([32,37,],[45,45,]),'if_stmt':([32,37,],[46,46,]),'param_list':([33,],[53,]),'param':([33,82,],[54,103,]),'expresion':([51,60,61,62,63,72,98,106,108,110,],[65,83,85,88,89,100,116,119,121,123,]),'exp':([51,60,61,62,63,72,92,98,106,108,110,],[67,67,67,67,67,67,111,67,67,67,67,]),'termino':([51,60,61,62,63,72,92,93,94,98,106,108,110,],[68,68,68,68,68,68,68,112,113,68,68,68,68,]),'factor':([51,60,61,62,63,72,92,93,94,95,96,98,106,108,110,],[71,71,71,71,71,71,71,71,71,114,115,71,71,71,71,]),'atomic_factor':([51,60,61,62,63,69,70,72,92,93,94,95,96,98,106,108,110,],[73,73,73,73,73,97,99,73,73,73,73,73,73,73,73,73,73,]),'argument_list':([61,],[84,]),'print_arguments':([62,],[87,]),'else_part':([122,],[126,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> PROGRAM ID SEMICOLON vars_opt funcs_opt MAIN body END','programa',8,'p_programa','parser.py',11),
  ('vars_opt -> vars_list','vars_opt',1,'p_vars_opt','parser.py',15),
  ('vars_opt -> empty','vars_opt',1,'p_vars_opt','parser.py',16),
  ('vars_list -> vars','vars_list',1,'p_vars_list','parser.py',20),
  ('vars_list -> vars_list vars','vars_list',2,'p_vars_list','parser.py',21),
  ('vars -> VAR var_decl_list','vars',2,'p_vars','parser.py',28),
  ('function_list -> function','function_list',1,'p_function_list','parser.py',32),
  ('function_list -> function_list function','function_list',2,'p_function_list','parser.py',33),
  ('funcs_opt -> function_list','funcs_opt',1,'p_funcs_opt','parser.py',40),
  ('funcs_opt -> empty','funcs_opt',1,'p_funcs_opt','parser.py',41),
  ('function -> type ID DEL_PAR_OPEN param_list DEL_PAR_CLOSE LBRACKET vars_opt body RBRACKET SEMICOLON','function',10,'p_function','parser.py',46),
  ('param_list -> param','param_list',1,'p_param_list','parser.py',50),
  ('param_list -> param_list COMMA param','param_list',3,'p_param_list','parser.py',51),
  ('param_list -> empty','param_list',1,'p_param_list','parser.py',52),
  ('param -> ID COLON type','param',3,'p_param','parser.py',59),
  ('type -> VOID','type',1,'p_type','parser.py',63),
  ('type -> INT','type',1,'p_type','parser.py',64),
  ('type -> FLOAT','type',1,'p_type','parser.py',65),
  ('type -> STRING','type',1,'p_type','parser.py',66),
  ('type -> BOOL','type',1,'p_type','parser.py',67),
  ('var_decl_list -> var_decl','var_decl_list',1,'p_var_decl_list','parser.py',71),
  ('var_decl_list -> var_decl_list var_decl','var_decl_list',2,'p_var_decl_list','parser.py',72),
  ('var_decl -> id_list COLON type SEMICOLON','var_decl',4,'p_var_decl','parser.py',79),
  ('id_list -> ID','id_list',1,'p_id_list','parser.py',83),
  ('id_list -> id_list COMMA ID','id_list',3,'p_id_list','parser.py',84),
  ('body -> LBRACE statement_list RBRACE','body',3,'p_body','parser.py',91),
  ('statement_list -> statement','statement_list',1,'p_statement_list','parser.py',95),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','parser.py',96),
  ('statement_list -> empty','statement_list',1,'p_statement_list','parser.py',97),
  ('statement -> assign','statement',1,'p_statement','parser.py',104),
  ('statement -> print_stmt','statement',1,'p_statement','parser.py',105),
  ('statement -> condition','statement',1,'p_statement','parser.py',106),
  ('statement -> cycle','statement',1,'p_statement','parser.py',107),
  ('statement -> function_call SEMICOLON','statement',2,'p_statement','parser.py',108),
  ('statement -> return_stmt','statement',1,'p_statement','parser.py',109),
  ('statement -> if_stmt','statement',1,'p_statement','parser.py',110),
  ('if_stmt -> IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body SEMICOLON','if_stmt',6,'p_if_stmt','parser.py',114),
  ('if_stmt -> IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body ELSE body SEMICOLON','if_stmt',8,'p_if_stmt','parser.py',115),
  ('return_stmt -> RETURN expresion SEMICOLON','return_stmt',3,'p_return_stmt','parser.py',122),
  ('return_stmt -> RETURN SEMICOLON','return_stmt',2,'p_return_stmt','parser.py',123),
  ('print_stmt -> PRINT DEL_PAR_OPEN print_arguments DEL_PAR_CLOSE SEMICOLON','print_stmt',5,'p_print_stmt','parser.py',127),
  ('print_arguments -> expresion','print_arguments',1,'p_print_arguments','parser.py',131),
  ('print_arguments -> print_arguments COMMA expresion','print_arguments',3,'p_print_arguments','parser.py',132),
  ('assign -> ID ASSIGN_OP expresion SEMICOLON','assign',4,'p_assign','parser.py',139),
  ('cycle -> DO body WHILE DEL_PAR_OPEN expresion DEL_PAR_CLOSE SEMICOLON','cycle',7,'p_cycle','parser.py',144),
  ('condition -> IF DEL_PAR_OPEN expresion DEL_PAR_CLOSE body else_part SEMICOLON','condition',7,'p_condition','parser.py',149),
  ('else_part -> ELSE body','else_part',2,'p_else_part','parser.py',154),
  ('else_part -> empty','else_part',1,'p_else_part','parser.py',155),
  ('exp -> termino','exp',1,'p_exp','parser.py',159),
  ('exp -> exp OP_SUMA termino','exp',3,'p_exp','parser.py',160),
  ('exp -> exp OP_RESTA termino','exp',3,'p_exp','parser.py',161),
  ('termino -> factor','termino',1,'p_termino','parser.py',165),
  ('termino -> termino OP_MULT factor','termino',3,'p_termino','parser.py',166),
  ('termino -> termino OP_DIV factor','termino',3,'p_termino','parser.py',167),
  ('factor -> DEL_PAR_OPEN expresion DEL_PAR_CLOSE','factor',3,'p_factor','parser.py',171),
  ('factor -> OP_SUMA atomic_factor','factor',2,'p_factor','parser.py',172),
  ('factor -> OP_RESTA atomic_factor','factor',2,'p_factor','parser.py',173),
  ('factor -> atomic_factor','factor',1,'p_factor','parser.py',174),
  ('atomic_factor -> ID','atomic_factor',1,'p_atomic_factor','parser.py',183),
  ('atomic_factor -> CONST_INT','atomic_factor',1,'p_atomic_factor','parser.py',184),
  ('atomic_factor -> CONST_FLOAT','atomic_factor',1,'p_atomic_factor','parser.py',185),
  ('atomic_factor -> CONST_STRING','atomic_factor',1,'p_atomic_factor','parser.py',186),
  ('atomic_factor -> TRUE','atomic_factor',1,'p_atomic_factor','parser.py',187),
  ('atomic_factor -> FALSE','atomic_factor',1,'p_atomic_factor','parser.py',188),
  ('atomic_factor -> DEL_PAR_OPEN expresion DEL_PAR_CLOSE','atomic_factor',3,'p_atomic_factor','parser.py',189),
  ('function_call -> ID DEL_PAR_OPEN argument_list DEL_PAR_CLOSE','function_call',4,'p_function_call','parser.py',196),
  ('argument_list -> expresion','argument_list',1,'p_argument_list','parser.py',200),
  ('argument_list -> argument_list COMMA expresion','argument_list',3,'p_argument_list','parser.py',201),
  ('argument_list -> empty','argument_list',1,'p_argument_list','parser.py',202),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',209),
  ('expresion -> exp','expresion',1,'p_expresion','parser.py',224),
  ('expresion -> exp OP_REL exp','expresion',3,'p_expresion','parser.py',225),
]
