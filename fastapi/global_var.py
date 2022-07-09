# 调用全局变量  实现两个py文件之间的数据传递

def _init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    # 定义一个全局变量
    _global_dict[key] = value

"""
get_value有时会出现在另一个py文件读取失败的问题
尝试在写入value地方 直接在下一行使用get_value  
运行程序后再将其删掉  另一个py文件可以正常读取
"""
def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        print('读取' + key + '失败\r\n')
