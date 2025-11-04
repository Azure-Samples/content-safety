# Content Safety Failover Walkthrough

This folder contains an escalation workflow that combines multiple Azure Content Safety features with a model-based fallback. The `content_filters.py` script illustrates how to chain severity thresholds, blocklists, and an Azure OpenAI evaluation to decide whether content should be blocked.

## Prerequisites

Populate the following variables in the root `.env` file before running the sample:

| Variable | Purpose |
| --- | --- |
| `FOUNDRY_CONTENTSAFETY_ENDPOINT` | Primary Content Safety endpoint used by the main and secondary filters |
| `FOUNDRY_CONTENTSAFETY_KEY` | Key for the Content Safety resource above |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint used for the model evaluation pass |
| `AZURE_OPENAI_DEPLOYMENT_KEY` | Key associated with the Azure OpenAI deployment |
| `AZURE_OPENAI_DEPLOYMENT_ID` | Deployment name referenced during chat completions |

> Tip: This script shares the same Poetry environment as the rest of the repository. Follow the setup steps in the root `README.md` to install dependencies.

## How the Workflow Operates

1. `ContentFilterFactory` prepares two `ContentSafetyClient` instances with different severity thresholds (`Level.MEDIUM` for the main pass and `Level.LOW` for the secondary pass).
2. `ContentFilteringApp.evaluate_content` runs the primary filter first. If a category meets or exceeds the configured severity, the secondary filter double-checks the classification.
3. When the secondary filter is also triggered, the content is sent to `model_evaluation`, which uses Azure OpenAI to obtain a final verdict (`Harmfull` or `Not Harmfull`).
4. Any content confirmed as harmful is added to the configured blocklist through `BlocklistClient.add_or_update_blocklist_items`.
5. The function returns the original content when it passes all checks, or `None` when it is escalated and stored in the blocklist.

## Step-by-Step Walkthrough

1. Confirm the prerequisites and dependency installation from the root documentation.
2. Choose or create a blocklist name and update the `blocklist` variable in `content_filters.py` if necessary.
3. Replace the sample paragraph in the `__main__` section with the text you want to evaluate.
4. (Optional) Adjust the `Level` enum values or swap the severity thresholds when instantiating `ContentFilterFactory.create_client` to tune sensitivity.
5. Run the workflow: `poetry run python src/cs_failover/content_filters.py`.
6. Review the console output to see which filters were triggered and inspect the Content Safety blocklist to confirm the escalation.

## Extending the Sample

- Integrate additional blocklist rules by calling `add_to_blocklist` directly with custom descriptions.
- Swap the Azure OpenAI evaluation for another model or prompt if you want a different escalation policy.
- Wrap the `ContentFilteringApp` class in a web framework or Azure Function to expose the failover logic as an API.
