# parser_db.py
import ply.yacc as yacc
from lex_db import tokens
import common_db

def p_statement(p):
    '''statement : query
                 | create_table
                 | insert_stmt
                 | delete_stmt
                 | update_stmt
                 | drop_table'''
    p[0] = p[1]

def p_create_table(p):
    '''create_table : CREATE TABLE TCNAME LPAREN field_defs RPAREN'''
    p[0] = common_db.Node('CREATE_TABLE', [p[5]], [p[3]])

def p_field_defs(p):
    '''field_defs : field_def
                  | field_def COMMA field_defs'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# 统一类型：TCNAME TYPE（TYPE 可以是 integer 或 char(20) 等）
def p_field_def(p):
    'field_def : TCNAME TYPE'
    p[0] = (p[1], p[2])

def p_insert_stmt(p):
    '''insert_stmt : INSERT INTO TCNAME VALUES LPAREN value_list RPAREN'''
    p[0] = common_db.Node('INSERT', [p[6]], [p[3]])

def p_value_list(p):
    '''value_list : CONSTANT
                  | CONSTANT COMMA value_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_delete_stmt(p):
    '''delete_stmt : DELETE FROM TCNAME'''
    p[0] = common_db.Node('DELETE', [], [p[3]])

def p_update_stmt(p):
    '''update_stmt : UPDATE TCNAME SET TCNAME EQX CONSTANT WHERE TCNAME EQX CONSTANT'''
    p[0] = common_db.Node('UPDATE',
                          [(p[4], p[6]), (p[8], p[10])],
                          [p[2]])

def p_drop_table(p):
    '''drop_table : DROP TABLE TCNAME'''
    p[0] = common_db.Node('DROP', [], [p[3]])

def p_query_sfw(p):
    'query : SELECT sel_list FROM table_name opt_where'
    nodes = [p[2], p[4]]
    if p[5] is not None:
        nodes.append(p[5])
    p[0] = common_db.Node('SELECT', nodes)

def p_sel_list_star(p):
    'sel_list : STAR'
    p[0] = common_db.Node('FIELDLIST', [], ['*'])

def p_sel_list_names(p):
    'sel_list : TCNAME rest_fields'
    fields = [p[1]] + (p[2] if p[2] else [])
    p[0] = common_db.Node('FIELDLIST', [], fields)

def p_rest_fields(p):
    '''rest_fields : COMMA TCNAME rest_fields
                   | '''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_table_name(p):
    'table_name : TCNAME'
    p[0] = p[1]

def p_opt_where(p):
    '''opt_where : WHERE condition
                 | '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_condition(p):
    'condition : TCNAME EQX CONSTANT'
    p[0] = (p[1], p[3])

def p_error(p):
    print(f"语法错误：{p.value if p else 'EOF'}")

def set_handle():
    common_db.global_parser = yacc.yacc(start='statement')
