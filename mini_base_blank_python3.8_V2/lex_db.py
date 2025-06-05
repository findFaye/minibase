# lex_db.py
import ply.lex as lex
import common_db
import re

tokens = (
    'SELECT','FROM','WHERE',
    'CREATE','TABLE','INSERT','INTO','VALUES',
    'DELETE','UPDATE','SET','DROP',
    'LPAREN','RPAREN','COMMA','EQX','STAR',
    'CONSTANT','TYPE','TCNAME'
)

# —— 关键字 （忽略大小写）
def t_CREATE(t): r'create'; return t
def t_TABLE(t):  r'table';  return t
def t_INSERT(t): r'insert'; return t
def t_INTO(t):   r'into';   return t
def t_VALUES(t): r'values'; return t
def t_DELETE(t): r'delete'; return t
def t_UPDATE(t): r'update'; return t
def t_SET(t):    r'set';    return t
def t_DROP(t):   r'drop';   return t
def t_SELECT(t): r'select'; return t
def t_FROM(t):   r'from';   return t
def t_WHERE(t):  r'where';  return t

# —— 符号
def t_LPAREN(t): r'\('; return t
def t_RPAREN(t): r'\)'; return t
def t_COMMA(t):   r',';  return t
def t_EQX(t):     r'=';  return t
def t_STAR(t):    r'\*'; return t

# —— 常量：数字 或 '文本'
def t_CONSTANT(t):
    r"\d+|'[^']*'"
    return t

# —— 类型：只匹配 char 或 integer，后面可跟 (数字)
def t_TYPE(t):
    r"(?:char|integer)(?:\s*\(\s*\d+\s*\))?"
    return t

# —— 标识符：表名、列名
def t_TCNAME(t):
    r'[A-Za-z_]\w*'
    return t

# —— 忽略空白（包括换行）
t_ignore = ' \t\r\n'

# —— 忽略分号
def t_ignore_SEMICOLON(t):
    r';'
    pass

# —— 错误处理
def t_error(t):
    print(f"非法字符 '{t.value[0]}'")
    t.lexer.skip(1)

# —— 词法分析器初始化
def set_lex_handle():
    common_db.global_lexer = lex.lex(reflags=re.IGNORECASE)

# —— 词法测试（可临时保留）
if __name__ == "__main__":
    lexer = lex.lex(reflags=re.IGNORECASE)
    test_sql = "create table courses(c_id char(20), title char(20), credit integer)"
    print("测试输入:", test_sql)
    lexer.input(test_sql)
    for tok in lexer:
        print(tok)
