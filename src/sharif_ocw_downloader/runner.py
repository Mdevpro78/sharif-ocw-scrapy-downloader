"""
Main runner for the Scrapy application.

Responsibilities:
    1. Parse command-line arguments
    2. Configure Scrapy process
    3. Initialize spider
    4. Execute crawl
    5. Handle shutdown
Collaborators:
    - CrawlerProcess (Composition - creates)
    - CourseSpider (Composition - runs)

Definition: Entry point that orchestrates the entire crawl process from
            configuration to execution.
"""

import argparse
import logging
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings
from src.sharif_ocw_downloader.spiders.course_spider import (
    CourseSpider,
)

logger = logging.getLogger(__file__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="OCW Scraper - Download course content from Sharif OCW",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--course-id",
        type=int,
        required=True,
        help="Course ID to download",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("./downloads"),
        help="Output directory (default: ./downloads)",
    )

    parser.add_argument(
        "--max-concurrent-downloads",
        type=int,
        default=5,
        choices=range(1, 21),
        metavar="[1-20]",
        help="Maximum concurrent downloads (default: 5)",
    )

    parser.add_argument(
        "--toggle-ordinals",
        action="store_true",
        default=True,
        help="Include ordinal numbers in names (default: True)",
    )

    parser.add_argument(
        "--no-ordinals",
        dest="toggle_ordinals",
        action="store_false",
        help="Exclude ordinal numbers from names",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite existing files (default: False)",
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()

    # Create settings
    settings = get_project_settings()
    output_path = Path(args.output_path).resolve().absolute()
    logger.info(output_path)
    settings["FILES_STORE"] = str(output_path.as_posix())
    settings["OCW_USE_ORDINALS"] = args.toggle_ordinals
    settings["OCW_OVERWRITE_EXISTING"] = args.overwrite
    settings["CONCURRENT_REQUESTS"] = (
        args.max_concurrent_downloads
    )
    settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = (
        args.max_concurrent_downloads
    )
    settings["CONCURRENT_ITEMS"] = args.max_concurrent_downloads

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Create crawler process
    process = CrawlerProcess(settings)

    # Start spider
    process.crawl(
        CourseSpider,
        course_id=args.course_id,
        settings=settings,
    )

    # Print configuration
    print("=" * 60)
    print("OCW Scraper - Course Downloader")
    print("=" * 60)
    print(f"Course ID: {args.course_id}")
    print(f"Output Path: {args.output_path.resolve().absolute()}")
    print(f"Max Concurrent: {args.max_concurrent_downloads}")
    print(f"Use Ordinals: {args.toggle_ordinals}")
    print(f"Overwrite: {args.overwrite}")
    print("=" * 60)
    print("\nStarting download...\n")

    try:
        # Start the crawl
        process.start()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
