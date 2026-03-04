---
name: nb2-gen
description: Nano Banana 2 图片生成/编辑 Skill。基于 AJI AI API 调用 Gemini 3.1 Flash Image 模型，支持二次元转真人、图片编辑、多图合成。
homepage: https://ai.ajiai.top
metadata:
  clawdbot:
    emoji: 🍌
    requires:
      bins: [python3, pip3]
---

# NB2 Gen

Nano Banana 2 图片生成工具，基于 AJI AI API。

## 配置

**必须设置 API Key：**

```bash
export NB2_API_KEY="sk-你的AJI AI Key"
```

可选配置：
```bash
export NB2_API_URL="https://ai.ajiai.top/v1/chat/completions"  # API 地址
export NB2_MODEL="AJbanana3-4k"                                 # 模型名
```

**获取 AJI AI Key：**
- 访问 https://ai.ajiai.top
- 注册并充值
- 在控制台获取 API Key

## 用法

### 1. 文生图

```bash
python3 ~/.openclaw/workspace/skills/nb2-gen/scripts/generate.py "一个穿女仆装的coser站在樱花树下" output.jpg
```

参数：
- `--aspect 2:3` - 宽高比（默认 2:3）
- `--size 4K` - 输出尺寸（默认 4K，可选 1K/2K/4K）
- `--temp 0.8` - temperature（默认 0.8）

### 2. 图片编辑（二次元转真人）

```bash
python3 ~/.openclaw/workspace/skills/nb2-gen/scripts/edit.py input.jpg "把这张图变成真人coser" output.jpg
```

### 3. 多图合成

```bash
python3 ~/.openclaw/workspace/skills/nb2-gen/scripts/compose.py "图1的人摆图2的姿势" output.jpg img1.jpg img2.jpg
```

### 4. 多轮对话迭代

```bash
python3 ~/.openclaw/workspace/skills/nb2-gen/scripts/chat.py
```

## 提示词技巧

- **二次元转真人最佳提示词**: `"把这张图变成真人coser"` — 一句话比长prompt效果更好
- **双图局部编辑**: 图片在前+一句话指令，不写约束列表
- **temperature**: 0.8 够用，1.0 有时会跑偏
- **不要裁剪原图**: 直接用原图喂模型

## 模型说明

- **AJbanana3-4k**: 4K 输出，质量接近 Pro，速度比 Pro 快
- **gemini-3.1-flash-image-preview**: Nano Banana 2，$0.03/张

## 依赖

```bash
pip3 install requests
```
