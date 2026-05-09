import math

# ─── 数据 ────────────────────────────────────────────
# 关键：反例也有「主演→类型」路径，但终点是「动作」不是「科幻」
# 所以规则链末端需要「值 == 科幻」才算覆盖，不能只看能不能走通

facts = [
    ("马修", "主演", "星际穿越"),
    ("马修", "主演", "接触"),
    ("李安", "主演", "少年派"),
    ("汤姆", "主演", "碟中谍"),
    ("汤姆", "主演", "壮志凌云"),
    ("星际穿越", "类型", "科幻"),
    ("接触",     "类型", "科幻"),
    ("少年派",   "类型", "科幻"),
    ("碟中谍",   "类型", "动作"),
    ("壮志凌云", "类型", "动作"),
]
facts_ext = facts + [
    ("斯嘉丽", "主演", "复仇者联盟"),
    ("复仇者联盟", "类型", "科幻"),
]

positives = {"马修", "李安"}
negatives = {"汤姆"}

# ─── FOIL 工具 ───────────────────────────────────────
def log2(x):
    return math.log2(x) if x > 0 else -math.inf

def foil_gain(p, n, pp, np_):
    if pp == 0:
        return -math.inf
    return pp * (log2(pp / (pp + np_)) - log2(p / (p + n)))

def extend(bindings, relation, target_value, facts):
    """
    从绑定 (X, cur) 延伸一步：
    - 若 target_value 不为 None：只保留终点等于 target_value 的绑定
    - 若 target_value 为 None：保留所有可延伸的绑定
    """
    result = set()
    for (x, cur) in bindings:
        for (s, r, o) in facts:
            if s == cur and r == relation:
                if target_value is None or o == target_value:
                    result.add((x, o))
    return result

def roots(bindings):
    return {x for x, _ in bindings}

# ─── FOIL 主函数 ─────────────────────────────────────
def foil(positives, negatives, facts):
    all_rels   = list({r for _, r, _ in facts})
    all_values = list({o for _, _, o in facts})  # 所有可能的终点值

    pos_b = {(e, e) for e in positives}
    neg_b = {(e, e) for e in negatives}
    chain = []   # [(relation, target_value_or_None)]

    print("=" * 58)
    print("目标：学习「X 偏好科幻」")
    print(f"正例={positives}  反例={negatives}")
    print("=" * 58)

    for depth in range(1, 5):
        p = len(roots(pos_b))
        n = len(roots(neg_b))
        if p == 0:
            break

        print(f"\n第 {depth} 轮 — 尝试各种「关系 [→ 固定值]」组合")

        best = {"gain": -math.inf, "rel": None, "val": None,
                "pos_b": set(), "neg_b": set()}

        # 候选：关系 + 不限值（中间跳）/ 关系 + 固定终点值（末端锁定）
        candidates = [(rel, None) for rel in all_rels]
        candidates += [(rel, val) for rel in all_rels for val in all_values]

        for rel, val in candidates:
            new_pos = extend(pos_b, rel, val, facts)
            new_neg = extend(neg_b, rel, val, facts)
            pp  = len(roots(new_pos))
            np_ = len(roots(new_neg))
            gain = foil_gain(p, n, pp, np_)
            label = f"[{rel}→{val}]" if val else f"[{rel}]"
            if gain > -math.inf:
                marker = "  ← 最佳" if gain > best["gain"] else ""
                print(f"  {label}: 正={roots(new_pos)} 反={roots(new_neg)}"
                      f"  Gain={gain:.3f}{marker}")
            if gain > best["gain"]:
                best = {"gain": gain, "rel": rel, "val": val,
                        "pos_b": new_pos, "neg_b": new_neg}

        if best["rel"] is None or best["gain"] == -math.inf:
            print("  无可用条件，停止。")
            break

        chain.append((best["rel"], best["val"]))
        pos_b = best["pos_b"]
        neg_b = best["neg_b"]
        label = f"{best['rel']}→{best['val']}" if best["val"] else best["rel"]
        print(f"\n  → 选「{label}」 Gain={best['gain']:.3f}")
        print(f"  规则链: {' ∧ '.join(f'[{r}→{v}]' if v else f'[{r}]' for r,v in chain)}")

        if not roots(neg_b):
            print(f"  反例已排除！规则完成。")
            break

    print("\n" + "=" * 58)
    if chain:
        desc = " 且 ".join(
            f"X经{r}到达\"{v}\"" if v else f"X经{r}到某节点"
            for r, v in chain)
        print(f"规则：{desc} → X 偏好科幻\n")

        print("预测：")
        for entity in ["马修", "汤姆", "李安", "斯嘉丽"]:
            b = {(entity, entity)}
            for rel, val in chain:
                b = extend(b, rel, val, facts_ext)
            hit = bool(roots(b))
            print(f"  {entity}: {'偏好科幻 ✓' if hit else '不偏好科幻 ✗'}")

foil(positives, negatives, facts)
