# HELLFIRE AI Solutions — Verification Layer

Наскрізна інфраструктура (не модуль). GitHub-based верифікація фахівців перед допуском у пул виконавців: публічний GitHub-доказ релевантної реалізації модуля/вектора — не резюме, не диплом. Базовий процес (issue → форк → скоуп-ний PR) описаний у [`hellfire-ai/.github`'s CONTRIBUTING.md](https://github.com/HELLFIRE-Solutions/.github/blob/main/CONTRIBUTING.md); цей репозиторій — те, що відбувається *після* мерджу PR: заявка на допуск у пул, оцінка релевантності, синк статусу.

Пов'язано з `internal-db` (сесія 04, статус верифікації) і майбутнім Nostr Time-Tracker (сесія 14, верифікований GitHub-профіль стає першим записом track record). Той самий принцип верифікації (TWIRA — Trust-Weighted Intent Routing з TETA+PI) застосовується і до людей, і до AI-агентів — деталі в [`docs/CRITERIA.md`](docs/CRITERIA.md#same-rubric-human-or-ai).

## Документація

- [`docs/PROCESS.md`](docs/PROCESS.md) — наскрізний процес подачі заявки, 7 кроків від issue в модулі до синку в internal-db.
- [`docs/CRITERIA.md`](docs/CRITERIA.md) — рубрика оцінки (4 виміри, 0–3 кожен, поріг верифікації) + що вважається релевантним для кожного з 8 продаваних модулів.
- [`docs/INTERNAL_DB_SYNC.md`](docs/INTERNAL_DB_SYNC.md) — як і чому синк в `crm.contractors` — тільки UPDATE, без INSERT (немає легітимного джерела `full_name`).
- [`docs/NOSTR_HANDOFF.md`](docs/NOSTR_HANDOFF.md) — контракт даних для сесії 14 (яка ще не почата).
- [`.github/ISSUE_TEMPLATE/verification-submission.yml`](.github/ISSUE_TEMPLATE/verification-submission.yml) — форма заявки.

## Швидкий старт

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,db]"

verification-layer submit octocat gtm-agent \
  https://github.com/HELLFIRE-Solutions/gtm-agent/pull/12 \
  "Implemented HubSpot contact upsert matching architecture.md's integration point" \
  --vector hubspot-integration

verification-layer decide submissions/octocat/gtm-agent.yaml \
  --by bob --relevance 3 --functionality 3 --scope-discipline 3 --originality 2 \
  --notes "Squarely on-vector, ran it locally, scoped PR."

verification-layer list

cp .env.example .env  # DATABASE_URL, тільки для sync-db
verification-layer sync-db submissions/octocat/gtm-agent.yaml
```

`pytest tests/` — 8 тестів (модель + валідація рубрики, YAML store round-trip).

## Свідомі рішення

- **Не автоматизований scoring gate.** `decide` завжди вимагає людину-рев'юєра (`--by`) і нотатки — фіксовано після того, як сесія 11 (compliance-layer) позначила ризик дрейфу у AI Act Annex III (high-risk), якби це стало автоматизованим найм-гейтом без людини в циклі.
- **Файли, не БД, для деталей заявки.** `submissions/*.yaml` — публічний, git-tracked аудиторський слід; `internal-db` отримує лише грубий підсумок (verified/rejected), не деталі скорингу.

**Статус:** Задачі 1–4 з kickoff-промпту виконані (процес, критерії, internal-db синк, nostr-tracker handoff). Не протестовано проти живого Postgres (той самий блокер, що й у internal-db — немає psql/docker на цій машині).

**Ліцензія:** MIT.
