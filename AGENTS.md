# 项目级 AGENTS.md

## 项目架构概述

本项目是一个基于Python的文本冒险游戏，采用模块化架构设计，结合FastAPI构建API接口。整体架构为模块化单体应用（Modular Monolith），分为游戏逻辑层、API接口层和数据模型层。

## 目录结构说明

```
.
├── api.py          # API路由定义（FastAPI）
├── game.py         # 游戏核心逻辑与引擎
├── player.py       # 玩家实体与状态管理
├── room.py         # 房间管理与连接
├── item.py         # 物品系统定义
├── enemy.py        # 敌人类定义
├── npc.py          # 非玩家角色定义
├── main.py         # 应用入口
├── tests/          # 单元测试文件
└── requirements.txt # 依赖包管理
```

## 核心模块职责

- **api.py**: 提供RESTful API接口，处理HTTP请求和响应，实现玩家管理、移动和交易功能
- **game.py**: 包含游戏引擎[GameEngine](file:///mnt/data/NCU/third_2/Software%20Engineering/OurTeam-Project2026/game.py#L139-L249)和游戏主控类，处理核心业务逻辑
- **player.py**: 定义玩家实体，管理玩家状态（健康值、背包、位置等）和行为
- **room.py**: 定义房间实体，管理房间连接关系和内部物品、NPC
- **item.py**: 定义各类物品（基础物品、武器、消耗品、可交易物品）
- **npc.py**: 定义非玩家角色，处理交易等功能
- **enemy.py**: 定义敌人实体，处理战斗逻辑

## 编码规范约束

1. 使用Python 3.8+语法，遵循PEP 8代码风格
2. 所有函数和类必须包含docstrings文档字符串
3. 变量命名使用snake_case，类名使用PascalCase
4. 导入顺序：标准库→第三方库→项目内部模块，每组之间空一行
5. 保持函数单一职责，长度不超过50行
6. 所有API端点必须使用Pydantic模型进行数据验证

## 禁止操作清单

1. 不得直接修改全局变量或共享状态，应通过类方法操作
2. 不得在模块级别执行有副作用的操作
3. 不得绕过API层直接操作游戏状态
4. 不得在游戏逻辑中硬编码业务规则，应通过配置或参数传递
5. 不得在[GameEngine](file:///mnt/data/NCU/third_2/Software%20Engineering/OurTeam-Project2026/game.py#L139-L249)外部直接访问玩家私有属性
6. 不得引入循环依赖，保持清晰的依赖方向：api → game/player/room → item