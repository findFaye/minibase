# main_db.py
import lex_db
import parser_db
import query_plan_db
import common_db

def run_sql():
    sql = input('请输入SQL语句：')
    lex_db.set_lex_handle()
    parser_db.set_handle()
    try:
        common_db.global_syn_tree = common_db.global_parser.parse(sql.strip(), lexer=common_db.global_lexer)
        if not common_db.global_syn_tree:
            print("语法树构建失败")
            return
        print("------ 语法树 ------")
        common_db.show(common_db.global_syn_tree)
        print("------ 执行结果 ------")
        query_plan_db.construct_logical_tree()
        query_plan_db.execute_logical_tree()
    except Exception as e:
        print(f"执行失败：{e}")

if __name__ == '__main__':
    while True:
        print("菜单：")
        print("1. 执行SQL语句")
        print("0. 退出")
        choice = input("请选择：")
        if choice == "1":
            run_sql()
        elif choice == "0":
            print("退出。")
            break
