# item.py
# ================================================
# 物品模块（独立、可复用）
# ================================================

class Item:
    """物品类（可拾取/描述）"""
    def __init__(self, name: str, description: str, takeable: bool = True):
        self.name = name          # 原样保存（支持中文）
        self.description = description
        self.takeable = takeable