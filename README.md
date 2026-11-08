# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->
Path from submission to label:

1. A client sends `POST /submit` with a JSON object containing non-empty
   `text` and `creator_id`. The route rejects invalid JSON or missing values
   before scoring.
2. `detector.model_signal(text)` uses local GPT-2 perplexity to estimate how
   predictable the text is; a higher score means more AI-like.
3. `stylometry.style_signal(text)` measures sentence-length spread,
   type-token ratio, and punctuation density without reading meaning.
4. If `AI201_WATERMARK_KEY` is configured, `watermark.detect_watermark(text)`
   checks for the keyed watermark produced by this project's generator.
   Positive detection adds evidence; a missing or inconclusive watermark is
   reported but is not treated as human evidence.
5. `scoring.combine_signals(...)` takes the weighted mean of the model and
   style scores, plus positive watermark evidence when present.
6. `scoring.score_to_label(combined_score)` maps scores at or below `0.35` to
   human, scores at or above `0.65` to AI, and the intervening range to unsure.
7. The route creates a `content_id` and writes all scores, watermark status,
   guess, and label to the append-only audit log.
8. The JSON response returns the `content_id`, signals, combined score
   (`confidence`), guess, and reader-facing label.

For `POST /appeal`, the writer supplies a prior `content_id` and reasoning.
The route records an `under_review` appeal event beside the original decision;
the audit log preserves the original decision rather than overwriting it.
`GET /log` returns the recorded entries.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Signal One measures predictability. It uses a language model to calculate perplexity, which estimates how surprising the text is to another language model. Text that is easy for the model to predict receives a higher AI score, while text that is harder to predict receives a lower AI score.

**Why that might differ between human and AI writing:**
AI systems generate text by repeatedly selecting likely next words. As a result, AI-generated text is often highly predictable to another language model.

Human writing can contain unusual word choices, unexpected transitions, personal phrasing, and less predictable sentence structures, which may increase perplexity and reduce the AI score.

**What it can't see:**
Predictability is not authorship. Plain human writing can look AI-generated.
A real person may write using simple vocabulary, short sentences, and straightforward language. The detector may classify this as AI-like because it is highly predictable.

### Signal two — the style signal

**What it measures:**
Signal Two measures the statistical shape of the writing.
It analyzes: sentence length variation, vocabulary diversity, punctuation usage
without attempting to understand the meaning of the text.

**Why that might differ between human and AI writing:**
AI-generated writing often trends toward: medium-length sentences, consistent structure, repeated vocabulary.
Human writing is often less regular, with greater variation in sentence lengths and vocabulary choices.

**What it can't see:**
Writing shape is not meaning. Small formatting changes can affect scores without changing the message.
Signal Two cannot understand content or meaning. This signal cannot read. It has no idea what the text says.
A person can alter sentence breaks, punctuation, formatting, or add typos without changing the meaning. Those changes may significantly alter the style score.

### Signal three — the watermark signal

**What it measures:** When configured with `AI201_WATERMARK_KEY`,
`watermark.detect_watermark` checks whether text contains a statistically
unusual share of tokens favored by `watermark.generate` using the matching
secret key. The detector reports a z-score and status. Text below the minimum
length is reported as insufficient evidence.

**Why it might differ between human and AI writing:** A generator that embeds
this watermark deliberately biases token selection according to a keyed,
context-dependent token set. Text produced by that instrumented path may
therefore carry detectable evidence.

**What it can't see:** This only detects our own matching watermark. It cannot
identify output from arbitrary AI systems or GPT-2 text generated without the
watermark. Editing may remove the evidence. “Not detected,” “insufficient
text,” and “not configured” are not proof of human authorship.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Use a weighted mean: model `0.45`, style `0.45`, and positive
watermark evidence `0.10`. A positive watermark detection contributes a score
of `1.0`. If no watermark is detected, the watermark signal is omitted and the
other two weights are normalized, preserving their equal-weight mean. Thus
“not detected,” “insufficient text,” or “not configured” does not lower the
score or count as evidence for human authorship.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.45`,
`WEIGHT_STYLE_SIGNAL = 0.45`, and `WEIGHT_WATERMARK_SIGNAL = 0.10` in
`config.py`. The unsure band is `>0.35` and `<0.65`. With no positive
watermark, scores `0.9` and `0.1` still combine to `0.50`; with a positive
watermark detection, the combined score becomes `0.55`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

Three test pieces run through the model and style signals (local GPT-2 model signal):

1. "The train was late again. I bought a warm pretzel while I waited. By the
   time I got home, it had stopped raining."
2. "I tried to make dinner after work, but I was tired and burned the onions.
   We ordered noodles instead. Honestly, it was a better plan."
3. "Effective communication is essential for successful collaboration. Clear
   goals help teams coordinate their efforts and make informed decisions.
   Regular feedback supports continuous improvement and helps organizations
   achieve better outcomes."

| Test piece | Model signal | Style signal | Combined score |
|---|---:|---:|---:|
| Train and pretzel | 0.6645 | 0.3918 | 0.5282 |
| Dinner after work | 0.4289 | 0.3051 | 0.3670 |
| Conventional formal prose | 0.5394 | 0.5309 | 0.5352 |

The two signals agree on which side of `0.50` the dinner sample and the formal
prose sample fall; they disagree on the train sample. There the model signal
leans AI-like (`0.6645`) while the style signal leans human-like (`0.3918`).
The equal-weight mean is `0.5282`, which lands in the unsure band instead of
letting either signal make a confident claim. These are heuristic scores, not
proof of who wrote any sample.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 inclusive | We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship. |
| unsure | >0.35 and <0.65 | We can't tell from these signals whether this text was written by a person or generated by AI. |
| high-confidence AI | 0.65–1.00 inclusive | We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The unsure label says what the system cannot determine without treating an
uncertain score as an accusation. A person can appeal if the result concerns
their own writing.

**Reachability check:** I submitted these three examples to `POST /submit`.
Each result included `model_score`, `style_score`, and `combined_score` in the
response and decision log.

| Submitted text | Model | Style | Combined | Guess |
|---|---:|---:|---:|---|
| "No. At 4:17 a.m., beneath the sodium lamps, I watched a fox sidle through the vacant lot—its russet coat stippled with rain, its paws soundless on the grit. The kettle shrieked upstairs; my neighbor's window snapped shut. I had forgotten the bread, the appointment, and almost my own name. What a ridiculous, damp little Tuesday!" | 0.3138 | 0.2281 | 0.2710 | human |
| "The afternoon was quiet. I walked to the store and bought a few things. On the way home, a dog barked from a porch. It reminded me of the dog we had when I was little, though I cannot remember its name." | 0.8533 | 0.4222 | 0.6378 | unsure |
| "Artificial intelligence can help people work more efficiently. Artificial intelligence can help people solve problems. Artificial intelligence can help people make decisions. Artificial intelligence can help people learn new things. Artificial intelligence can help people save time. Artificial intelligence can help people achieve better results." | 0.9686 | 0.7139 | 0.8413 | ai |

This verifies that all three label ranges are reachable through the submission
route. The unusual human example is intentionally a test of signal behavior,
not evidence that the scores identify authorship accurately.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence can help people work more efficiently. Artificial intelligence can help people solve problems. Artificial intelligence can help people make decisions. Artificial intelligence can help people learn new things. Artificial intelligence can help people save time. Artificial intelligence can help people achieve better results.", "creator_id": "readme-sample"}'
```

```json
{
  "combined_score": 0.8413,
  "confidence": 0.8413,
  "content_id": "83cdbc55-1c17-4ff8-8406-dcbe3421bba1",
  "guess": "ai",
  "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.",
  "model_score": 0.9686,
  "style_score": 0.7139
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "83cdbc55-1c17-4ff8-8406-dcbe3421bba1", "reasoning": "I wrote this text myself and would like the result reviewed."}'
```

```json
{
  "content_id": "83cdbc55-1c17-4ff8-8406-dcbe3421bba1",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8413,
      "content_id": "83cdbc55-1c17-4ff8-8406-dcbe3421bba1",
      "creator_id": "readme-sample",
      "guess": "ai",
      "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.",
      "model_score": 0.9686,
      "status": "decided",
      "style_score": 0.7139,
      "timestamp": "2026-11-01T13:13:34+00:00"
    },
    {
      "content_id": "83cdbc55-1c17-4ff8-8406-dcbe3421bba1",
      "creator_id": "readme-sample",
      "event": "appeal",
      "reasoning": "I wrote this text myself and would like the result reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-01T13:14:19+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1 — generating calibration samples**

- *What I asked for:* I asked the AI assistant to help create three contrasting
  samples for checking the detector: clearly AI-like prose, clearly human
  prose, and formal human prose. I also used the clearly-AI sample as the base
  for a lightly edited AI example.
- *What came back:* The samples made it possible to run both signals on the
  same text. In this local GPT-2 run, the clearly-AI sample scored
  `model=0.8473`, `style=0.4468`; the clearly-human sample scored
  `0.4978` and `0.3838`; and the formal-human sample scored `0.6497` and
  `0.4991`. The lightly edited variant scored `0.7299` and `0.4557`.
- *What I changed:* I compared the individual signal values instead of
  treating the combined label as ground truth. All four combined results fell
  in the unsure range, so I recorded that limitation and did not claim these
  few generated samples validate detector accuracy.

**Moment 2 — adding a watermark generator and detector**

- *What I asked for:* I asked the assistant to create `watermark.py` with both
  a GPT-2 text generator that embeds a secret-keyed, context-dependent token
  watermark and a detector for that watermark.
- *What came back:* It added a logits processor that biases a keyed subset of
  tokens during generation and a detector that reports the green-token count,
  fraction, and z-score. A 99-token generated continuation was detected with
  the same key (`z=7.0211`); checking with a different key gave `z=0.058` and
  no detection. Text below the configured minimum returns
  `insufficient_text`.
- *What I changed:* I integrated it as optional, positive-only evidence in
  `/submit`. A positive keyed detection contributes `0.10`; negative,
  unavailable, or too-short results are excluded rather than being treated as
  a human signal. I documented that it still needs false-positive and
  editing-robustness testing.

---

## Stretch Features

### Third signal — keyed watermark integration

`watermark.py::generate` uses the project's local GPT-2 model and adds a
small logit bonus to a context-dependent, secret-keyed subset of next tokens.
`watermark.py::detect_watermark` tests text for an excess of those tokens with
a one-sided z-score. `POST /submit` reports `watermark_status`,
`watermark_detected`, `watermark_z_score`, and `watermark_score`. Generation
and detection must use the same secret `AI201_WATERMARK_KEY`; keep it private
and do not commit it.

Try it locally:

```bash
export AI201_WATERMARK_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python watermark.py generate "A short story about a lighthouse" --max-new-tokens 120
python watermark.py detect "paste the generated continuation here"
```

In the local GPT-2 check, a 99-token watermarked continuation scored `z=7.0211`
and was detected with its generation key. A different key scored `z=0.058`
and was not detected. A short passage returned `insufficient_text`, not a
human-like score. This is a controlled prototype: it cannot detect watermarks
from generators using another method, and edits may weaken or remove its
evidence.

I also submitted generated watermarked text through the Flask `/submit` route
with the matching key configured. The response reported
`watermark_status="detected"`, `watermark_z_score=9.0139`, and
`watermark_score=1.0`; its model and style scores were `0.4945` and `0.5211`,
giving a combined score of `0.5570` (unsure). The test verified that the same
fields were written to the audit entry. Without a configured key, the route
reports `watermark_status="not_configured"` and leaves the watermark score
null, so the existing two-signal mean is unchanged.

**How I weighted the three:** `config.py` sets model `0.45`, style `0.45`, and
watermark `0.10`. The `0.10` is included only for a positive detection; when
watermark evidence is unavailable or negative, the other weights are
renormalized to their prior equal-weight average. This conservative policy
keeps lack of a watermark from being mistaken for evidence of human writing.
The z-score is not itself a calibrated authorship probability, so this
weighting needs false-positive and detection-rate evaluation on a
representative labeled test set.


<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 200
  [10/15] 200
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
============================================================

5 of 15 were rate limited. Paste the run above into your README
under **Rate Limiting**, and check GET /log recorded the rejections.

Wrote results/flood_2026-11-04_1929.md
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Run: `results/attack_run_2026-11-08_0850.md` (56 attacks). **33 held, 23 broke.**

| Family | Held | Broke | Notes |
|---|---|---|---|
| evasion (10) | 1 | 9 | Only EV10 (repeated stanza) scored `ai`. EV01–EV09 AI text came back `unsure` (0.36–0.58) or `human` (EV08, 0.317). |
| false_positive (8) | 2 | 6 | FP01 `unsure` and FP08 `human` held. FP02–FP07 human writing labelled `ai` (0.66–0.71). |
| prompt_injection (6) | 5 | 1 | Injected instructions mostly ignored (PI01, 03, 04, 05, 06 `unsure`). PI02 ("SYSTEM: …") got `human` 0.294 on AI text. |
| malformed (20) | 13 | 7 | MF01 and RQ01–RQ12 returned clean `400`. MF02 (single char) broke with a `500` and a Werkzeug debugger page. MF03 and MF04 (junk) scored `human`; MF05, MF06, MF07 (junk, emoji, Arabic) and MF08 (60,000 chars) scored `ai`. |
| flood_same_creator (12) | 12 | 0 | First 10 returned `200`, FL01_11 and FL01_12 returned `429`. |

Broke: EV01–EV09, FP02–FP07, PI02, MF02–MF08.



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "d898312b-78f4-4b30-894b-1468ee905113", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.565, "combined_score": 0.6851, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "6ca0d747-d43d-48f6-a96b-b83c3183a026", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.5798, "combined_score": 0.6901, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "7ece137d-f38e-4d36-a42d-983b9ee4b414", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5276, "combined_score": 0.7046, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "f5f64394-2c51-4bfb-b3d4-418cc564fac8", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.5055, "combined_score": 0.6692, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:00+00:00", "content_id": "233bc65d-3393-4e1d-9495-3cbf108dc0cb", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.552, "combined_score": 0.3578, "label": "We can't tell from these signals whether this text was written by a person or generated by AI.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:01+00:00", "content_id": "7e06922e-346d-48a4-b2d7-0645f5ea5e5d", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.4542, "combined_score": 0.5792, "label": "We can't tell from these signals whether this text was written by a person or generated by AI.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:01+00:00", "content_id": "86817b06-9615-4c46-8029-8da4ac243cb8", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.7622, "combined_score": 0.8707, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "e7d38ce3-ffeb-43e4-9c0c-bb58753e5ef5", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3843, "combined_score": 0.2944, "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "baf94c09-a8d2-4dd6-bca9-edbe08149c99", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.2377, "combined_score": 0.4389, "label": "We can't tell from these signals whether this text was written by a person or generated by AI.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:02+00:00", "content_id": "55383d9f-73ae-4955-943f-3a98710e08c1", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.3333, "combined_score": 0.1666, "label": "We think this was probably written by a person, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:03+00:00", "content_id": "7d5e8b0a-3cc6-4325-92ff-708d5e70f81e", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6667, "combined_score": 0.8321, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:03+00:00", "content_id": "0c3fdfbc-f3d4-467d-9207-4d10e173cd92", "creator_id": "attacker_MF08", "guess": "ai", "model_score": 0.9876, "style_score": 0.7707, "combined_score": 0.8792, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:03+00:00", "content_id": "85102990-ec54-4a14-8e8f-e730acb8065c", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.5, "combined_score": 0.7484, "label": "We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship.", "status": "decided", "watermark_score": null, "watermark_status": "not_configured", "watermark_detected": null, "watermark_z_score": null}
{"timestamp": "2026-11-08T13:50:04+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

Entries, in order: FP03, FP05, FP07, FP04 (human writers called AI);
EV01, EV09 (AI text that evaded to "unsure"); EV10 (held); PI02 (injection
that got a "human" label); PI05 (log-injection, not obeyed); MF03 (control
characters scored "human"); MF05, MF08, MF06 (junk and a 60,000-character
input called AI); and a `429` rejection from the flood rows (FL01_11 — note
it carries only timestamp, creator, reason and limit).

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03** — a non-native English speaker writing carefully about their first
month in a new country was labelled "probably generated by AI" (combined
0.685; the model signal was 0.805). The writer did nothing wrong except use
short, plain, correct sentences, which the perplexity signal reads as
machine-like. Nothing in the label tells them why, and the same pattern hit
FP02, FP04, FP05, FP06 and FP07, so this is systematic: careful, formal, or
second-language writing is the group the detector penalises most.



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | No more than 1/10 personally written pieces labelled high-confidence AI | 0/10 AI (synthetic proxy) | 0/10 AI (synthetic proxy) | 0/10 AI (synthetic proxy) | Not valid: samples are not my own writing |
| 2. Score spread | AI average at least 0.25 above human average | -0.114 (0.517 vs 0.631) | -0.114 (0.517 vs 0.631) | -0.114 (0.517 vs 0.631) | Miss |
| 3. Label coverage | Reach human, unsure, and AI | All three | All three | All three | Pass |
| 4. Appeal path | 100% logged and under_review | 1/1 | 1/1 | 1/1 | Pass |
| 5. Bad input | Missing, empty, oversized text return structured errors without a crash | 2/3; oversized accepted | 2/3; oversized accepted | 2/3; oversized accepted | Miss |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

From `results/run_2026-11-08_0910_before.md`, produced by
`run_eval.py::main` against `app.py::submit` (criterion 5, missing text):

```json
{
  "status": 400,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "invalid_text",
  "message": "text must be a non-empty string.",
  "sent": "{\"creator_id\": \"eval_missing_text\"}"
}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->


The score-spread target missed in all three trials: the AI-reference samples
averaged 0.5174, below the human-reference average of 0.6314. This is the
opposite of the expected separation and matches the false-positive pattern in
the attack run. Criterion 1's synthetic samples all landed in `unsure`, but
that is only a proxy result; it cannot establish the false-positive rate on my
own writing. Label coverage and the appeal path worked in every trial. The
bad-input route returned structured 400 errors for missing and empty text, but
accepted the 60,000-character input and labelled it AI, so it does not meet
the criterion.


---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
