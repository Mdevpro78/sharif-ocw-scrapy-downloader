<p align="center">
<h1 align="center"> Sharif OCW Scrapy's Downloader </h1>
<p align="center">

<a href="https://img.shields.io">
<img src="https://img.shields.io/badge/Project%20Status-Active-green.svg" alt="Project Status: Active">
</a>

<a href="https://www.python.org/downloads/">
<img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
</a>

<a href="https://scrapy.org">
<img src="https://img.shields.io/badge/Scrapy-2.11+-green.svg" alt="Scrapy Version">
</a>

<a href="https://pydantic.dev">
<img src="https://img.shields.io/badge/Pydantic-2.6+-blue.svg" alt="Pydantic Version">
</a>

<a href="https://www.mkdocs.org">
<img src="https://img.shields.io/badge/docs-mkdocs-blue.svg" alt="Documentation">
</a>

<a href="LICENSE">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</a>

</p>
<p align="center"><em> One-week MVP sprint board for OCW Sharif Scrapy's Downloader.</em>
</p>
<p align="center">
<a href="#getting-started" class="md-button md-button--primary">Getting Started</a>
<a href="https://github.com/Mdevpro78/sharif-ocw-scrapy-downloader" class="md-button">View on GitHub</a>
</p>
</p>

---

## 🚀 Getting Started

### 📥 Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Mdevpro78/sharif-ocw-scrapy-downloader
cd sharif-ocw-scrapy-downloader
```

### ⚡️ Quick Installation

Install the required dependencies using one of the following methods:

!!! tip "Installation Options"

    === "Using pip"

        ```bash
        # Install using pip
        pip install -r requirements.txt (or requirements.dev.txt )
        ```

    === "Using uv (Recommended)"

        ```bash
        # Sync dependencies
        make uv_sync_all
        ```

### 🏃‍♂️ Running the Crawler

#### Method 1: Using Makefile Commands

The project includes several convenient Makefile targets for common operations:

!!! example "Available Makefile Commands"

    ```bash
    # Set up development environment
    make setup_dev

    # Run pre-commit hooks
    make uv_pre_commit

    # Clean cache and temporary files
    make clean
    ```

#### Method 2: Direct Execution

To download course content, use the following command:

```bash
uv run python sharif_ocw_downloader/runner.py --course-id=course_id --max-concurrent-downloads=2 --output-path="../test_download_dir"
```

!!! info "Command Parameters"

    - `--course-id=course_id`: Specifies the course ID to download (replace with desired course ID)
    - `--max-concurrent-downloads=2`: Sets the maximum number of concurrent downloads
    - `--output-path="../test_download_dir"`: Defines the output directory for downloaded files

## 📁 Project Layout

!!! abstract "Directory Structure"

    ```plaintext
    sharif-ocw-scrapy-downloader/
    ├── .github/                    # GitHub workflows and configurations
    ├── docs/                       # Documentation files
    │   ├── index.md               # Main documentation page
    │   ├── contributing.md        # Contribution guidelines
    │   └── static/                # Static assets for documentation
    ├── src/                       # Source code
    │   └── sharif_ocw_downloader/ # Main package
    │       ├── spiders/           # Scrapy spiders
    │       ├── config.py          # Configuration management
    │       ├── items.py           # Scrapy items
    │       ├── middlewares.py     # Scrapy middlewares
    │       ├── pipelines.py       # Scrapy pipelines
    │       ├── runner.py          # Main runner script
    │       └── settings.py        # Scrapy settings
    ├── scripts/                   # Utility scripts
    ├── Dockerfile                 # Docker configuration
    ├── docker-compose.yml         # Docker Compose configuration
    ├── Makefile                   # Build and development commands
    ├── pyproject.toml             # Project configuration
    └── requirements.txt           # Python dependencies
    ```

---

## 👥 Contributing

!!! info "Ways to Contribute"

    We welcome all contributions! Choose your path:

    ```plaintext
    - 🐛 [Report Bugs](#bug-reports)
    - 💡 [Suggest Features](#feature-requests)
    - 🔧 [Submit Code](#pull-requests)
    ```

### Bug Reports {: #bug-reports }

!!! warning "Bug Report Template"

    ```markdown
    **Description:**
    Clear, concise description of the issue
    **Steps to Reproduce:**
    1. Step one
    2. Step two
    3. Current result
    4. Expected result
    **Environment:**
    - OS: [e.g., Windows 11]
    - Browser: [e.g., Chrome 120]
    - Version: [e.g., 1.0.0]
    ```

### Feature Requests {: #feature-requests }

!!! example "Feature Request Template"

    ```markdown
    **Problem:** What problem does this feature solve?
    **Solution:**
    Describe your proposed solution
    **Alternatives:**
    What alternatives have you considered?
    ```

### Pull Requests {: #pull-requests }

!!! tip "Quick Start"

    ```markdown
    # Setup git clone <https://github.com/username/repo>
    cd repo uv sync
    # Development
    git checkout -b feature/name
    # Make changes
    git commit -m "feat: add amazing feature"
    git push origin feature/name
    ```

    **Guidelines:**

    1. ✅ Follow code style
    2. 📝 Update docs

!!! success "Ready to Contribute"

    The project follows standard GitHub workflows. For detailed guidelines, see our [Contribution Guide](CONTRIBUTING.md).

---

<p align="center" style="margin-top: 32px; margin-bottom: 32px;">
<em>Built with ❤️ using <a href="https://www.mkdocs.org">MkDocs</a> and <a href="https://squidfunk.github.io/mkdocs-material/">Material for MkDocs</a></em>
</p>
