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
Path from text submission to label:

1. Text arrives at /submit
The user submits a JSON payload containing text and creator_id.
The route extracts those values.

2. Model signal is calculated
detector.model_signal(text) evaluates how predictable the text is using a local language model.
It converts perplexity into a 0-1 score where higher means more likely AI.

3. Style signal is calculated
stylometry.style_signal(text) analyzes the shape of the writing rather than its meaning.
It uses sentence variation, vocabulary diversity, and punctuation patterns to produce a second score.

4. Signals are combined
scoring.combine_signals(model_score, style_score) combines both signals into a single overall score.

5. Score is converted to a decision
scoring.score_to_label(score) converts the numeric score into a classification such as human, unsure, or AI.

6. Decision is logged
The system records the content ID, signal scores, combined score, and decision in the audit log for transparency and future review.

7. Label is returned to the user
The user receives the content ID, signal scores, combined score, classification, and label text.

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

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take the arithmetic mean of the model and style scores. Both
signals count equally; when they disagree, neither can overrule the other, so
the combined score falls between them. A strong split pulls the result toward
the middle rather than producing a confident decision from just one signal.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5` and
`WEIGHT_STYLE_SIGNAL = 0.5` in `config.py`. The unsure band is `0.35–0.65`;
the weighted mean of scores `0.9` and `0.1`, for example, is `0.50`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

Three test pieces run through both signals** (local GPT-2 model signal):

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

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

---

## Stretch Features
A third signal, with a written note on how you weighted the three.


<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

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

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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
