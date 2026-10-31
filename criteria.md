# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False Positives
<!-- Your criterion. It must name a number. -->
Criterion: Of 10 pieces of writing that I personally wrote without AI assistance, no more than 1 may be labeled high-confidence AI.

**Why this target:**
The biggest harm this system can cause is falsely accusing a real writer. Missing some AI generated content is less harmful than incorrectly labeling human work as AI. This criterion prioritizes protecting legitimate users from false accusations.


---

## 2. Score Spread
<!-- Your criterion. -->
Criterion: The average score for 5 clearly AI generated samples must be at least 0.25 higher than the average score for 5 clearly human-written samples.

**Why this target:**
If both groups receive nearly identical scores, the detector is not providing meaningful information. A noticeable separation demonstrates that the two signals are contributing useful evidence rather than random noise.

---

## 3. Label Coverage
<!-- Your criterion. -->
Criterion: All three labels (human, unsure, and AI) must be reachable. During testing, I must produce at least one example that receives each label.

**Why this target:**
A label that can never be produced indicates a broken threshold configuration. The system was designed with three outcomes, so all three outcomes must actually occur.

---

## 4. Appeal Path
<!-- Your criterion. -->
Criterion: For 100% of valid appeals submitted with an existing content_id:
the appeal is recorded in the audit log, and
the submission status changes to under_review.

**Why this target:**
The appeal process is the user's protection against a false positive. If even one valid appeal is silently lost or fails to change status, the person affected has no practical way to challenge the decision.

---

## 5. Bad Input Handling
<!-- Your criterion. -->
Criterion: For 100% of requests where text is missing, empty, or exceeds the maximum accepted size, the service returns a structured error response and does not crash.

**Why this target:**
Malformed input is common in real systems. The service should fail predictably and provide useful feedback rather than producing a server error or becoming unavailable.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
