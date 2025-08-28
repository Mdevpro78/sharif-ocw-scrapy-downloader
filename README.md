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

## 📚 Overview

**Project Goal:** Deliver an MVP Scrapy-based downloader for Sharif OCW that:

- Fetches course metadata and sessions
- Downloads all downloadable files
- Organizes outputs into structured folders
- Provides progress tracking and basic error handling

**Success Criteria:**

- Able to download at least one complete course (videos + PDFs)
- Correct directory structure with sanitized filenames
- Basic duplicate detection + retry handling works
- GitHub issues, milestones, and PRs follow roadmap

**Team Size:** 1 developer (solo)

**Roles & Responsibilities:**

- Developer: Implement, test, document, manage repo, and review

**Definition of Done (DoD):**

- Code compiles and runs without errors
- Passes basic integration tests on one sample course
- Artifacts stored in correct directory structure
- Pull requests merged into `main` with review checklist passed

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip, uv, or another Python package manager

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/Mdevpro78/sharif-ocw-scrapy-downloader/
cd sharif-ocw-scrapy-downloader

# Install dependencies using UV (recommended)
make uv_sync_docs

# Or using pip
pip install -e .[docs]
```

### Running Locally

```bash
# Start the development server
make uv_mkdoc_serve

# Or using UV directly
uv run mkdocs serve
```

### Using Docker

MkDocForge can be easily run using Docker:

```bash
# Build the Docker image
make docker-build

# Start the container
make docker-up

# View logs
make docker-logs

# Stop the container
make docker-down
```

Alternatively, you can use Docker Compose directly:

```bash
# Build and start in one command
docker compose up

# Or build and start in detached mode
docker compose up -d
```

Once running, access the documentation at [http://localhost:8000](http://localhost:8000).

## 📁 Project Structure

### Directories

| Path     | Purpose                                     |
| -------- | ------------------------------------------- |
| docs/    | 📚 Docs: guidelines, roadmap, static assets |
| src/     | 🧩 Source (Scrapy project + package)        |
| .github/ | ⚙️ CI/CD workflows                          |
| scripts/ | 🧰 Utility scripts                          |

### Code layout (src)

| Path                                     | Role                           |
| ---------------------------------------- | ------------------------------ |
| src/scrapy.cfg                           | Scrapy config                  |
| src/sharif_ocw_downloader/config.py      | Configuration management       |
| src/sharif_ocw_downloader/items.py       | Item definitions (data models) |
| src/sharif_ocw_downloader/middlewares.py | Middleware components          |
| src/sharif_ocw_downloader/pipelines.py   | Item pipelines (process/store) |
| src/sharif_ocw_downloader/settings.py    | Scrapy settings                |
| src/sharif_ocw_downloader/spiders/       | Spider implementations         |

### Key files & configs

| File                  | Purpose                        |
| --------------------- | ------------------------------ |
| Dockerfile            | 🐳 Build Docker image          |
| docker-compose.yml    | Orchestrate services           |
| Makefile              | Common automation tasks        |
| mkdocs.yml            | MkDocs site config             |
| pyproject.toml        | Python project metadata/config |
| cliff.toml            | git-cliff (changelog) config   |
| requirements.lock     | Locked production deps         |
| requirements-dev.lock | Locked development deps        |

## 🔧 Configuration

MkDocForge is highly configurable through the `mkdocs.yml` file. See the [MkDocs documentation](https://www.mkdocs.org/) for basic configuration and explore our examples for advanced setups.

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guide](docs/contributing.md) for guidelines on how to make contributions.

## 👥 Target Audience

- **Development Teams**: Create comprehensive documentation for software projects
- **Technical Writers**: Leverage markdown with powerful extensions for technical content
- **Open Source Projects**: Provide high-quality documentation with minimal overhead
- **Organizations**: Maintain consistent documentation standards across projects

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Repository](https://github.com/Mdevpro78/mkdocforge)
- [Visit Documentation](https://mdevpro78.github.io/mkdocforge/)
- [MkDocs Official Site](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
