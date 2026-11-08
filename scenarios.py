"""
Inputs for the five acceptance criteria in criteria.md.

Criterion 1's inputs below are synthetic human-style proxies, not the user's
own unaided writing. Replace them with personal writing before treating that
criterion's result as a valid false-positive measurement.
"""

import csv
from pathlib import Path


_ATTACKS_PATH = Path(__file__).parent / "attack_set" / "attacks.csv"
with _ATTACKS_PATH.open(encoding="utf-8", newline="") as _attack_file:
    _ATTACKS = {row["id"]: row["text"] for row in csv.DictReader(_attack_file)}


def _attack_texts(*ids: str) -> list[str]:
    return [_ATTACKS[attack_id] for attack_id in ids]


SCENARIOS = [
    {
        "name": "criterion 1 synthetic human-style proxy (not personal writing)",
        "criterion": 1,
        "texts": [
            "I missed the bus by less than a minute, so I walked to the next stop and waited there. The morning was cold, but the bakery on the corner had just opened. I bought a roll and arrived at work with enough time to make tea.",
            "The library moved the returns desk near the front doors last month. It is easier to find now, although the queue gets in the way when school lets out. I still like the quieter tables upstairs, especially on rainy afternoons.",
            "We planted tomatoes in the small bed behind the garage. The first few leaves looked pale, so I moved the pots into the sun and watered them less often. They are doing better now, and one plant has its first yellow flower.",
            "My sister called while I was making soup and asked for the recipe. I had never written it down, so I tried to explain the amounts from memory. It came out a little different this time, but everyone had seconds.",
            "The train ride takes about forty minutes if there are no delays. I usually bring a book, though I spend more time looking out the window than reading. There is a stretch beside the river where the light changes in a lovely way.",
            "I sorted the drawer of cables on Sunday and found three chargers for devices I no longer own. The useful ones went into a small box by the desk. I recycled the rest and finally had room for the batteries.",
            "At the market, a man was selling pears from a wooden cart. I chose a few that were still firm because I wanted them for the week. They ripened on the counter, and the last one was sweet enough to eat over the sink.",
            "The repair took longer than expected because the replacement part did not fit the first time. The mechanic showed me the worn piece and explained what had happened. I appreciated the explanation, even though it meant coming back the next day.",
            "I started taking a short walk after lunch instead of checking my phone at my desk. Some days I only go around the block, but it helps me reset before the afternoon meetings. I have noticed more gardens on the route than I expected.",
            "The old notebook has a bent cover and a coffee stain on the first page. I keep it because it holds a list of places we visited on our first road trip. A few names are hard to read now, but I remember the long drive and the roadside peaches.",
        ],
    },
    {
        "name": "score spread: AI and human reference samples",
        "criterion": 2,
        "texts": [
            "Effective planning helps teams use their time and resources wisely. Before beginning a project, members should agree on its goals, identify the tasks involved, and decide who will complete each one. A clear schedule makes progress easier to monitor and gives the group an opportunity to address delays early. Regular communication also helps ensure that everyone understands how their work contributes to the final result.",
            "Public parks provide important benefits to people living in cities. They offer space for exercise, recreation, and contact with nature, while also creating places where neighbors can meet. Trees and planted areas can improve the appearance of a neighborhood and provide shade during hot weather. Maintaining these spaces requires ongoing investment, but accessible parks can improve daily life for residents of many ages.",
            "Learning a new skill takes patience and consistent effort. Beginners often make mistakes because they are still developing the habits and knowledge needed to perform well. Breaking a large goal into smaller steps can make improvement easier to track. Feedback from others is useful when it is specific and timely, and repeated practice helps turn new techniques into reliable abilities.",
            "Good communication is essential when people work toward a shared objective. Participants need to exchange relevant information, listen carefully, and clarify points that may be misunderstood. Written records can preserve decisions and make responsibilities clear. When concerns are raised early, a group has more time to consider alternatives and adjust its plans before small difficulties become larger problems.",
            "Household energy use can be reduced through a combination of practical changes. Sealing gaps around doors and windows helps maintain indoor temperatures, while efficient appliances use less electricity to perform everyday tasks. People can also compare their usage over time to identify patterns and set realistic goals. These steps may lower utility costs while reducing demand on the wider energy system.",
            "We got to the campsite about four. The pitch was fine, a bit sloped, but there was a tap nearby and the toilets were clean enough. Putting the tent up took longer than it should have because I had forgotten how the poles went. The weather held until Saturday night, when the rain came in sideways and woke us all up.",
            "This report sets out the findings of the working group. The group met four times between January and March. Its remit was to review the current arrangements and to recommend changes where these were warranted. The group found that the existing arrangements are generally effective, although some responsibilities could be made clearer.",
            "I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and they helped me to find an apartment. I am still learning the way people speak here, but each week feels a little easier.",
            "To configure the service, edit the settings file in the installation directory. Set the host value to the address the service should bind to. Set the port value to an unused port above 1024. Save the file and restart the service. The service will log its startup status and report any configuration errors.",
            "Dear Sir or Madam, I am writing to enquire about the position advertised on your website. I have five years of relevant experience and I believe I would be a strong fit for the role. I have attached my curriculum vitae for your consideration. I am available for an interview at a time convenient to you.",
        ],
    },
    {
        "name": "label coverage across low, middle, and high score inputs",
        "criterion": 3,
        "texts": _attack_texts("FP08", "EV01", "EV09", "EV10"),
    },
    {
        "name": "appeal path: submit then appeal and verify audit event",
        "criterion": 4,
        "appeal": {
            "reasoning": "This is my own work. Please have a person review the decision.",
        },
        "texts": [
            "I took the longer route home because the main road was closed for repairs. The detour passed a small park where children were playing near the fountain. By the time I reached my street, the sky had cleared and the evening felt much warmer.",
        ],
    },
    {
        "name": "bad input: missing, empty, and oversized text",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_missing_text"},
            {"text": "", "creator_id": "eval_empty_text"},
            {"text": "word " * 12000, "creator_id": "eval_oversized_text"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not isinstance(text, str) or not text.strip():
                problems.append(
                    f"scenario {i}, text {j} is empty or not a string"
                )

        if scenario.get("appeal") and not isinstance(scenario["appeal"], dict):
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has an invalid appeal config"
            )
    return problems
