# 每日提醒自动化 🍎

> **完全自动化**的每日提醒系统：输入方案 → 自动创建 Apple 提醒 + Obsidian 笔记 + 仪表盘

[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)](https://www.apple.com/macos)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ 功能特点

| 功能 | 描述 |
|------|------|
| 🤖 AI 解析 | 自然语言输入，AI 自动解析生成方案 |
| ⏰ 自动提醒 | 创建 Apple 提醒事项，带时间 + 每天重复 |
| 📱 跨平台推送 | iPhone / Mac 自动同步推送通知 |
| 📝 Obsidian 集成 | 自动创建每日笔记 + 追踪仪表盘 |
| 📊 统计追踪 | Tracker 插件可视化完成情况 |

---

## 🚀 快速开始

### 方式一：命令行使用

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/daily-reminder-automation.git
cd daily-reminder-automation

# 2. 安装依赖
pip3 install pyobjc-framework-EventKit

# 3. 运行示例
python3 scripts/create_reminder.py '{
  "calendar": "每日健康",
  "reminders": [
    {"title": "🌅 晨光曝光", "time": "08:00", "notes": "拉开窗帘", "priority": 1, "repeat_daily": true}
  ]
}'
```

### 方式二：AI 助手使用

将此 Skill 放到 AI 助手的 Skills 目录下：

| AI 助手 | Skills 目录 |
|---------|------------|
| **CodeBuddy** | `Skills/Skill/03-daily-reminder-automation/` |
| **Claude Code** | `~/.claude/skills/daily-reminder-automation/` |

然后在对话中：

```
用户: 帮我设置每天低碳水提醒
      8点 晨光曝光 - 拉窗帘直视自然光
      12点 午餐顺序 - 先肉后碳水
      21点 睡前断电 - 关手机闭眼

AI: [自动解析 → 创建提醒 → 生成笔记]
```

---

## 📁 文件结构

```
daily-reminder-automation/
├── README.md                 # 本文件
├── SKILL.md                  # AI 助手 Skill 定义
├── install.sh                # 一键安装脚本
├── scripts/
│   ├── create_reminder.py    # 创建 Apple 提醒
│   ├── obsidian_updater.py   # 更新 Obsidian 笔记
│   └── automation.py         # 完整自动化流程
└── examples/
    └── config.json           # 示例配置
```

---

## 📝 使用示例

### 输入格式

```
每天 [主题]：
[时间] [任务] - [说明]
...

监控：[监控项]
```

### 示例：生化重构方案

```yaml
每天生化重构：
  08:00 视网膜曝光 - 拉窗帘直视自然光 5-10 分钟
  10:30 电解质防御 - 心慌时盐温水，绝对禁食
  11:15 液压缓冲预热 - 喝半杯温热海盐水
  11:30 重装填火力覆盖 - 午餐肉菜打底+补剂
  20:00 物理封关 - 晚餐后立刻刷牙离席
  23:00 强制断电重置 - 吞镁+降温+扔手机

监控：晨光、断食、顺序、补剂、封关、睡眠
```

---

## ⚙️ 配置说明

### 提醒参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `title` | string | 提醒标题 |
| `time` | string | 提醒时间 (HH:MM) |
| `notes` | string | 备注 |
| `priority` | int | 优先级 (1=高, 5=中, 9=低) |
| `repeat_daily` | bool | 是否每天重复 |

### 追踪参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 追踪项名称 |
| `tag` | string | Obsidian 标签 |

---

## 🔧 依赖

- **macOS** (EventKit 仅限 macOS)
- **Python 3.8+**
- **pyobjc-framework-EventKit**

```bash
pip3 install pyobjc-framework-EventKit
```

---

## 🔐 权限

首次运行时，macOS 会请求以下权限：

- **提醒事项**：创建和管理提醒
- **终端**：执行脚本

请在「系统设置 → 隐私与安全性」中授权。

---

## 📱 同步

提醒创建后会自动同步到：

- **iPhone**：提醒事项 App（需登录同一 Apple ID）
- **Mac**：提醒事项 App
- **Apple Watch**：提醒事项 Complication

---

## 🤝 适配的 AI 助手

| AI 助手 | 支持状态 | 使用方式 |
|---------|---------|---------|
| **CodeBuddy** | ✅ 完全支持 | 放入 Skills 目录 |
| **Claude Code** | ✅ 完全支持 | 放入 skills 目录 |
| **Cursor** | ✅ 完全支持 | 放入 .cursor/skills/ |
| **命令行** | ✅ 完全支持 | 直接运行脚本 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License