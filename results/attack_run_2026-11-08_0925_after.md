# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 09:25
- Manually judged: **41 HELD, 15 BROKE**

The script cannot decide whether an evasion worked. The Verdict column below
records a manual HELD or BROKE judgment against each attack's target.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `0141e7b3-99ae-4d91-ad9e-57096e23c91e` | unsure | 0.358 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `9ea9618b-e098-4663-b191-b25886945fa2` | unsure | 0.503 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `77d0dee8-650b-4a53-8f78-61f1aac64ac0` | unsure | 0.556 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a591a672-4be8-4c0d-a0d3-6432fc33c5d6` | unsure | 0.575 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `15a0a1cd-cd1e-4aad-81ca-46021a09f88f` | unsure | 0.364 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `eb42fad2-079f-42c2-a93a-628c9e00f4d5` | unsure | 0.529 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `0c1079db-e4fb-4dc2-8c72-ae49a0420d26` | unsure | 0.562 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `e98a0f86-9d81-4a21-aa91-4d207a94dc4e` | human | 0.317 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6ffc0182-789a-4375-b6f1-ffcc30b7f936` | unsure | 0.579 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `cfd2d9ae-4a08-4fb5-974e-494d8ba77401` | ai | 0.871 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `8053a4ec-85c3-4c31-ae52-dc5eb4745121` | unsure | 0.575 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `f72d6b45-4509-43a7-bf76-eaf6b80a16d1` | unsure | 0.663 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `4fc8d4fc-67ec-40d5-9a46-9a062cc4a215` | unsure | 0.685 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `70023504-7861-475d-b21c-abfb94cadddb` | unsure | 0.669 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `4ecd0b11-757d-4c7e-9581-84bdf1b08614` | unsure | 0.690 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `2919a282-e4e1-41aa-933e-d0e49ed1e086` | unsure | 0.695 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `0fe1f3a3-6aa9-4afa-85a1-184edce37b3a` | unsure | 0.705 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `61d39481-1175-4c41-8983-4539280866f4` | human | 0.278 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `480e5df5-c411-4971-985a-835ca718e63b` | unsure | 0.457 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cd2d61c7-68bf-40da-8944-92b02989c966` | human | 0.294 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `503cc41e-3338-4efc-8e2d-b442262670ee` | unsure | 0.541 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4396603d-a1bd-4e61-a8b0-90ef9d487738` | unsure | 0.425 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `14205000-cff5-446e-8193-2a31fbccc6bd` | unsure | 0.439 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4e4a4200-401b-4885-ac07-c2726b7cbb68` | unsure | 0.548 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `40d3306f-c13a-4f63-8d04-928c17e93afb` | human | 0.167 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `79d42d17-4035-44f6-964f-65a3f9bc4cb5` | human | 0.256 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `0bb866cd-d074-400d-ad78-65afd5a04e80` | ai | 0.832 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `edda05ba-0ba8-4503-99f3-9d9c17217f52` | unsure | 0.748 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `4751e4e2-cf40-49a5-8fb8-1cc06d911275` | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `0a008c48-2829-4852-9ecd-1a6421b7aa80` | ai | 0.879 | BROKE |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6dfa58c1-b6d1-4c92-a061-498c196264a7` | human | 0.287 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6c810472-2faa-4346-bcb4-54ff11db76d7` | human | 0.287 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b313f0a6-5c2b-4fca-b176-7aa31bbcfa79` | human | 0.287 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2aad8519-0d33-4ece-97a8-e1dbf5514518` | human | 0.287 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e825dc8b-8204-4e3f-ade4-fa9b54e83d6d` | human | 0.287 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0708d6ee-75c0-4d83-ae0c-a614b7849f69` | human | 0.287 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3f36e363-bb95-44da-9bf1-b8fac4b5ba92` | human | 0.287 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `753cb55d-8c15-4c75-933d-9f224e673142` | human | 0.287 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `97a4b5da-bf74-4424-9597-c29645e41ecb` | human | 0.287 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7da123c1-e5cf-49ce-9782-e92ae016679a` | human | 0.287 | HELD |
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
  "content_id": "0141e7b3-99ae-4d91-ad9e-57096e23c91e",
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
  "content_id": "9ea9618b-e098-4663-b191-b25886945fa2",
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
  "content_id": "77d0dee8-650b-4a53-8f78-61f1aac64ac0",
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
  "content_id": "a591a672-4be8-4c0d-a0d3-6432fc33c5d6",
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
  "content_id": "15a0a1cd-cd1e-4aad-81ca-46021a09f88f",
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
  "content_id": "eb42fad2-079f-42c2-a93a-628c9e00f4d5",
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
  "content_id": "0c1079db-e4fb-4dc2-8c72-ae49a0420d26",
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
  "content_id": "e98a0f86-9d81-4a21-aa91-4d207a94dc4e",
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
  "content_id": "6ffc0182-789a-4375-b6f1-ffcc30b7f936",
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
  "content_id": "cfd2d9ae-4a08-4fb5-974e-494d8ba77401",
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
  "content_id": "8053a4ec-85c3-4c31-ae52-dc5eb4745121",
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
  "content_id": "f72d6b45-4509-43a7-bf76-eaf6b80a16d1",
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
  "content_id": "4fc8d4fc-67ec-40d5-9a46-9a062cc4a215",
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
  "content_id": "70023504-7861-475d-b21c-abfb94cadddb",
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
  "content_id": "4ecd0b11-757d-4c7e-9581-84bdf1b08614",
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
  "content_id": "2919a282-e4e1-41aa-933e-d0e49ed1e086",
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
  "content_id": "0fe1f3a3-6aa9-4afa-85a1-184edce37b3a",
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
  "content_id": "61d39481-1175-4c41-8983-4539280866f4",
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
  "content_id": "480e5df5-c411-4971-985a-835ca718e63b",
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
  "content_id": "cd2d61c7-68bf-40da-8944-92b02989c966",
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
  "content_id": "503cc41e-3338-4efc-8e2d-b442262670ee",
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
  "content_id": "4396603d-a1bd-4e61-a8b0-90ef9d487738",
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
  "content_id": "14205000-cff5-446e-8193-2a31fbccc6bd",
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
  "content_id": "4e4a4200-401b-4885-ac07-c2726b7cbb68",
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
  "content_id": "40d3306f-c13a-4f63-8d04-928c17e93afb",
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
  "content_id": "79d42d17-4035-44f6-964f-65a3f9bc4cb5",
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
  "content_id": "0bb866cd-d074-400d-ad78-65afd5a04e80",
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
  "content_id": "edda05ba-0ba8-4503-99f3-9d9c17217f52",
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
  "content_id": "4751e4e2-cf40-49a5-8fb8-1cc06d911275",
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
  "content_id": "0a008c48-2829-4852-9ecd-1a6421b7aa80",
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
  "content_id": "6dfa58c1-b6d1-4c92-a061-498c196264a7",
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
  "content_id": "6c810472-2faa-4346-bcb4-54ff11db76d7",
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
  "content_id": "b313f0a6-5c2b-4fca-b176-7aa31bbcfa79",
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
  "content_id": "2aad8519-0d33-4ece-97a8-e1dbf5514518",
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
  "content_id": "e825dc8b-8204-4e3f-ade4-fa9b54e83d6d",
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
  "content_id": "0708d6ee-75c0-4d83-ae0c-a614b7849f69",
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
  "content_id": "3f36e363-bb95-44da-9bf1-b8fac4b5ba92",
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
  "content_id": "753cb55d-8c15-4c75-933d-9f224e673142",
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
  "content_id": "97a4b5da-bf74-4424-9597-c29645e41ecb",
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
  "content_id": "7da123c1-e5cf-49ce-9782-e92ae016679a",
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
