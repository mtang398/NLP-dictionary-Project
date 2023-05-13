# 定义一个空列表，用于保存学生的姓名
students = []

# 从键盘输入学生的姓名，并保存到列表中
while True:
    name = input("请输入学生的姓名（按回车键结束输入）：")
    if not name:  # 如果输入为空字符串，则退出循环
        break
    students.append(name)

# 从键盘输入要检索的学生姓名
search_name = input("请输入要检索的学生姓名：")

# 检索学生姓名是否已保存在列表中
if search_name in students:
    print("学生 %s 已保存在列表中。" % search_name)
else:
    print("学生 %s 未保存在列表中。" % search_name)
