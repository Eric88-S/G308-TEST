"""
math_generator.py — 随机算式生成器
用于在设备A（显示端）生成白底 Times New Roman 显示的计算题。
只生成整数结果、无负数的四则混合运算。
"""

import random
from sympy import simplify


def generate_problem():
    """
    随机生成一个两位数以内的四则混合运算表达式。
    保证结果为正整数。
    返回字符串，如 "12×4-132÷3"
    """
    ops_display = ['+', '-', '×', '÷']
    ops_py = {'+': '+', '-': '-', '×': '*', '÷': '/'}

    # 最多尝试 50 次，确保生成有效表达式
    for _ in range(50):
        # 随机 3 或 4 个操作数
        num_count = random.choice([3, 4])
        nums = [random.randint(10, 99)]  # 第一个两位数，造数，闭区间

        for i in range(num_count - 1):
            op = random.choice(ops_display)#挑数
            prev = nums[i]

            if op == '+':
                nxt = random.randint(1, 99)
            elif op == '-':
                nxt = random.randint(1, max(1, prev))
            elif op == '×':
                nxt = random.randint(1, 9)
            elif op == '÷':
                factors = [f for f in range(2, prev + 1) if prev % f == 0]
                nxt = random.choice(factors) if factors else 1
            nums.append(nxt)

        # 组装表达式
        expr_parts = [str(nums[0])]
        for i in range(num_count - 1):
            expr_parts.append(ops_display[random.randint(0, 3)])
            expr_parts.append(str(nums[i + 1]))

        expr = ''.join(expr_parts)

        # 用 SymPy 验证结果
        py_expr = expr.replace('×', '*').replace('÷', '/')
        try:
            val = simplify(py_expr)
            if val.is_Integer and val > 0:
                return expr
        except Exception:
            continue

    # 兜底：简单加法
    return f'{random.randint(10, 99)}+{random.randint(1, 99)}'
