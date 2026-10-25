# DATA SOURCE & AUTOMATION STATE

## Registered Sources

| Source Name | Type | URL / Endpoint | Status | Sync Interval | Notes |
|---|---|---|---|---|---|
| GitHub Trending & Tech | REST API | `https://api.github.com` | READY | 6 hours | Repositories, topics, stars, licenses |
| Hugging Face Hub | REST API | `https://huggingface.co/api` | READY | 6 hours | Models, datasets, tasks, tags |
| arXiv Computer Science | RSS / API | `http://export.arxiv.org/api/query` | READY | 12 hours | AI, LLM, CS research papers |
| Dev.to Community | REST API | `https://dev.to/api/articles` | READY | 6 hours | Web, Cloud, AI articles |
| International Hackathons | Structured Feeds | Curated Competitions Feed | READY | 12 hours | Verified student competitions |
| Career Gateway Feeds | Structured API | Verified Job Postings API | READY | 12 hours | IT & English internships/freshers |

## Review & Verification Queue
- States: `Pending`, `NeedsVerification`, `Approved`, `Rejected`, `Published`, `Expired`, `Archived`
- Zero fake metrics: All items require verified timestamps, origin URLs, and licensing attributes.
