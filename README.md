# Content Safety Repository

Welcome! This repository gathers several Azure Content Safety demonstrations that show how to analyze text, images, prompts, and build higher-level moderation workflows with failover logic. Use this document as the central hub and dive into the per-folder READMEs for deep dives and walkthroughs.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Running the Demonstrations](#running-the-demonstrations)
- [Repository Layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.11 or later
- An Azure subscription with the [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) resource provisioned
- (Optional) An Azure OpenAI resource for groundedness and failover demonstrations
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

Set the following environment variables in a `.env` file at the repository root (all scripts load values with `python-dotenv`). Only populate the variables needed for the demos you plan to run.

| Variable | Description |
| --- | --- |
| `AZURE_CONTENTSAFETY_ENDPOINT` | Endpoint of the Azure Content Safety resource |
| `AZURE_CONTENTSAFETY_KEY` | Key of the Azure Content Safety resource |
| `AZURE_CONTENTSAFETY_API_VERSION` | API version when calling REST demos such as blocklists |
| `AZURE_OPENAI_ENDPOINT` | (Optional) Azure OpenAI endpoint used by groundedness and failover workflows |
| `AZURE_OPENAI_DEPLOYMENT_ID` | (Optional) Deployment name used for groundedness and failover workflows |
| `AZURE_OPENAI_DEPLOYMENT_KEY` | (Optional) Key used by failover workflow to authenticate with Azure OpenAI |
| `FOUNDRY_CONTENTSAFETY_ENDPOINT` | (Optional) Content Safety endpoint leveraged by the failover sample |
| `FOUNDRY_CONTENTSAFETY_KEY` | (Optional) Content Safety key leveraged by the failover sample |

## Environment Setup

1. Clone this repository and change into the directory.
2. Create and populate a `.env` file with the variables listed above.
3. Install dependencies with `poetry install`.
4. If you use Poetry's virtual environment, activate it (for example, `poetry shell`).

## Running the Demonstrations

Each scenario includes a numbered walkthrough. Start with the summaries in [`src/README.md`](src/README.md) and follow the linked instructions for:

- Text analysis with severity scoring
- Image content safety
- Prompt shielding and blocklist operations via REST
- Comprehensive REST factory patterns for Content Safety
- Content moderation failover logic that escalates responses

The [`src/cs_failover/README.md`](src/cs_failover/README.md) file focuses on the failover implementation and explains how to orchestrate cascading filters.

## Repository Layout

- `src/` – Source code and individual scenario walkthroughs (see `src/README.md`)
- `src/cs_failover/` – Failover workflow and advanced moderation logic (see `src/cs_failover/README.md`)
- `tests/` – Automated tests for selected components
- `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE.md` – Project metadata

## Contributing

We welcome contributions! Please read the [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
