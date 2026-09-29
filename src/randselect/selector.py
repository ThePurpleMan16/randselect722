def available_choices(items, used):
    """Return items not present in `used`, preserving order."""
    return [item for item in items if item not in used]

def random_selection(n_list, q_list, rng=random):

  chosen_name = rng.choice(n_list)
  chosen_question = rng.choice(q_list)

  return (chosen_name, chosen_question)


def selection_without_repeats(n_list, q_list, used_names, used_questions, rng=random):
  # Returns None once either pool has nothing left to draw.
  names = [n for n in n_list if n not in used_names]
  qs = [q for q in q_list if q not in used_questions]

  if not names or not qs:
    return None

  return random_selection(names, qs, rng)
