import time
import sys

class log(object):
    # 优化格式化化版本
    # 输出日志的类
    # 显示格式: \033[显示方式;前景色;背景色m

    # 彩色输出
    RED = '\033[31m'  # 红色
    GREEN = '\033[32m'  # 绿色
    YELLOW = '\033[33m'  # 黄色
    # BLUE = '\033[34m'  # 蓝色
    # FUCHSIA = '\033[35m'  # 紫红色
    # CYAN = '\033[36m'  # 青蓝色
    # WHITE = '\033[37m'  # 白色
    RESET = '\033[0m'  # 终端默认颜色

    # 普通输出
    # RED = ''
    # GREEN = ''
    # YELLOW = ''
    # RESET = ''

    def color_str(self, color, s):
        print(time.strftime('\n[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())), end='')
        print('{}{}{}'.format(getattr(self, color), s, self.RESET))
        sys.stdout.flush()
        # with open("log.txt", 'a', encoding='utf-8')as fn:
        #     fn.write(time.strftime('\n[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())) + s)

    def error(self, s):
        self.color_str('RED',str(s))

    def info(self, s):
        self.color_str("GREEN",str(s))

    def warn(self, s):
        self.color_str("YELLOW",str(s))



l = log()
