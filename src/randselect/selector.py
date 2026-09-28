def available_choices(items, used):
    """Return items not present in `used`, preserving order."""
    return [item for item in items if item not in used]


def random_selection(n_list, q_list, rng, *, used_names=(), used_questions=()):
    """Pick one random name and one random question via rng.choice().

    rng must expose .choice() (e.g. the `random` module itself, or a
    random.Random(seed) instance) so selection is seedable/testable.
    """
    chosen_name = rng.choice(available_choices(n_list, used_names))
    chosen_question = rng.choice(available_choices(q_list, used_questions))

    return (chosen_name, chosen_question)