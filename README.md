# Daily News Aggregator

A simple daily news aggregator that fetches hot news from multiple RSS sources and generates English Markdown reports.

## Features

- 📰 **Multi-category News Aggregation**: Tech, Gaming, Finance, Science, Entertainment news
- 🔄 **Manual Execution**: Run on-demand, no scheduled tasks
- 🤖 **MCP Integration**: Enhanced news sources via MCP servers (EXA)
- 🌐 **Translation Support**: Independent translation script for Chinese versions
- 📊 **Markdown Output**: Clean Markdown format reports
- ⚙️ **Configurable**: JSON-based configuration for easy customization

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get News

```bash
python daily_news_aggregator.py
```

### 3. Translate to Chinese (Optional)

```bash

python translate_news.py

```
use translation website: https://markdown.guru/translate/zh-cn

## Output Files

- `news_output/daily_news_YYYY-MM-DD.md` - English news report
- `news_output/daily_news_YYYY-MM-DD_cn.md` - Chinese translated version

## RSS Source Configuration

Edit `news_config.json` to customize RSS and MCP sources:



### MCP Sources

The aggregator now supports MCP (Model Context Protocol) servers for enhanced news gathering:

- **EXA**: Technology-focused search and documentation

Each category can be configured to use specific MCP sources in the `mcp_sources.sources` configuration.

## Project Structure

```
GetNews/
├── daily_news_aggregator.py    # Main news aggregation script
├── exa_search_md.py            # Exa_search_md
├── translate_news.py           # Translation script
├── news_config.json            # Configuration file
├── requirements.txt            # Dependencies
├── news_output/                # Output directory
└── README.md                   # Documentation
```

## Dependencies

- `aiohttp==3.9.1` - Asynchronous HTTP requests
- `deep-translator==1.11.4` - Translation library
- `mcp==1.0.0` - MCP client library

## Usage

1. Run `python daily_news_aggregator.py` to fetch latest news (RSS + MCP sources)
2. Check `news_output/` directory for Markdown files
3. Run `python translate_news.py` for Chinese version if needed
4. Translation script automatically finds the latest news file

### MCP Integration

The system now integrates multiple MCP servers for enhanced news gathering:

- **RSS Sources**: Traditional RSS feed parsing (existing functionality)
- **MCP Sources**: Real-time news from specialized servers
  - EXA: Technology-focused search and documentation

**Configuration Requirements**:
1. Set up API keys in `exa_search_md.py` 


News from both RSS and MCP sources are automatically deduplicated and merged in the final report.

## Notes

- Translation requires internet connection
- RSS sources may occasionally be unavailable, program skips failed sources
- MCP sources provide real-time news but require internet connectivity
- Translation API has rate limits, program adds delays automatically
