def write_to_markdown(content,filename="bazi_analysis.md"):
    """
    将生成的文本写入 Markdown 文件
    :param filename: str, 目标 Markdown 文件名
    :param content: str, 需要写入的 Markdown 格式内容
    """
    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write("# AI 生成的运势分析\n\n")  # 添加标题
        md_file.write(content)  # 写入生成内容