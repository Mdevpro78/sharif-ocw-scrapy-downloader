from urllib.parse import urlparse
from collections.abc import Iterator

import scrapy
import orjson as json
from scrapy.http import Request, Response

from ..items import SharifOcwDownloaderSessionItem


class CourseSpider(scrapy.Spider):
    """Spider for downloading course content from Sharif OCW.

    This spider crawls the Sharif OCW API to discover and download course content.
    It handles course metadata parsing, session discovery, and generates download items.

    Responsibilities:
        - Initiate crawl with course metadata request
        - Parse course metadata from API responses
        - Discover and parse course sessions
        - Generate download items for pipeline processing

    Collaborators:
        - Scrapy Settings: Configuration parameters
        - Request: HTTP request generation
        - Response: API response handling
        - SharifOcwDownloaderSessionItem: Download item creation
    """

    name = "sharif_ocw_course_downloader"
    allowed_domains = (
        "ocw.sharif.ir",
        "ocw.sharif.edu",
    )

    def __init__(
        self,
        course_id: int,
        settings,
        *args,
        **kwargs,
    ):
        """
        Initialize spider with course ID and settings.

        Args:
            course_id: Course identifier
            settings: Application settings
        """
        super().__init__(*args, **kwargs)
        self.course_id = course_id
        self.app_settings = settings
        self.ocw_course_url = settings.get("OCW_COURSE_URL")
        self.ocw_chapter_url = settings.get("OCW_CHAPTER_URL")
        self.ocw_content_base_url = settings.get(
            "OCW_BASE_URL",
        )

    async def start(self) -> Iterator[Request]:
        """
        Generate initial requests.

        Yields:
            Request for course metadata
        """
        self.logger.info(
            f"Starting crawl for course ID: {self.course_id}",
        )

        course_request_payload = {"id": self.course_id}
        yield Request(
            url=f"{self.ocw_course_url}",
            method="POST",
            callback=self.parse_metadata,
            meta={
                "course_id": self.course_id,
            },
            body=json.dumps(course_request_payload),
            dont_filter=True,
            priority=10,
        )

    def parse_metadata(
        self,
        response: Response,
    ) -> Iterator[Request]:
        """
        Parse course metadata response.

        Args:
            response: HTTP response with course metadata
        Yields:
            Request for chapters and sessions metadata
        """
        try:
            # Parse JSON response
            course = json.loads(response.text)
            course_title = course["title"]
            # Prepare payload
            payload = {
                "limit": None,
                "order_type": "ASC",
                "course_id": self.course_id,
                "status": ["free", "non-free"],
            }
            yield Request(
                url=self.ocw_chapter_url,
                method="POST",
                body=json.dumps(payload),
                callback=self.parse_sessions,
                meta={
                    "course_id": self.course_id,
                    "course_title": course_title,
                },
                dont_filter=True,
                priority=9,
            )

        except Exception as e:
            self.logger.error(f"Error parsing metadata: {e}")
            self.handle_parse_error(response, e)

    def parse_sessions(
        self,
        response: Response,
    ) -> Iterator[SharifOcwDownloaderSessionItem]:
        """
        Parse sessions response and yield download items.

        Args:
            response: HTTP response with sessions data

        Yields:
            SharifOcwDownloaderSessionItem for each downloadable session
        """
        # Parse JSON response
        data = json.loads(response.text)
        course_title = response.meta.get("course_title")
        chapter_counter = 0
        # Extract chapters
        chapters_data = data.get("chapters", {})
        for _, chapter_data in chapters_data.items():
            for session in chapter_data.get("sessions", []):
                yield SharifOcwDownloaderSessionItem(
                    title=session.get("title"),
                    link=f"{self.ocw_content_base_url}{session.get('link')}",
                    session_sort=session.get("sort"),
                    ext=self._get_extension(
                        url=session.get("link"),
                    ),
                    chapter_title=chapter_data.get("title"),
                    chapter_sort=chapter_counter,
                    course_title=course_title,
                )
            chapter_counter += 1

    def _get_extension(self, url: str) -> str:
        """Extract file extension."""
        path = urlparse(url).path
        return (
            "." + path.split(".")[-1] if "." in path else ".bin"
        )
