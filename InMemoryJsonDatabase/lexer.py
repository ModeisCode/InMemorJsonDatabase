import ply.lex

tokens = (
    'COMMAND',
    'PARAMETER',
    'INDEXED_KEY',
    'TO_INDEXED_KEY',
    'VALUE',
)

t_COMMAND = r'\b(ADD|NULL|VALUE|INDEX|IN|OUT|DEL|SETTINGS|ALERT|NEWGROUP|INCR|DECR|SHOW|USERNAME)\b'
t_PARAMETER = r'[a-zA-z]+'
t_VALUE = r'(\"[^\"]*\"|\d+)'
t_INDEXED_KEY = r'[a-zA-z]+:\d+'
t_TO_INDEXED_KEY = r'TO:[a-zA-z]+:\d+'

t_ignore = ' \t\n,'

def t_newline(t):
    r'\n'
    t.lineno += 1

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



lexer = ply.lex.lex()

input = """
ADD NO KEY:0
"""

def getLexedData(input_ :str):
    global lexer
    lexer.input(input_)
    cmd = 0
    parameter = 0
    to_indexed_key = 0
    count = 0
    instruction = { "COMMAND":"" , "GROUP":"" , "KEY":"" , "INDEXED_KEY":[] , "TO_INDEXED_KEY":"" , "VALUES":[] }
    errs = {"COMMAND_NOT_ENOUGH":0,"PARAMETER_NOT_ENOUGH":0 , "TO_INDEXED_KEY_NOT_ENOUGH":0}
    while True:
        count += 1
        tok = lexer.token()
        if not tok:
            break
        if tok.type == 'COMMAND':
            cmd += 1
            if count == 1:
                instruction['COMMAND'] = tok.value
        elif tok.type == 'PARAMETER':
            parameter += 1
            if count == 2 and parameter < 3:
                instruction['GROUP'] = tok.value
            if count == 3 and parameter < 3:
                instruction['KEY'] = tok.value
        elif tok.type == 'INDEXED_KEY':
            if count >= 3:
                instruction['INDEXED_KEY'].append(tok.value)
        elif tok.type == 'TO_INDEXED_KEY':
            to_indexed_key += 1
            if count >= 4:
                instruction['TO_INDEXED_KEY'] = tok.value
        if cmd >= 2 or cmd <= 0:
            errs['COMMAND_NOT_ENOUGH'] = cmd
        if parameter > 2 or parameter <= 0:
            errs['PARAMETER_NOT_ENOUGH'] = parameter
        if to_indexed_key > 1 or to_indexed_key < 1:
            errs['TO_INDEXED_KEY_NOT_ENOUGH'] = to_indexed_key           
        if tok.type == 'VALUE':
            instruction['VALUES'].append(tok.value)
        #print(tok.type, tok.value , count)
        #print(cmd)
    return instruction,errs



#print(getLexedData(input))