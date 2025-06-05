# query_plan_db.py
import common_db
import os

def construct_logical_tree():
    # 将解析得到的语法树直接作为逻辑执行树
    common_db.global_logical_tree = common_db.global_syn_tree

def execute_logical_tree():
    tree = common_db.global_logical_tree
    if tree is None:
        print("无逻辑计划树，无法执行！")
        return

    # CREATE TABLE
    if tree.value == "CREATE_TABLE":
        table_name = tree.var[0]
        fields = tree.children[0]
        with open(f"{table_name}.dat", "w", encoding="utf-8") as f:
            # 写入列名和类型行
            f.write(",".join([col for col, _ in fields]) + "\n")
            f.write(",".join([typ for _, typ in fields]) + "\n")
        print(f"表 {table_name} 创建成功！")
        return

    # INSERT
    if tree.value == "INSERT":
        table_name = tree.var[0]
        values = tree.children[0]
        with open(f"{table_name}.dat", "a", encoding="utf-8") as f:
            f.write(",".join([v.strip("'") for v in values]) + "\n")
        print("插入成功！")
        return

    # DELETE (清空表内容)
    if tree.value == "DELETE":
        table_name = tree.var[0]
        with open(f"{table_name}.dat", "r+", encoding="utf-8") as f:
            header = f.readline()
            types = f.readline()
            f.seek(0)
            f.write(header)
            f.write(types)
            f.truncate()
        print(f"表 {table_name} 已清空。")
        return

    # UPDATE
    if tree.value == "UPDATE":
        table_name = tree.var[0]
        (set_col, set_val), (where_col, where_val) = tree.children
        with open(f"{table_name}.dat", "r", encoding="utf-8") as f:
            lines = f.readlines()
        header = lines[0].strip().split(",")
        typeline = lines[1]
        updated = []
        for line in lines[2:]:
            row = line.strip().split(",")
            if row[header.index(where_col)] == where_val.strip("'"):
                row[header.index(set_col)] = set_val.strip("'")
            updated.append(row)
        with open(f"{table_name}.dat", "w", encoding="utf-8") as f:
            f.write(",".join(header) + "\n")
            f.write(typeline)
            for row in updated:
                f.write(",".join(row) + "\n")
        print("更新成功！")
        return

    # DROP TABLE
    if tree.value == "DROP":
        table_name = tree.var[0]
        try:
            os.remove(f"{table_name}.dat")
            print(f"表 {table_name} 已删除。")
        except:
            print(f"删除失败或文件不存在：{table_name}.dat")
        return

    # SELECT
    if tree.value == "SELECT":
        fieldlist_node = tree.children[0]
        table_name = tree.children[1]
        condition = tree.children[2] if len(tree.children) > 2 else None

        # 确保 table_name 为字符串
        if not isinstance(table_name, str):
            table_name = table_name.var if hasattr(table_name, 'var') else str(table_name)

        try:
            with open(f"{table_name}.dat", "r", encoding="utf-8") as f:
                header = f.readline().strip().split(",")
                f.readline()  # 跳过类型行
                records = [line.strip().split(",") for line in f if line.strip()]
                # 计算输出列索引
                if fieldlist_node.var == ['*']:
                    idxs = list(range(len(header)))
                else:
                    idxs = [header.index(col) for col in fieldlist_node.var]
                # 遍历输出
                for rec in records:
                    if condition:
                        col, val = condition
                        if rec[header.index(col)] != val.strip("'"):
                            continue
                    print(",".join(rec[i] for i in idxs))
        except FileNotFoundError:
            print(f"数据文件 {table_name}.dat 未找到！")
        except Exception as e:
            print(f"查询出错：{e}")
        return

    # 未识别的操作
    print(f"未知操作类型：{tree.value}")
