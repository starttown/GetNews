#!/usr/bin/env python3
"""
每日新闻聚合器 - 获取多领域热点新闻并生成中文总结
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List
import aiohttp
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class NewsItem:
    """新闻条目数据类"""
    title: str
    content: str
    url: str
    source: str
    category: str
    published_at: str
    summary: str = ""
    tags: List[str] = None
    title_cn: str = ""  # 中文标题
    summary_cn: str = ""  # 中文摘要

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class DailyNewsAggregator:
    """每日新闻聚合器"""

    def __init__(self, config_file="news_config.json"):
        self.config_file = config_file
        self.load_config()

        self.output_dir = Path("news_output")
        self.output_dir.mkdir(exist_ok=True)

    def load_config(self):
        """从JSON配置文件加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.categories = config.get('categories', {})
            self.sources = config.get('sources', {})
            self.category_names = config.get('category_names', {})

        except FileNotFoundError:
            print(f"FileNotFoundError")
            raise

        except Exception as e:
            print(f"加载配置文件失败: {e}")
            raise



    async def fetch_rss_feed(self, url: str, category: str) -> List[NewsItem]:
        """获取RSS源新闻 - 使用简单HTTP请求"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()

                        # 简单解析RSS XML（临时方案）
                        news_items = []
                        import xml.etree.ElementTree as ET

                        try:
                            root = ET.fromstring(content)
                            items = root.findall('.//item')[:10]  # 取前10条

                            for item in items:
                                title_elem = item.find('title')
                                link_elem = item.find('link')
                                desc_elem = item.find('description')

                                if title_elem is not None and link_elem is not None:
                                    title = title_elem.text.strip() if title_elem.text else ""
                                    url = link_elem.text.strip() if link_elem.text else ""
                                    content = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""

                                    if title and url:
                                        # 创建新闻条目
                                        news_item = NewsItem(
                                            title=title,
                                            content=content,
                                            url=url,
                                            source=url.split('/')[2] if '/' in url else 'Unknown',
                                            category=category,
                                            published_at=datetime.now().isoformat(),
                                            summary=self.generate_summary(content)
                                        )
                                        news_items.append(news_item)

                        except ET.ParseError:
                            print(f"XML解析失败: {url}")

                        return news_items
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return []

    def parse_date(self, date_tuple):
        """解析日期元组"""
        if date_tuple:
            try:
                return datetime(*date_tuple[:6])
            except:
                pass
        return None

    def generate_summary(self, content: str) -> str:
        """生成新闻摘要"""
        if len(content) > 200:
            return content[:200] + "..."
        return content



    def generate_category_summary(self, news_items: List[NewsItem], category: str) -> str:
        """为分类生成中文总结"""
        if not news_items:
            return "暂无新闻"

        # 提取所有标题和摘要
        titles = [item.title for item in news_items[:5]]  # 取前5条的主要新闻
        summaries = [item.summary for item in news_items[:5] if item.summary]

        # 生成总结文本
        summary_text = f"{category}类今日热点新闻："



        summary_text += "、".join(titles[:3])  # 取前3个标题

        # 添加趋势分析
        if len(news_items) > 10:
            summary_text += f"。今日共收集{len(news_items)}条相关新闻，显示该领域发展活跃。"
        elif len(news_items) > 5:
            summary_text += f"。今日共收集{len(news_items)}条相关新闻，值得关注。"
        else:
            summary_text += f"。今日共收集{len(news_items)}条相关新闻。"

        return summary_text



    async def aggregate_news(self) -> Dict[str, List[NewsItem]]:
        """聚合所有新闻"""
        all_news = {}

        for category, keywords in self.categories.items():
            print(f"正在获取{category}类新闻...")

            # RSS源新闻
            rss_news = []
            for rss_url in self.sources.get(category, []):
                news_items = await self.fetch_rss_feed(rss_url, category)
                if news_items:  # 确保不是None
                    rss_news.extend(news_items)


            # 合并并去重
            all_category_news = rss_news
            all_news[category] = self.deduplicate_news(all_category_news)

            print(f"{category}类获取到{len(all_news[category])}条新闻")

        return all_news

    def deduplicate_news(self, news_items: List[NewsItem]) -> List[NewsItem]:
        """去重新闻"""
        seen_urls = set()
        unique_news = []

        for item in news_items:
            if item.url not in seen_urls:
                seen_urls.add(item.url)
                unique_news.append(item)

        # 按发布时间排序
        unique_news.sort(key=lambda x: x.published_at, reverse=True)
        return unique_news[:20]  # 每类最多20条

    def generate_report(self, news_data: Dict[str, List[NewsItem]]) -> str:
        """生成日报"""
        report = f"# Daily Hot News Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        total_news = sum(len(news) for news in news_data.values())
        report += f"**Total News**: {total_news} items\n\n"

        for category, news_items in news_data.items():
            if news_items:
                category_name = self.category_names.get(category, category)

                report += f"## {category_name} ({len(news_items)} items)\n\n"

                for i, item in enumerate(news_items[:10], 1):  # 每类显示前10条
                    report += f"### {i}. {item.title}\n"
                    report += f"**Source**: {item.source}\n"
                    report += f"**Date**: {item.published_at[:10]}\n"
                    if item.summary:
                        report += f"**Summary**: {item.summary}\n"
                    report += f"**Link**: {item.url}\n\n"

        return report

    async def save_report(self, report: str):
        """保存报告"""
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"daily_news_{today}.md"

        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"新闻报告已保存到: {filepath}")

    async def run_daily_aggregation(self):
        """运行每日新闻聚合"""
        print("开始每日新闻聚合...")

        # 聚合新闻
        news_data = await self.aggregate_news()

        # 生成报告
        report = self.generate_report(news_data)

        # 保存报告
        await self.save_report(report)

        print("每日新闻聚合完成！")

async def main():
    """主函数"""
    aggregator = DailyNewsAggregator()
    await aggregator.run_daily_aggregation()

if __name__ == "__main__":
    asyncio.run(main())