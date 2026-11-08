# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 09:22
- Manually judged: **41 HELD, 15 BROKE**

The script cannot decide whether an evasion worked. The Verdict column below
records a manual HELD or BROKE judgment against each attack's target.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `3c5b3f1c-1218-4c41-b579-5444e4d27636` | unsure | 0.358 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d73e4057-522d-4d03-aab3-cb4bf21d9227` | unsure | 0.503 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `9220be0c-8f1c-47c6-b08c-b63840213a93` | unsure | 0.556 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `d18b0cc6-b885-44ef-81c6-4143823b2c49` | unsure | 0.575 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e658e130-2d08-495a-8816-d26d0b304aef` | unsure | 0.364 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `450099a1-2dfe-4af8-aec1-f6d2e9f08de8` | unsure | 0.529 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `79bcdce1-3bf9-4d48-98fd-3814098bbc9b` | unsure | 0.562 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `80202fed-57fe-487b-9aa7-a915692a667d` | human | 0.317 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `31913d90-8b00-49bd-8ecc-02e2939c69d2` | unsure | 0.579 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `7cca379c-bbf0-4997-a23d-57e27307be89` | ai | 0.871 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `62806af6-16b7-48b0-ab9a-077522ee939a` | unsure | 0.575 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `92c30f89-c37d-466a-8573-83e7f4bebf05` | unsure | 0.663 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `8b523655-8b41-474c-ad6f-16759430a8f0` | unsure | 0.685 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `5ab47878-f8fc-4e29-8865-b467b7606b1c` | unsure | 0.669 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `e9353d7e-2200-4977-9dfd-1ea33b3ad31f` | unsure | 0.690 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `aa669d35-6f95-4aa5-b5f1-5717099e4db3` | unsure | 0.695 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `ea38a2e8-9b1e-4bb3-b424-ede785fd5832` | unsure | 0.705 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `de2cd46f-d08c-4967-b975-5575e2161223` | human | 0.278 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `8bdbdbec-d3a9-45ab-b036-c014b6b59210` | unsure | 0.457 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c634b4ef-838c-47a0-9b5a-8a82420dcbd2` | human | 0.294 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `7debf92b-39fd-49eb-af33-bfd01f949095` | unsure | 0.541 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e65c7e2d-3a53-4a05-bc3e-5cdceedd2ae9` | unsure | 0.425 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `d040554f-361a-4c3e-82c1-e8f4bc34c732` | unsure | 0.439 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `2c8efe75-e6a2-4960-893d-59b380d805ae` | unsure | 0.548 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `a1031e86-0225-4168-a0df-e6c290995152` | human | 0.167 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `67fa155e-421d-4da6-9746-477511407c05` | human | 0.256 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `94dabd3b-8d2b-46b1-8723-c074fb495d28` | ai | 0.832 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `b84d4a42-de40-4d0f-a97b-b190cfe3c1c6` | unsure | 0.748 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `3947fa7d-d4de-43c8-a46b-724a3e6e4723` | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `2778145e-4099-45fd-82cd-a4e16f6c4890` | ai | 0.879 | BROKE |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f804b360-1552-4438-88cc-19d16627499f` | human | 0.287 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c9d82b25-01bf-4988-a014-8080bfe70eed` | human | 0.287 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dd58e4ea-5628-4866-a903-6280fa612ff4` | human | 0.287 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bfb561d0-6f68-4634-88c0-22f96faf8993` | human | 0.287 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `14d6f555-2d67-4fdd-9a93-937850e19007` | human | 0.287 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d13912c8-ece8-4a90-81ca-800fb3a9f365` | human | 0.287 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ab65a80d-2885-482e-abaa-ba2314815beb` | human | 0.287 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `096faf55-d79a-40d9-9051-b424b69c652d` | human | 0.287 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c454ea4-1897-4325-8060-f71d5fda441b` | human | 0.287 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f6877acf-444d-4dbe-bc15-a3299cb5494b` | human | 0.287 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---:|---:|---:|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 8 | 0 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 15 | 5 |
| `prompt_injection` | 6 | 5 | 1 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "3c5b3f1c-1218-4c41-b579-5444e4d27636",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3578,
  "model_score": 0.1635,
  "style_score": 0.552,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "d73e4057-522d-4d03-aab3-cb4bf21d9227",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5032,
  "model_score": 0.5943,
  "style_score": 0.4121,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "9220be0c-8f1c-47c6-b08c-b63840213a93",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5559,
  "model_score": 0.6662,
  "style_score": 0.4457,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "d18b0cc6-b885-44ef-81c6-4143823b2c49",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5749,
  "model_score": 0.6114,
  "style_score": 0.5383,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "e658e130-2d08-495a-8816-d26d0b304aef",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3639,
  "model_score": 0.3212,
  "style_score": 0.4066,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "450099a1-2dfe-4af8-aec1-f6d2e9f08de8",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5292,
  "model_score": 0.5727,
  "style_score": 0.4858,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "79bcdce1-3bf9-4d48-98fd-3814098bbc9b",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5619,
  "model_score": 0.5862,
  "style_score": 0.5376,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "80202fed-57fe-487b-9aa7-a915692a667d",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3166,
  "model_score": 0.2452,
  "style_score": 0.388,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "31913d90-8b00-49bd-8ecc-02e2939c69d2",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5792,
  "model_score": 0.7042,
  "style_score": 0.4542,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "7cca379c-bbf0-4997-a23d-57e27307be89",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8707,
  "model_score": 0.9792,
  "style_score": 0.7622,
  "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "62806af6-16b7-48b0-ab9a-077522ee939a",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5746,
  "model_score": 0.6175,
  "style_score": 0.5317,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "92c30f89-c37d-466a-8573-83e7f4bebf05",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6628,
  "model_score": 0.7387,
  "style_score": 0.5868,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "8b523655-8b41-474c-ad6f-16759430a8f0",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6851,
  "model_score": 0.8051,
  "style_score": 0.565,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "5ab47878-f8fc-4e29-8865-b467b7606b1c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6692,
  "model_score": 0.8329,
  "style_score": 0.5055,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e9353d7e-2200-4977-9dfd-1ea33b3ad31f",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6901,
  "model_score": 0.8005,
  "style_score": 0.5798,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "aa669d35-6f95-4aa5-b5f1-5717099e4db3",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6952,
  "model_score": 0.8814,
  "style_score": 0.5091,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "ea38a2e8-9b1e-4bb3-b424-ede785fd5832",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7046,
  "model_score": 0.8816,
  "style_score": 0.5276,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "de2cd46f-d08c-4967-b975-5575e2161223",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2775,
  "model_score": 0.3223,
  "style_score": 0.2326,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "8bdbdbec-d3a9-45ab-b036-c014b6b59210",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4572,
  "model_score": 0.4625,
  "style_score": 0.4519,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c634b4ef-838c-47a0-9b5a-8a82420dcbd2",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2944,
  "model_score": 0.2044,
  "style_score": 0.3843,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "7debf92b-39fd-49eb-af33-bfd01f949095",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5412,
  "model_score": 0.5943,
  "style_score": 0.488,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "e65c7e2d-3a53-4a05-bc3e-5cdceedd2ae9",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4255,
  "model_score": 0.4998,
  "style_score": 0.3511,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "d040554f-361a-4c3e-82c1-e8f4bc34c732",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4389,
  "model_score": 0.6401,
  "style_score": 0.2377,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "2c8efe75-e6a2-4960-893d-59b380d805ae",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.548,
  "model_score": 0.5583,
  "style_score": 0.5376,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "a1031e86-0225-4168-a0df-e6c290995152",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.1666,
  "model_score": 0.0,
  "style_score": 0.3333,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "67fa155e-421d-4da6-9746-477511407c05",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "94dabd3b-8d2b-46b1-8723-c074fb495d28",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8321,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "b84d4a42-de40-4d0f-a97b-b190cfe3c1c6",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.7484,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "3947fa7d-d4de-43c8-a46b-724a3e6e4723",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell from these signals whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "2778145e-4099-45fd-82cd-a4e16f6c4890",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8792,
  "model_score": 0.9876,
  "style_score": 0.7707,
  "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "f804b360-1552-4438-88cc-19d16627499f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c9d82b25-01bf-4988-a014-8080bfe70eed",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "dd58e4ea-5628-4866-a903-6280fa612ff4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "bfb561d0-6f68-4634-88c0-22f96faf8993",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "14d6f555-2d67-4fdd-9a93-937850e19007",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "d13912c8-ece8-4a90-81ca-800fb3a9f365",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "ab65a80d-2885-482e-abaa-ba2314815beb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "096faf55-d79a-40d9-9051-b424b69c652d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "1c454ea4-1897-4325-8060-f71d5fda441b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "f6877acf-444d-4dbe-bc15-a3299cb5494b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2871,
  "model_score": 0.0287,
  "style_score": 0.5455,
  "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
