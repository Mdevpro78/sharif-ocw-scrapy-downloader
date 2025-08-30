import scrapy


class SharifOcwDownloaderSessionItem(scrapy.Item):
    """
    Represents a session item in the Sharif OCW downloader pipeline.

    Responsibilities:
        1. Carry session data through pipelines.
    Collaborators:
        - Spider (Association - created by)
        - DownloadPipeline (Dependency - processed by)
        - FileSystemPipeline (Dependency - uses)
    """

    # Content information
    title = scrapy.Field()
    ext = scrapy.Field()
    link = scrapy.Field()

    # Ordering
    chapter_sort = scrapy.Field()
    session_sort = scrapy.Field()

    # Metadata
    course_title = scrapy.Field()
    chapter_title = scrapy.Field()
