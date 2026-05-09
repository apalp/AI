facts = [
    ("马修", "主演", "星际穿越"),
    ("星际穿越", "类型", "科幻"),
    ("汤姆", "主演", "碟中谍"),
    ("碟中谍", "类型", "动作"),
]

# 候选规则条件：「X 主演 Y，且 Y 类型是科幻」
# 问：这个条件"覆盖"谁？= 把谁代入 X，条件能成立？

def is_covered(x, facts):
    # 第一步：找 X 主演的电影
    movies = [obj for s, r, obj in facts if s == x and r == "主演"]
    # 第二步：看这些电影里有没有科幻
    for movie in movies:
        genres = [obj for s, r, obj in facts if s == movie and r == "类型"]
        if "科幻" in genres:
            return True  # 条件成立 → X 被"覆盖"
    return False          # 条件不成立 → X 未被"覆盖"

print(is_covered("马修", facts))  # True  ← 马修被覆盖
print(is_covered("汤姆", facts))  # False ← 汤姆未被覆盖
