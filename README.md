# OurTeam-Project2026

这是一个基于Python的文字冒险游戏项目，实现了完整的游戏逻辑和API接口。

## 团队成员
PO：李东毅

SM：张智霖

DT：周文杰

## 功能特性

- 文字冒险游戏核心逻辑
- 房间探索与导航
- 物品收集与使用
- 玩家状态管理
- API接口支持
- 交易系统

## 文件结构

```
.
├── api.py         # API路由和接口定义
├── game.py        # 游戏引擎和核心逻辑
├── player.py      # 玩家类定义
├── room.py        # 房间类定义
├── item.py        # 物品类定义
├── enemy.py       # 敌人类定义
├── npc.py         # NPC类定义
├── main.py        # 游戏入口
├── tests/         # 单元测试
├── htmlcov/       # 代码覆盖率报告
└── requirements.txt # 依赖包
```

## 快速开始

安装依赖：

```bash
pip install -r requirements.txt
```

运行游戏：

```bash
python main.py
```

运行API服务：

```bash
uvicorn api:app --reload
```

运行测试：

```bash
pytest tests/
```

## API接口

- `POST /player/{player_id}/create` - 创建玩家
- `GET /player/{player_id}` - 获取玩家状态
- `POST /player/{player_id}/move` - 移动玩家
- `POST /actions/trade` - 与NPC交易