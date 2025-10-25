#!/usr/bin/env python3
"""
新闻翻译脚本 - 将生成的新闻报告翻译成中文
只翻译文本内容，保留链接
"""

import re
from pathlib import Path
from deep_translator import GoogleTranslator
import time

class NewsTranslator:
    """新闻翻译器"""

    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='zh-CN')

    def translate_text(self, text: str) -> str:
        """翻译文本，跳过空字符串和链接"""
        if not text or not text.strip():
            return text

        # 跳过链接
        if text.startswith('http') or '://' in text:
            return text

        # 跳过纯数字和特殊字符
        if re.match(r'^[\d\s\.\-\(\)]+$', text):
            return text

        try:
            # 分批翻译，避免过长文本
            if len(text) > 1000:
                chunks = self._split_text(text)
                translated_chunks = []
                for chunk in chunks:
                    if chunk.strip():
                        translated = self.translator.translate(chunk)
                        translated_chunks.append(translated)
                        time.sleep(0.1)  # 减少延迟
                return ''.join(translated_chunks)
            else:
                time.sleep(0.1)  # 减少延迟
                return self.translator.translate(text)
        except Exception as e:
            print(f"翻译失败: {e}")
            return text

    def _split_text(self, text: str, max_length: int = 1000) -> list:
        """将长文本分割成小块"""
        chunks = []
        while len(text) > max_length:
            # 找到合适的分割点
            split_pos = text.rfind('.', 0, max_length)
            if split_pos == -1:
                split_pos = text.rfind(' ', 0, max_length)
            if split_pos == -1:
                split_pos = max_length

            chunks.append(text[:split_pos + 1])
            text = text[split_pos + 1:]
        if text:
            chunks.append(text)
        return chunks

    def translate_markdown_file(self, input_file: str, output_file: str = None):
        """翻译Markdown文件"""
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"文件不存在: {input_file}")
            return

        if output_file is None:
            output_file = str(input_path.parent / f"{input_path.stem}_cn{input_path.suffix}")

        print(f"开始翻译文件: {input_file}")

        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分行处理
        lines = content.split('\n')
        translated_lines = []

        for i, line in enumerate(lines):
            # 跳过空行
            if not line.strip():
                translated_lines.append(line)
                continue

            # 跳过标题符号和格式
            if line.strip().startswith('#') or line.strip().startswith('*') or line.strip().startswith('-'):
                # 只翻译标题文本部分
                if '**' in line:
                    # 处理粗体文本
                    parts = re.split(r'(\*\*.*?\*\*)', line)
                    translated_parts = []
                    for part in parts:
                        if part.startswith('**') and part.endswith('**'):
                            # 翻译粗体内容
                            inner_text = part[2:-2]
                            translated_inner = self.translate_text(inner_text)
                            translated_parts.append(f"**{translated_inner}**")
                        else:
                            translated_parts.append(self.translate_text(part))
                    translated_lines.append(''.join(translated_parts))
                else:
                    translated_lines.append(self.translate_text(line))
            else:
                # 普通文本行
                translated_lines.append(self.translate_text(line))

            # 添加延迟避免API限制
            if i > 0 and i % 10 == 0:
                time.sleep(0.2)

        # 保存翻译后的文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(translated_lines))

        print(f"翻译完成，保存到: {output_file}")

def main():
    """主函数"""
    translator = NewsTranslator()

    # 获取最新的新闻文件
    news_dir = Path("news_output")
    if not news_dir.exists():
        print("news_output目录不存在")
        return

    # 查找最新的md文件
    md_files = list(news_dir.glob("daily_news_*.md"))
    if md_files:
        latest_md = max(md_files, key=lambda x: x.stat().st_mtime)
        print(f"找到最新的Markdown文件: {latest_md}")
        translator.translate_markdown_file(str(latest_md))

if __name__ == "__main__":
    main()