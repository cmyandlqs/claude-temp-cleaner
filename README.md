# Claude Temp Cleaner

简洁快速的 Windows 桌面工具，用于扫描并清理 Claude 生成的 `tmpclaude-*` 临时文件/目录。

A clean and fast Windows desktop tool to scan and remove Claude-generated `tmpclaude-*` temp files/directories.

## 特性 / Features
- 递归扫描指定目录，匹配 `tmpclaude-*`
- 预览结果后再确认删除（安全）
- 清晰列表与统计信息
- mac 风格简洁 UI（PySide6）

## 环境要求 / Requirements
- Windows 10/11
- Python 3.10+

## 安装 / Installation
建议使用虚拟环境：

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 运行 / Run
```powershell
python src\app.py
```

## 测试 / Tests
```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## 使用说明 / Usage
1) 启动应用
2) 选择目标文件夹
3) 查看扫描结果
4) 确认后清理

## 备注 / Notes
- 默认仅匹配 `tmpclaude-` 前缀
- 不排除任何子目录
