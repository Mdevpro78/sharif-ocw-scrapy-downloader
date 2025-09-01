import re
import logging
import unicodedata
from pathlib import Path
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline


logger = logging.getLogger(__name__)


class SharifOcwDownloaderPipeline(FilesPipeline):
    """
    Single pipeline handling both download and filesystem organization.

    This pipeline generates deterministic file paths in the format:
    {course_title}/{chapter_sort:03d}__{chapter_title}/{session_sort:03d}__{title}.{ext}
    """

    def get_media_requests(self, item, info):
        item = ItemAdapter(item)

        if link := item.get("link", None):
            yield Request(link, method="GET", dont_filter=True)

    def file_path(
        self,
        request,
        response=None,
        info=None,
        *,
        item=None,
    ):
        item_data = ItemAdapter(item)

        course_title = item_data.get("course_title", "unknown")
        chapter_sort = item_data.get("chapter_sort", 0)
        chapter_title = item_data.get("chapter_title", "chapter")
        session_sort = item_data.get("session_sort", 0)
        session_title = item_data.get("title", "session")
        ext = item_data.get("ext", ".bin")

        # Sanitize each component for both English and Persian
        course_title = self._sanitize_text_component(course_title)
        chapter_title = self._sanitize_text_component(
            chapter_title,
        )
        session_title = self._sanitize_text_component(
            session_title,
        )

        # Build path components with zero-padding
        chapter = f"{int(chapter_sort):03d}__{chapter_title}"
        session = f"{int(session_sort):03d}__{session_title}"

        # Ensure extension has proper format
        if ext and not ext.startswith("."):
            ext = f".{ext.lstrip('.')}"

        # Construct full path
        full_path = f"{course_title}/{chapter}/{session}{ext}"

        logger.info(f"Generated path: {full_path}")

        abs_path = (
            Path(self.crawler.settings.get("FILES_STORE"))
            / full_path
        )
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        return full_path

    def item_completed(self, results, item, info):
        if results:
            ok, x = results[0]
            item["download_status"] = (
                "completed" if ok else "failed"
            )
        return item

    @staticmethod
    def _sanitize_text_component(text) -> str:
        """Sanitize text component for filesystem use with Unicode support."""
        if not text or not isinstance(text, str):
            return "untitled"

        # Normalize Unicode for both English and Persian (NFC is more appropriate than NFC)
        text = unicodedata.normalize("NFC", text)

        # Remove zero-width and control characters
        text = re.sub(
            r"[\u200b-\u200f\uFEFF\x00-\x08\x0b\x0c\x0e-\x1f]",
            "",
            text,
        )

        # Replace invalid filesystem characters
        invalid_chars = re.compile(r'[<>:"/\\|?*]')
        text = invalid_chars.sub("_", text)

        # Clean up multiple underscores and whitespace
        text = re.sub(r"_+", "_", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip("_ ")

        return text or "untitled"
