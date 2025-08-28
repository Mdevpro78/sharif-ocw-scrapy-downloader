from config import config as env


BOT_NAME = env.OCW_BOT_NAME

SPIDER_MODULES = ["sharif_ocw_downloader.spiders"]
NEWSPIDER_MODULE = "sharif_ocw_downloader.spiders"

ADDONS = {}

# ===========================================================================
# OCW SETTINGS
# ===========================================================================

OCW_BASE_URL = env.OCW_BASE_URL
OCW_API_TIMEOUT = env.OCW_API_TIMEOUT
OCW_OUTPUT_PATH = env.OCW_OUTPUT_PATH
OCW_USE_ORDINALS = env.OCW_USE_ORDINALS
OCW_OVERWRITE = env.OCW_OVERWRITE_EXISTING
OCW_MAX_FILENAME = env.OCW_MAX_FILENAME_LENGTH
# ===========================================================================
# End of OCW SETTINGS
# ===========================================================================

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "sharif_ocw_downloader (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = env.ROBOTSTXT_OBEY

# Concurrency and throttling settings
CONCURRENT_REQUESTS = env.CONCURRENT_REQUESTS
CONCURRENT_REQUESTS_PER_DOMAIN = (
    env.CONCURRENT_REQUESTS_PER_DOMAIN
)
DOWNLOAD_DELAY = env.DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = env.RANDOMIZE_DOWNLOAD_DELAY

# Download
DOWNLOAD_TIMEOUT = env.DOWNLOAD_TIMEOUT
DOWNLOAD_MAXSIZE = env.DOWNLOAD_MAXSIZE
DOWNLOAD_WARNSIZE = env.DOWNLOAD_WARNSIZE

# Retry
RETRY_ENABLED = env.RETRY_ENABLED
RETRY_TIMES = env.RETRY_TIMES
RETRY_HTTP_CODES = [
    int(x.strip()) for x in env.OCW_RETRY_HTTP_CODES.split(",")
]

# Logging
LOG_ENABLED = env.LOG_ENABLED
LOG_LEVEL = env.LOG_LEVEL
LOG_STDOUT = env.LOG_STDOUT

# Disable cookies (enabled by default)
COOKIES_ENABLED = env.COOKIES_ENABLED

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = env.TELNETCONSOLE_ENABLED

# Stats
STATS_CLASS = (
    "scrapy.statscollectors.MemoryStatsCollector"
    if env.OCW_STATS_ENABLED
    else None
)

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": OCW_BASE_URL,
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "sharif_ocw_downloader.middlewares.SharifOcwDownloaderSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {}
if env.RETRY_ENABLED:
    DOWNLOADER_MIDDLEWARES.setdefault(
        "sharif_ocw_downloader.middlewares.SharifOcwDownloaderDownloaderMiddleware",
        550,
    )

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {}
if env.OCW_PROGRESS_ENABLED:
    ITEM_PIPELINES.setdefault(
        "sharif_ocw_downloader.pipelines.SharifOcwDownloaderPipeline",
        300,
    )
