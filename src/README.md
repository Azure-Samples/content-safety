# Source Demos Walkthrough

This folder contains the runnable samples that demonstrate different facets of Azure Content Safety. Each section below lists the purpose of the script, its key capabilities, and a step-by-step walkthrough to execute it.

All scripts rely on environment variables loaded from a `.env` file in the repository root. See the root `README.md` for the common setup steps (install dependencies with Poetry and populate credentials).

## `blocklist.py` – Blocklist Management via REST

Highlights

- Creates or updates a text blocklist using the REST API
- Adds multiple entries to the blocklist
- Analyzes a sample text against both the standard classifiers and the custom blocklist

Walkthrough

1. Ensure `AZURE_CONTENTSAFETY_ENDPOINT`, `AZURE_CONTENTSAFETY_KEY`, and `AZURE_CONTENTSAFETY_API_VERSION` are present in `.env`.
2. Optionally edit the `blocklistName`, `blocklistItems`, or sample `text` values in the script to match your scenario.
3. Run the demo: `poetry run python src/blocklist.py`.
4. Review the console output to confirm blocklist creation, item upload, and text analysis results.

## `text.py` – Asynchronous Text Analysis

Highlights

- Uses the asynchronous SDK client (`azure.ai.contentsafety.aio`) for batch text moderation
- Demonstrates severity scoring across all built-in categories
- Includes multiple sample texts to trigger different classification paths

Walkthrough

1. Set `AZURE_CONTENTSAFETY_ENDPOINT` and `AZURE_CONTENTSAFETY_KEY` in `.env`.
2. Adjust or translate the sample paragraphs if needed to test additional behaviors.
3. Execute the script: `poetry run python src/text.py`.
4. Inspect the printed dictionaries to see severity levels per category.

## `image.py` – Image Safety Classification

Highlights

- Calls the image analysis endpoint asynchronously
- Processes a set of sample images located under `src/images/`
- Prints the raw response for deeper inspection of category scores

Walkthrough

1. Confirm `AZURE_CONTENTSAFETY_ENDPOINT` and `AZURE_CONTENTSAFETY_KEY` exist in `.env`.
2. Replace the example files in `src/images/` with your own images if desired (maintain relative paths or update the constants).
3. Run the analysis: `poetry run python src/image.py`.
4. Examine the output to compare moderation results across the provided images.

## `prompt_shield.py` – Prompt Shield Factory Pattern

Highlights

- Implements the factory pattern to encapsulate REST prompt-shield calls
- Sends the same user prompt with and without additional contextual documents
- Returns formatted JSON responses for easy reading

Walkthrough

1. Provide `AZURE_CONTENTSAFETY_ENDPOINT` and `AZURE_CONTENTSAFETY_KEY` in `.env`.
2. Modify the `user_prompt` or `documents` arrays to replicate the prompt-injection scenario you want to test.
3. Execute: `poetry run python src/prompt_shield.py`.
4. Review the JSON output for both executions to understand how mitigation guidance changes.

## `rest_cs.py` – Comprehensive REST Factory Showcase

Highlights

- Demonstrates an extensible factory hierarchy that orchestrates multiple Content Safety operations
- Includes dedicated products for blocklists, groundedness validation, prompt shielding, and harmful content analysis
- Shows how to reuse configuration and headers across REST calls

Walkthrough

1. Populate the baseline Content Safety variables (`AZURE_CONTENTSAFETY_ENDPOINT`, `AZURE_CONTENTSAFETY_KEY`).
2. Add Azure OpenAI settings—`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT_ID`—to enable the groundedness workflow.
3. Adjust sample texts or blocklist entries inside `client_code` to match your use case.
4. Run the orchestrator: `poetry run python src/rest_cs.py`.
5. Observe the console output for each factory invocation to see how responses differ by product.

## Next Steps

For advanced escalation logic and failover handling, continue with the dedicated walkthrough in [`cs_failover/README.md`](cs_failover/README.md).
