import os

def generate_tree_html(root_dir, current_dir='.'):
    """递归生成目录树的 HTML（<ul> + <details>）"""
    # 获取当前目录下的所有条目（文件和子目录）
    entries = sorted(os.listdir(current_dir))
    dirs = []
    files = []
    
    for entry in entries:
        full_path = os.path.join(current_dir, entry)
        # 跳过隐藏目录（如 .git, .github）和隐藏文件
        if entry.startswith('.'):
            continue
        if os.path.isdir(full_path):
            dirs.append(entry)
        elif entry.endswith('.html') and entry != 'index.html':
            # 只收集 .html 文件，排除根目录的 index.html
            files.append(entry)
    
    # 如果没有文件和目录，返回空
    if not dirs and not files:
        return ''
    
    html = '<ul class="file-tree">\n'
    
    # 先处理子目录（带 details/summary）
    for d in dirs:
        sub_path = os.path.join(current_dir, d)
        # 递归生成子目录内容
        sub_content = generate_tree_html(root_dir, sub_path)
        # 如果子目录内没有东西，就不显示
        if sub_content:
            html += f'''  <li class="folder">
    <details>
      <summary>📁 {d}</summary>
      {sub_content}
    </details>
  </li>\n'''
        else:
            # 空目录也可以显示，但无子内容
            html += f'  <li class="folder">📁 {d}</li>\n'
    
    # 处理当前目录下的 .html 文件
    for f in files:
        # 计算相对路径（相对于根目录）
        rel_path = os.path.relpath(os.path.join(current_dir, f), start=root_dir)
        name = os.path.splitext(f)[0]
        html += f'  <li class="file"><a href="{rel_path}">{name}</a></li>\n'
    
    html += '</ul>\n'
    return html

def generate_index():
    """生成完整的 index.html"""
    # 扫描从根目录开始
    tree_html = generate_tree_html('.', '.')
    
    full_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>思维导图站 - 索引目录</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            background: #f6f8fa;
        }}
        h1 {{
            color: #24292f;
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 0.3rem;
        }}
        .file-tree {{
            list-style: none;
            padding-left: 0;
        }}
        .file-tree ul {{
            list-style: none;
            padding-left: 1.5rem;
        }}
        .folder {{
            margin: 0.4rem 0;
            cursor: default;
        }}
        details {{
            margin-left: 0;
        }}
        summary {{
            cursor: pointer;
            font-weight: 500;
            color: #0969da;
            outline: none;
        }}
        summary:hover {{
            color: #0550ae;
        }}
        .file {{
            margin: 0.25rem 0 0.25rem 1.2rem;
        }}
        a {{
            text-decoration: none;
            color: #0969da;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .note {{
            background: #fff;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            border: 1px solid #e1e4e8;
            color: #57606a;
        }}
    </style>
</head>
<body>
    <h1>📚 文件索引</h1>
    <div class="note">💡 点击文件夹前的 <strong>▶</strong> 可展开/收起子目录。</div>
    {tree_html}
</body>
</html>"""
    return full_html

if __name__ == "__main__":
    print("🔍 正在扫描目录树...")
    html_content = generate_index()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ 已生成 index.html，包含目录层级结构。")