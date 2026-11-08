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
   human, scores at or above `0.75` to AI, and the intervening range to unsure.
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
`config.py`. The unsure band is `>0.35` and `<0.75`. With no positive
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
| unsure | >0.35 and <0.75 | We can't tell from these signals whether this text was written by a person or generated by AI. |
| high-confidence AI | 0.75–1.00 inclusive | We think this was probably generated by AI, based on the patterns in the text. This is only an estimate, not proof of authorship. |

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

**Moment 3 — interpreting test results**

- *What I asked for:* I asked the AI assistant to compare my three-trial
  evaluation and full attack runs, connect failures to the route and scoring
  stages, and suggest one measurable improvement rather than changing several
  things at once.
- *What came back:* It highlighted that the score-spread result was reversed
  (AI-reference average `0.5174`, human-reference average `0.6314`) and that six
  human-writing attacks were labelled AI. It suggested raising the AI cutoff
  from `0.65` to `0.75` to move borderline accusations into `unsure`.
- *What I changed:* At my direction, the assistant changed the cutoff and
  helped record the before/after results. I reran the attack and evaluation
  sets: BROKE attacks fell from 23 to 15, with FP02–FP07 moving from AI to
  unsure, but nine of ten evasion attacks still avoided an AI label. I then
  asked it to add route-level bounds for short and oversized submissions; that
  second improvement has not yet been retested.



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

### Second improvement — pre-score submission bounds

The 09:25 attack run showed a one-character submission reaching the model and
returning a 500, while a 60,000-character submission was silently truncated by
the detector and still received an authorship label. I added route-level
validation before either signal runs: text must be at most 2,400 characters
and between 3 and 400 GPT-2 tokens. Short input now gets a structured 400;
oversized input gets a structured 413. This is intended to address MF02 and
MF08 and the oversized-text criterion, without changing valid-text scoring.
I have not rerun the attacks or evaluation after this change; the 09:25 results
above remain the measured baseline, and those outcomes are pending retest.


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
| 1. False positives | No more than 1/10 personally written pieces labelled high-confidence AI | 0/10 AI (synthetic proxy) | 0/10 AI (synthetic proxy) | 0/10 AI (synthetic proxy) | MISSED — invalid sample set |
| 2. Score spread | AI average at least 0.25 above human average | -0.114 (0.517 vs 0.631) | -0.114 (0.517 vs 0.631) | -0.114 (0.517 vs 0.631) | MISSED |
| 3. Label coverage | Reach human, unsure, and AI | All three | All three | All three | MET |
| 4. Appeal path | 100% logged and under_review | 1/1 | 1/1 | 1/1 | MET |
| 5. Bad input | Missing, empty, oversized text return structured errors without a crash | 2/3; oversized accepted | 2/3; oversized accepted | 2/3; oversized accepted | MISSED |

**Before/after evaluation** (full JSON: [before](./results/run_2026-11-08_0910_before.md),
[after](./results/run_2026-11-08_0925_after.md)):

| Criterion | Before | After | Comparison |
|---|---|---|---|
| 1. False positives | 0/10 proxy AI in each trial | 0/10 proxy AI in each trial | Not a valid personal-writing measurement in either run. |
| 2. Score spread | AI 0.5174, human 0.6314; Δ -0.1141 | Same means and delta in all trials | No change; still MISSED. Threshold changes labels, not raw scores. |
| 3. Label coverage | All three labels in every trial | All three labels in every trial | MET in both. |
| 4. Appeal path | 1/1 appeal recorded and under_review in each trial | Not exercised by the 09:25 runner | No after-run comparison; it only submitted text and did not call `/appeal`. |
| 5. Bad input | Missing/empty rejected; 60,000 characters accepted | Same in every trial | No change; still MISSED. |

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


Criterion 1 is MISSED because the inputs were generated proxies, not my own
unaided writing. The 0/10 proxy result cannot establish the false-positive
rate on my work; this is a test-setup limitation, not evidence about a service
stage.

Criterion 2 is MISSED in all three trials: the AI-reference samples averaged
0.5174, below the human-reference average of 0.6314 (target: AI at least 0.25
higher). **Stages: signal one, signal two, and the combining rule.** Signal
one inverted the expected ordering (AI mean 0.5079; human mean 0.7184), while
signal two barely separated the sets (0.5268 versus 0.5444). The normalized
45/45 average therefore left the AI mean lower. This matches the attack-run
pattern where conventional human writing often scores above the AI threshold.

Criterion 3 is MET: human, unsure, and AI were all reached in every trial.
Criterion 4 is MET: all three appeals returned `under_review` and had an
`under_review` appeal event in the audit log.

Criterion 5 is MISSED in all three trials. **Stage: route.** The route rejects
missing and empty text with structured 400 responses, but has no maximum-size
check, so the 60,000-character body reaches scoring and is labelled AI. Signal
one truncates its input to 400 tokens, so that score does not describe the
entire submitted text.

**Broken attacks — stage and mechanism**

- **EV01 — signal one / combining rule:** Typos made the model signal score
  0.1635; the style score was 0.552. Their average was 0.3578, just above the
  human threshold, so the AI text landed in `unsure`.
- **EV02, EV03, EV06, EV07 — signal two / combining rule:** Sentence
  fragmentation, a pasted quotation, uneven sentence lengths, and punctuation
  changed the style measurements (0.4121–0.5376). Averaging them with the
  model scores kept all four AI texts below the AI threshold (`unsure`).
- **EV04 — signal one / combining rule:** Unusual words raised perplexity,
  yielding a 0.6114 model score; the combined score was 0.5749, so the AI text
  was `unsure`.
- **EV05 — both signals / combining rule:** Heavy human editing lowered both
  scores to 0.3212 and 0.4066; the combined 0.3639 result was `unsure`.
- **EV08 — route / signal one / label mapping:** The route accepts text below
  the model's useful token window. The model score was 0.2452 and the combined
  0.3166 crossed the human threshold, so AI text was labelled `human`.
- **EV09 — signal two / combining rule:** The bolted-on human opening created
  disagreement (model 0.7042, style 0.4542); the average 0.5792 was `unsure`.
- **FP02–FP07 — signal one / combining rule / label mapping:** Formal,
  second-language, rubric-shaped, technical, template-like, and repetitive
  human writing produced model scores of 0.7387–0.8816. Style scores
  (0.5055–0.5868) did not counter them; the 45/45 average crossed the 0.65 AI
  threshold for all six.
- **PI02 — signal one / combining rule / label mapping:** The instruction-like
  prefix changed the AI text's predictability; model score 0.2044 and style
  score 0.3843 combined to 0.2944, which the label mapping correctly turned
  into `human` under the 0.35 cutoff.
- **MF02 — route / signal one:** The route accepts a one-character string;
  signal one raises `ValueError` because it has fewer than three tokens. The
  exception is not handled at the route, so the response is a 500 with a
  Werkzeug debugger page.
- **MF03, MF04 — route / signal one / combining rule:** Control characters and
  punctuation-only text are accepted. Signal one returned 0.0000 and 0.0112;
  combined scores 0.1666 and 0.2556 became confident `human` labels despite
  having no meaningful prose to assess.
- **MF05, MF06, MF07 — signal one / combining rule / label mapping:** The
  model signal is not calibrated for a repeated single token, emoji-only
  input, or Arabic text. It returned 0.9976, 0.9969, and 0.9064 respectively;
  the resulting combined scores all crossed the AI threshold.
- **MF08 — route / signal one / combining rule:** The route has no input-size
  limit. Signal one truncates the 60,000-character text to 400 tokens while
  the style signal scores the full input; the combined score 0.8792 is an
  overconfident AI decision on an oversized request.

**Pattern:** Signal one is the common source of both false positives and
evasion: perplexity is being treated as authorship evidence even for unusual,
short, non-English, or formulaic prose. Signal two's simple style measures
are also easy to perturb. The 45/45 combining rule and fixed label cutoffs
turn those noisy signals into confident labels; the route additionally needs
minimum- and maximum-input validation.


---

## The Improvement

**What I changed:** Raised `config.py::AI_THRESHOLD` from `0.65` to `0.75`.
The human cutoff stayed at `0.35`, so the unsure band widened from
`>0.35–<0.65` to `>0.35–<0.75`. This was the only scoring change.

**Which diagnosis pointed at it:** Six human-writing attacks (FP02–FP07)
had combined scores of `0.663–0.705` and were labelled AI. Raising the cutoff
puts those cases into `unsure` instead of making a confident accusation.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Run: [results/attack_run_2026-11-08_0925_after.md](./results/attack_run_2026-11-08_0925_after.md)
(56 attacks). **41 held, 15 broke.**

| Family | Held | Broke | What changed |
|---|---:|---:|---|
| evasion (10) | 1 | 9 | No change: only EV10 was labelled AI; EV01–EV09 remained unsure or human. |
| false_positive (8) | 8 | 0 | FP02–FP07 moved from AI to unsure; FP01 was unsure and FP08 human. |
| prompt_injection (6) | 5 | 1 | No change: PI02 still received a human label. |
| malformed (20) | 15 | 5 | MF06 and MF07 moved from AI to unsure; MF02–MF05 and MF08 still broke. |
| flood_same_creator (12) | 12 | 0 | No change: the 11th and 12th requests were rejected with 429. |

**Before/after attack verdicts** (full runs: [before](./results/attack_run_2026-11-08_0850.md),
[after](./results/attack_run_2026-11-08_0925_after.md)):

| Family | Before HELD/BROKE | After HELD/BROKE | Difference |
|---|---:|---:|---|
| evasion | 1 / 9 | 1 / 9 | No change. |
| false_positive | 2 / 6 | 8 / 0 | Six false-positive attacks moved from AI to unsure. |
| prompt_injection | 5 / 1 | 5 / 1 | No change. |
| malformed | 13 / 7 | 15 / 5 | Two AI labels moved to unsure; the crash and other malformed outcomes remain. |
| flood_same_creator | 12 / 0 | 12 / 0 | No change. |
| **Total** | **33 / 23** | **41 / 15** | **Eight fewer BROKE attacks.** |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

It reduced BROKE attacks from 23 to 15. All six human-writing false positives
were downgraded from AI to unsure, and two malformed inputs were also
downgraded from AI to unsure. That is a useful reduction in confident false
accusations, not proof those samples are human. The trade is visible: the
evasion results did not improve—only one of ten AI evasion samples was labelled
AI, and the other nine still landed in unsure or human. The higher cutoff did
not fix the underlying perplexity/style limitations.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**Attacks still BROKE**

The list below reflects the 09:25 run, before the second improvement in
**Stretch Features**. MF02 and MF08 are the targets of that new validation
change, but I have not reclassified them without a retest.

- **EV01–EV09 (evasion; signals one and two, then combining):** Adversarial
  edits still put AI text in `unsure` or `human`. Next I would calibrate both
  signals against edited variants and abstain when their evidence is weak or
  conflicts. I stopped before changing either signal so the threshold
  experiment remained isolated.
- **PI02 (signal one and label mapping):** The instruction-like prefix raised
  perplexity enough to produce a human-leaning score, which the `0.35` human
  cutoff mapped to `human`. Next I would test prompt-prefixed samples during
  signal calibration and route ambiguous cases to review. I stopped because
  there is no prompt-aware stage in this detector and adding one would be a
  separate change.
- **MF02 (route and signal one):** A one-character body reaches the model,
  which raises an uncaught `ValueError` and returns a 500 debugger page. Next
  I would validate minimum usable input before scoring and return a structured
  400. I stopped to avoid combining route validation with the threshold trial.
- **MF03–MF04 (route, signal one, and combining):** Control characters and
  punctuation-only text are accepted, receive near-zero model scores, and are
  labelled `human`. Next I would reject inputs with no meaningful words or
  return an explicit non-decision. I stopped because this is a separate input
  validation change.
- **MF05 (signal one and combining):** A single repeated character is
  predictable to the model and receives a `0.9976` AI score. Next I would
  calibrate or abstain on extremely repetitive, low-information text. I
  stopped to keep the threshold change as the only intervention.
- **MF08 (route and signal one):** The route accepts 60,000 characters while
  signal one scores only the first 400 tokens. Next I would enforce a maximum
  input size and return a structured error instead of classifying a truncated
  submission. I stopped because that is an independent route change.

**Criteria still MISSED**

- **Criterion 1:** The proxy texts are not my own unaided writing, so this
  cannot measure my false-positive rate. Next I need ten genuine samples; I
  stopped rather than claim generated text as my own.
- **Criterion 2:** The AI-minus-human score difference remains `-0.1141`,
  below the `+0.25` target, before and after the threshold change. Next I would
  calibrate the signals or their weights using labeled examples. I stopped
  because changing signal weights at the same time would make the threshold
  result impossible to isolate.
- **Criterion 5:** Missing and empty text are rejected, but the 60,000-character
  input is accepted and labelled AI. Next I would add route-level size and
  minimum-input checks. I stopped to keep this separate from the threshold
  trial.

Criterion 4 was MET in the before run, but the 09:25 evaluation did not call
`/appeal`, so there is no after-run measurement. I left `run_eval.py` unchanged
and did not claim the appeal result carried over.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I would keep the `0.75` cutoff and err toward protecting writers: the site and
its reviewers pay for more manual reviews and some AI work passing as `unsure`,
rather than writers paying for confident false accusations. That cost is real
here—nine of ten AI evasion attacks still avoided an AI label—so the service
operator bears the missed-detection and review burden.



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
