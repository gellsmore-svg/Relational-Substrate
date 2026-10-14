"""Exact stationary coarse words over the committed Generation 8I processes."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache

from rs_constraint_lab.durable import read_json
from rs_constraint_lab.gen008i_exec import decode
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import HistoryError, PRECISION
from rs_constraint_lab.history_roles import aggregate_quotient, role_orbits
from rs_constraint_lab.role_atlas import balance_gap, material_partition

CLOCK = "pair-event epoch"
ORIENTATION = "stationary forward Y^L=(Y_0,...,Y_{L-1})"
LENGTHS = (1, 2, 3, 4, 5, 6)
FLOOR = Decimal("1e-25")


@dataclass(frozen=True)
class ObservedChain:
    rows: tuple[dict[int, Fraction], ...]
    pi: tuple[Fraction, ...]
    observations: tuple

    def validate(self):
        size = len(self.rows)
        if len(self.pi) != size or len(self.observations) != size:
            raise HistoryError("hidden chain dimensions disagree")
        if sum(self.pi) != 1 or min(self.pi) <= 0:
            raise HistoryError("stationary probabilities must be positive and normalised")
        if any(sum(row.values()) != 1 or min(row.values()) <= 0 or
               any(type(target) is not int or not 0 <= target < size for target in row)
               for row in self.rows):
            raise HistoryError("invalid hidden transition row")
        if balance_gap(self.pi, self.rows):
            raise HistoryError("declared initial law is not stationary")


def published_models(root):
    directory = root / "constraint-lab/reports/tables"
    kernels = decode(read_json(directory / "generation-008i-kernels.json"))
    laws = decode(read_json(directory / "generation-008i-stationary-distributions.json"))
    catalog = decode(read_json(directory / "generation-008i-controller-catalog.json"))
    models = {row["controller_id"]: dict(row) for row in catalog}
    for source in (kernels, laws):
        for row in source:
            models[row["controller_id"]].update(row)
    neutral = decode(read_json(directory / "generation-008i-neutral.json"))
    models["I0-NEUTRAL"] = dict(neutral, **neutral["catalog"])
    return models


def rows_from_serial(serial):
    return tuple({int(target): Fraction(value) for target, value in row} for row in serial)


def chains_for(record):
    """Validate the published Kpi and construct its exact material orbit quotient."""
    structure = role_orbits()
    table = pair_classes()
    representatives, groups, class_of = material_partition()
    kpi = rows_from_serial(record["K_pi"])
    marginal = tuple(Fraction(value) for value in record["material"]["pair_mask"])
    if balance_gap(marginal, kpi):
        raise HistoryError("published Kpi is not stationary for published material marginal")
    comparisons = 0
    for masks in structure.mask_maps:
        for source, row in enumerate(kpi):
            transformed = {masks[target]: value for target, value in row.items()}
            if transformed != kpi[masks[source]]:
                raise HistoryError("published Kpi violates S4 covariance")
            comparisons += len(row)
    quotient, gap = aggregate_quotient(kpi, groups, class_of)
    if gap:
        raise HistoryError("Kpi material graph-class quotient invalid")
    class_pi = tuple(sum(marginal[p] for p in group) for group in groups)
    h = ObservedChain(
        rows_from_serial(record["quotient_kernel"]),
        tuple(Fraction(x) for x in record["stationary_orbit_masses"]),
        tuple(table.name_of[group[0] // 6] for group in structure.members),
    )
    current = ObservedChain(
        quotient, class_pi, tuple(table.name_of[p] for p in representatives),
    )
    h.validate()
    current.validate()
    return h, current, {
        "Kpi_S4_covariance_gap": Fraction(0), "Kpi_class_quotient_gap": gap,
        "Kpi_stationary_gap": balance_gap(marginal, kpi),
        "Kpi_covariance_transition_comparisons": comparisons,
        "H_hidden_states": len(h.rows), "Kpi_hidden_states": len(current.rows),
    }


def edge_map():
    table = pair_classes()
    return {table.name_of[p]: p.bit_count() for p in table.representatives}


def complement_class_map():
    table = pair_classes()
    return {table.name_of[p]: table.name_of[p ^ 63] for p in table.representatives}


def edge_chain(chain):
    mapping = edge_map()
    return ObservedChain(chain.rows, chain.pi, tuple(mapping[y] for y in chain.observations))


def sparse_words(chain, depth=6):
    """Forward filtering merges hidden endpoints of each positive observed prefix."""
    chain.validate()
    frontier = defaultdict(dict)
    for state, mass in enumerate(chain.pi):
        frontier[(chain.observations[state],)][state] = mass
    words, counts, work, supports = {}, {}, 0, {}
    for length in range(1, depth + 1):
        words[length] = {word: sum(endpoints.values()) for word, endpoints in sorted(frontier.items())}
        if sum(words[length].values()) != 1:
            raise HistoryError("observed words fail exact normalisation")
        counts[length] = len(frontier)
        supports[length] = {
            "minimum_endpoint_support": min(map(len, frontier.values())),
            "maximum_endpoint_support": max(map(len, frontier.values())),
        }
        if length == depth:
            break
        following = defaultdict(lambda: defaultdict(Fraction))
        for word, endpoints in frontier.items():
            for source, mass in endpoints.items():
                for target, value in chain.rows[source].items():
                    following[word + (chain.observations[target],)][target] += mass * value
                    work += 1
        frontier = following
    return words, {"reachable_words": counts, "forward_updates": work, "role_endpoint_support": supports}


def hidden_path_words(chain, depth=6):
    """Independent recursive hidden-path summation, without prefix endpoint merging."""
    result = {length: defaultdict(Fraction) for length in range(1, depth + 1)}
    visits = 0

    def visit(state, mass, word):
        nonlocal visits
        visits += 1
        result[len(word)][word] += mass
        if len(word) < depth:
            for target, value in chain.rows[state].items():
                visit(target, mass * value, word + (chain.observations[target],))

    for state, mass in enumerate(chain.pi):
        visit(state, mass, (chain.observations[state],))
    return {length: dict(sorted(rows.items())) for length, rows in result.items()}, visits


def project_words(words, mapping):
    result = defaultdict(Fraction)
    for word, mass in words.items():
        result[tuple(mapping[y] for y in word)] += mass
    return dict(sorted(result.items()))


def lumpability(chain):
    groups = defaultdict(list)
    for state, y in enumerate(chain.observations):
        groups[y].append(state)
    block_rows = []
    for row in chain.rows:
        projected = defaultdict(Fraction)
        for target, probability in row.items():
            projected[chain.observations[target]] += probability
        block_rows.append(projected)
    gap, witness = Fraction(0), None
    for label, states in sorted(groups.items()):
        reference = states[0]
        for other in states[1:]:
            for target in sorted(groups):
                a, b = block_rows[reference][target], block_rows[other][target]
                if abs(a - b) > gap:
                    gap = abs(a - b)
                    witness = {"source_observation": label, "source_A": reference,
                               "source_B": other, "target_observation": target,
                               "probability_A": a, "probability_B": b}
    return {"strongly_lumpable": gap == 0, "block_row_gap": gap, "witness": witness}


def decimal_fraction(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


@lru_cache(maxsize=32768)
def log_fraction(value):
    with localcontext() as context:
        context.prec = PRECISION
        return decimal_fraction(value).ln()


def information_term(value, ratio):
    if not value or ratio == 1:
        return Decimal(0)
    return decimal_fraction(value) * log_fraction(ratio)


def word_information(left, right):
    if sum(left.values()) != 1 or sum(right.values()) != 1:
        raise HistoryError("word JS requires normalised laws")
    with localcontext() as context:
        context.prec = PRECISION
        terms = {}
        for word in sorted(left.keys() | right.keys()):
            a, b = left.get(word, Fraction(0)), right.get(word, Fraction(0))
            terms[word] = (information_term(a, 2 * a / (a + b)) +
                           information_term(b, 2 * b / (a + b))) / 2
        return +sum(terms.values()), terms


def conditional_word_information(left, right, mapping):
    a_blocks, b_blocks = project_words(left, mapping), project_words(right, mapping)
    with localcontext() as context:
        context.prec = PRECISION
        result = Decimal(0)
        for word in sorted(left.keys() | right.keys()):
            a, b = left.get(word, Fraction(0)), right.get(word, Fraction(0))
            block = tuple(mapping[y] for y in word)
            ma, mb = a_blocks.get(block, Fraction(0)), b_blocks.get(block, Fraction(0))
            for value, mass in ((a, ma), (b, mb)):
                if value:
                    result += information_term(value, value * (ma + mb) / ((a + b) * mass)) / 2
        return +result


def triple_cmi(triples):
    ab, bc, b = defaultdict(Fraction), defaultdict(Fraction), defaultdict(Fraction)
    for (a, middle, c), mass in triples.items():
        ab[a, middle] += mass
        bc[middle, c] += mass
        b[middle] += mass
    with localcontext() as context:
        context.prec = PRECISION
        result = Decimal(0)
        exact_independent = True
        for (a, middle, c), mass in sorted(triples.items()):
            ratio = mass * b[middle] / (ab[a, middle] * bc[middle, c])
            exact_independent &= ratio == 1
            result += information_term(mass, ratio)
        return {"CMI_lag1": str(+result), "exact_conditional_independence": exact_independent}


def predictive_residual(words, order):
    """A positive gap refutes order r; zero is only this finite-depth check."""
    full = words[order + 2]
    prefix, suffix, suffix_joint = defaultdict(Fraction), defaultdict(Fraction), defaultdict(Fraction)
    for word, mass in full.items():
        prefix[word[:-1]] += mass
        suffix[word[1:-1]] += mass
        suffix_joint[word[1:]] += mass
    gap, witness = Fraction(0), None
    outputs = sorted({word[-1] for word in full})
    for past, normaliser in sorted(prefix.items()):
        for output in outputs:
            word = past + (output,)
            a = full.get(word, Fraction(0)) / normaliser
            b = suffix_joint[word[1:]] / suffix[past[1:]]
            if abs(a - b) > gap:
                gap = abs(a - b)
                witness = {"word": word, "full_conditional": a, "suffix_conditional": b,
                           "positive_prefix_probability": normaliser}
    return {"candidate_order": order, "tested_word_length": order + 2,
            "conditional_row_gap": gap, "witness": witness,
            "reading": "order refuted" if gap else "consistent at tested depth only"}


def word_records(left, right, *, contributions=None):
    result = []
    for word in sorted(left.keys() | right.keys()):
        a, b = left.get(word, Fraction(0)), right.get(word, Fraction(0))
        row = {"word": word, "P_H": a, "P_Kpi": b}
        if contributions is not None:
            row.update(difference=a - b, JS_contribution=str(contributions[word]))
        result.append(row)
    return result


def analyse(record, *, independent=False):
    h, kpi, validation = chains_for(record)
    classes, edges, all_words, triples, diagnostics = [], [], {}, {}, {}
    by_model = {}
    for label, chain in (("H", h), ("Kpi", kpi)):
        class_words, work = sparse_words(chain)
        edge_words = {length: project_words(rows, edge_map()) for length, rows in class_words.items()}
        direct_edges, edge_work = sparse_words(edge_chain(chain))
        if edge_words != direct_edges:
            raise HistoryError("class-word pushforward differs from direct edge-word engine")
        oracle_visits = 0
        if independent:
            oracle, oracle_visits = hidden_path_words(chain)
            if oracle != class_words:
                raise HistoryError("independent hidden-path word cross-check failed")
        by_model[label] = {"graph_class": class_words, "edge_count": edge_words}
        diagnostics[label] = {
            "graph_class": dict(lumpability(chain), **triple_cmi(class_words[3])),
            "edge_count": dict(lumpability(edge_chain(chain)), **triple_cmi(edge_words[3])),
            "work": work, "direct_edge_work": edge_work,
            "independent_hidden_path_visits": oracle_visits,
            "finite_depth": {projection: [predictive_residual(words, order) for order in range(1, 5)]
                             for projection, words in by_model[label].items()},
        }
    process = []
    with localcontext() as context:
        context.prec = PRECISION
        for length in LENGTHS:
            ci, ct = word_information(by_model["H"]["graph_class"][length], by_model["Kpi"]["graph_class"][length])
            ei, et = word_information(by_model["H"]["edge_count"][length], by_model["Kpi"]["edge_count"][length])
            shape = conditional_word_information(by_model["H"]["graph_class"][length], by_model["Kpi"]["graph_class"][length], edge_map())
            gap = abs(ci - ei - shape)
            if gap > FLOOR or ei - ci > FLOOR or min(ci, ei, shape) < -FLOOR:
                raise HistoryError("word information chain/data processing failed")
            process.append({"word_length": length, "I_model_class_word": str(ci),
                            "I_model_edge_word": str(ei), "I_model_class_word_given_edge_word": str(shape),
                            "chain_gap": str(gap)})
            for projection, value in (("graph_class", ci), ("edge_count", ei)):
                a, b = by_model["H"][projection][length], by_model["Kpi"][projection][length]
                equal = a == b
                if length <= 2 and not equal:
                    raise HistoryError("mandatory one/two-time matching failed")
                if (record.get("family") == "B" or record["controller_id"] == "I0-NEUTRAL") and not equal:
                    raise HistoryError("passive-register all-word equality failed")
                row = {"projection": projection, "word_length": length, "reachable_words_H": len(a),
                       "reachable_words_Kpi": len(b), "word_JS": str(value), "exact_equal": equal}
                (classes if projection == "graph_class" else edges).append(row)
                all_words[projection, length] = word_records(a, b)
                if length == 3:
                    triples[projection] = word_records(a, b, contributions=ct if projection == "graph_class" else et)
    validation.update(
        word_normalisation_gap=Fraction(0), class_to_edge_probability_gap=Fraction(0),
        independent_crosscheck_performed=independent, independent_crosscheck_gap=Fraction(0),
        L1_L2_exact_equal=True,
    )
    if not diagnostics["Kpi"]["graph_class"]["strongly_lumpable"]:
        raise HistoryError("Kpi graph-class Markov control failed")
    log_fraction.cache_clear()
    return {
        "controller_id": record["controller_id"], "feature": record.get("feature"),
        "family": record.get("family"), "m": record.get("m"),
        "clock": CLOCK, "orientation": ORIENTATION, "precision_decimal_digits": PRECISION,
        "word_atlas": classes + edges, "process_information": process,
        "diagnostics": diagnostics, "triples": triples, "validation": validation,
        "first_visible_word_length": {
            projection: next((row["word_length"] for row in rows if Decimal(row["word_JS"]) > FLOOR), None)
            for projection, rows in (("graph_class", classes), ("edge_count", edges))
        },
    }, {"clock": CLOCK, "orientation": ORIENTATION, "controller_id": record["controller_id"],
        "words": [{"projection": projection, "word_length": length, "rows": rows}
                  for (projection, length), rows in sorted(all_words.items())]}
