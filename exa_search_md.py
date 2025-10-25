#!/usr/bin/env python3
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import re
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

class NewsMCPClient:
    """MCP客户端，用于获取新闻并写入markdown文件"""
    
    def __init__(self, tool_name:str, url: str, arguments: str, output_dir:str):
        self.tool_name = tool_name
        self.url = url
        self.arguments = arguments
        self.output_dir = output_dir
        self.session: Optional[ClientSession] = None
        
    async def connect(self):
        """连接到MCP服务器"""
        try:
            print("🔗 正在连接到MCP服务器...")
            async with streamablehttp_client(self.url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    self.session = session
                    await session.initialize()
                    # 列出可用工具
                    tools_result = await session.list_tools()
                    available_tools = [tool.name for tool in tools_result.tools]
                    print(f"✅ 连接成功！可用工具: {', '.join(available_tools)}")
                    # 获取新闻并处理
                    await self.get_and_process_news()
                    
        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            raise
    
    async def get_news(self) -> List[Dict[str, Any]]:
        """获取新闻数据"""
        try:
            print(f"📰 正在获取{self.tool_name}类新闻")
            result = await self.session.call_tool(
                self.tool_name,
                self.arguments
            )
            print(f"📡 成功获取新闻数据")
            return json.loads(result.content[0].text) 
            
        except Exception as e:
            print(f"❌ 获取新闻失败: {str(e)}")
            return []
        
    async def add_closing_bracket(self,s: str) -> str:
        """
        如果 `s` 中出现 '('，就在末尾补齐 ')'
        """
        return s + ')' if '(' in s else s



    async def news_to_markdown(self,news_item):
        """将单个新闻条目转换为Markdown格式"""
        metadata = [
            f"**title:** {news_item.get('title', '')}",
            f"**author:** {news_item.get('author', '')}",
            f"**publishedDate:** {news_item.get('publishedDate', '')}",
            f"**source:** {news_item.get('url', '')}",
        ]
        
        content = [
            f"\n# {news_item.get('title', '')}\n",
            "\n".join(metadata) + "\n",
        ]
        
        # 添加图片（如果有）
        if news_item.get('image'):
            content.append(f"![image]({news_item['image']})\n")
        
        # 添加正文内容
        text = news_item.get('text', '')
        
        # 清理Wikipedia特有的链接
        LINK_RE = re.compile(r'\(http([^)]+)\)')

        links = LINK_RE.findall(text)

        if not links:
            print("⚠️ 这个文本里没有 Markdown 链接")
            return "\n".join(content)
        
        # ------------------------------------------------------------
        content.extend([f"**text:**"])

        for i, url in enumerate(links, start=1):
            content.extend([f"{i}. http{await self.add_closing_bracket(url)}"])
        
        content.extend([f"-"*200," "])

        return "\n".join(content)
    
    async def get_and_process_news(self):
        """获取新闻并处理的主要流程"""
        try:
            # 定义要获取的新闻类别
            print(f"🔄 正在处理 {self.tool_name} 类新闻...")
            # 获取新闻数据
            news_data = await self.get_news()
            results = news_data.get('results', [])
            news_count = 0
            today = datetime.now().strftime('%Y-%m-%d')

            filename = f"{self.tool_name}_{self.arguments.get("query","")}{today}.md"
            output_path = self.output_dir / filename

            with open(output_path, 'w', encoding='utf-8') as f:    
                for item in results:
                    markdown = await self.news_to_markdown(item)
                    f.write(markdown)
                    news_count += 1
                print(f"已保存{news_count}条到: {output_path} ") 

        except Exception as e:
            print(f"❌ 处理新闻时出错: {str(e)}")
            raise


async def main():
   
    print("🚀 启动MCP新闻获取客户端...")
    tool_name = "web_search_exa"
    url = "https://mcp.exa.ai/mcp?api_key=your_api_key&profile=your_profile"
    arguments = {
        "query": "games",
        "numResults": 10
    }
    output_dir = Path("news_output")

    try:
        # 创建客户端实例
        client = NewsMCPClient(tool_name, url,arguments,output_dir)
        # 连接并执行任务
        await client.connect()
        print("🎉 所有任务执行完成！")
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断操作")
    except Exception as e:
        print(f"\n💥 程序执行出错: {str(e)}")
    finally:
        print("👋 程序结束")


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())




    

    
