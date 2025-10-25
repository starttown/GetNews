# Daily News Aggregator

A simple daily news aggregator that fetches hot news from multiple RSS sources and generates English Markdown reports.

## Features

- 📰 **Multi-category News Aggregation**: Tech, Gaming, Finance, Science, Entertainment news
- 🔄 **Manual Execution**: Run on-demand, no scheduled tasks
- 🤖 **MCP Integration**: Enhanced news sources via MCP servers (Brave Search, EXA, Finance MCP)
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

```json
{
  "categories": {
    "tech": ["technology", "AI", "programming", "gadgets"],
    "gaming": ["gaming", "games", "esports", "virtual reality", "copyright", "law", "infringement"]
  },
  "sources": {
    "tech": ["https://feeds.arstechnica.com/arstechnica/technology-lab"],
    "gaming": ["https://www.gamespot.com/feeds/news/"]
  },
  "mcp_sources": {
    "enabled": true,
    "sources": {
      "tech": ["exa", "brave"],
      "gaming": ["brave"],
      "finance": ["financemcp", "brave"],
      "science": ["brave"],
      "entertainment": ["brave"]
    },
    "config": {
      "brave": {
        "freshness": "pw",
        "count": 5,
        "result_filter": ["news", "web"]
      },
      "exa": {
        "numResults": 5
      },
      "financemcp": {
        "max_results": 5
      }
    }
  },
  "category_names": {
    "tech": "Tech",
    "gaming": "Gaming"
  }
}
```

### MCP Sources

The aggregator now supports MCP (Model Context Protocol) servers for enhanced news gathering:

- **Brave Search**: General web news search with filtering options
- **EXA**: Technology-focused search and documentation
- **Finance MCP**: Specialized financial news and market data

Each category can be configured to use specific MCP sources in the `mcp_sources.sources` configuration.

## Project Structure

```
GetNews/
├── daily_news_aggregator.py    # Main news aggregation script
├── mcp_client.py              # MCP client for external news sources
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
- `asyncio-subprocess==0.2.0` - Async subprocess support

## Usage

1. Run `python daily_news_aggregator.py` to fetch latest news (RSS + MCP sources)
2. Check `news_output/` directory for Markdown files
3. Run `python translate_news.py` for Chinese version if needed
4. Translation script automatically finds the latest news file

### MCP Integration

The system now integrates multiple MCP servers for enhanced news gathering:

- **RSS Sources**: Traditional RSS feed parsing (existing functionality)
- **MCP Sources**: Real-time news from specialized servers
  - Brave Search: General news with advanced filtering
  - EXA: Technology-focused search and documentation
  - Finance MCP: Financial news and market data

**Configuration Requirements**:
1. Set up API keys in `news_config.json` under `api_keys` section
2. Configure which MCP sources to use for each category in `mcp_sources.sources`
3. Enable/disable MCP functionality with `mcp_sources.enabled`

News from both RSS and MCP sources are automatically deduplicated and merged in the final report.

## Notes

- Translation requires internet connection
- RSS sources may occasionally be unavailable, program skips failed sources
- MCP sources provide real-time news but require internet connectivity
- Translation API has rate limits, program adds delays automatically
- MCP integration can be disabled by setting `mcp_sources.enabled: false` in config