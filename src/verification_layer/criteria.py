"""Relevance rubric per module. See docs/CRITERIA.md for the full explanation.

Mirrors crm.modules in internal-db (session 04) — descriptions kept in sync
manually; internal-db's migrations/0006_seed_modules.sql is the source of truth
for the module list itself.
"""

from __future__ import annotations

VERIFIED_THRESHOLD = 9
MIN_DIMENSION_SCORE = 1  # any dimension at 0 is disqualifying regardless of total

# code -> (name, what counts as relevant, what doesn't)
MODULE_RELEVANCE: dict[str, dict[str, str]] = {
    "gtm-agent": {
        "name": "AI GTM / AI Sales",
        "relevant": "Warm-lead qualification logic, personalized outreach generation, "
        "demo-booking flow, or a CRM integration that moves leads through a pipeline.",
        "not_relevant": "A generic cold-email sender with no qualification/scoring step.",
    },
    "office-agent": {
        "name": "AI Office",
        "relevant": "Email triage/classification, internal knowledge base search "
        "(retrieval over internal docs), or document automation.",
        "not_relevant": "A plain calendar or todo app with no retrieval/triage component.",
    },
    "rag-01": {
        "name": "RAG 01",
        "relevant": "Retrieval-augmented generation infrastructure: chunking, "
        "embedding, indexing, retrieve-then-generate pipeline.",
        "not_relevant": "Calling an LLM API with no retrieval step.",
    },
    "uni-tag": {
        "name": "UNI Tag / GEO-AEO",
        "relevant": "llms.txt generation, schema.org markup, agent-readable meta "
        "tags, or measurable AI-search-visibility tooling.",
        "not_relevant": "Generic SEO scripts with no AI-agent-readability angle.",
    },
    "mcp-dev": {
        "name": "AI MCP Dev",
        "relevant": "An MCP server implementation against a real or plausible "
        "client CRM/API surface.",
        "not_relevant": "An MCP 'hello world' with no real tool/resource logic.",
    },
    "inhouse-llm": {
        "name": "In-house LLM",
        "relevant": "Self-hosting/serving an open-source model: inference server, "
        "fine-tuning pipeline, quantization/deployment work.",
        "not_relevant": "A wrapper around a hosted third-party API.",
    },
    "compliance-layer": {
        "name": "Compliance/Trust layer",
        "relevant": "DSGVO/AI Act compliance tooling, audit-trail logic, or "
        "something recognizably built on TWIRA's trust-weighting principle.",
        "not_relevant": "A generic form-validation library.",
    },
    "onboarding": {
        "name": "Onboarding/Training",
        "relevant": "Structured onboarding material generation or tooling tied to "
        "one of the other modules.",
        "not_relevant": "A generic static-site-generator template with no "
        "onboarding-specific content.",
    },
    "verification-layer": {
        "name": "Verification Layer (infra)",
        "relevant": "A PR against this repo itself — applying to work on the "
        "infra rather than a client module.",
        "not_relevant": "Evidence unrelated to verification/trust tooling.",
    },
    "nostr-tracker": {
        "name": "Nostr Time-Tracker (infra)",
        "relevant": "A PR against this repo itself — applying to work on the "
        "infra rather than a client module.",
        "not_relevant": "Evidence unrelated to Nostr-based tracking.",
    },
}


def is_known_module(module_code: str) -> bool:
    return module_code in MODULE_RELEVANCE


def passes_threshold(total: int, dimension_scores: list[int]) -> bool:
    return total >= VERIFIED_THRESHOLD and all(s >= MIN_DIMENSION_SCORE for s in dimension_scores)
