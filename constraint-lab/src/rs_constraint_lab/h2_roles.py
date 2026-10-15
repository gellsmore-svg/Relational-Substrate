"""Ordered depth-two role grammar and exact stationary H1 comparisons.

No scientific cells execute on import. Structural enumeration is parameter-free.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import permutations, product
import json

from flint import ctx, fmpq as Q, fmpq_mat
import mpmath as mp

from rs_constraint_lab.exact import period_of, strongly_connected_components
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import HistoryError
from rs_constraint_lab.state import edges

VERSION = "generation-008m-ordered-h2/v1"
PRECISION = 160
CLOCK = "pair-event epoch"
ctx.threads = 1
mp.mp.dps = PRECISION
PAIRS = tuple(edges(4))
STATES = tuple(product(range(64), range(6), range(6)))
H1_STATES = tuple(product(range(64), range(6)))
SLOT_MAPS = tuple(tuple(PAIRS.index(tuple(sorted((g[a], g[b])))) for a,b in PAIRS)
                  for g in permutations(range(4)))
MASK_MAPS = tuple(tuple(sum(1 << slots[e] for e in range(6) if p >> e & 1)
                        for p in range(64)) for slots in SLOT_MAPS)


def ready(value):
    if isinstance(value, (Q, Fraction)):
        return str(value)
    if isinstance(value, dict):
        return {str(k): ready(v) for k,v in value.items()}
    if isinstance(value, (tuple, list)):
        return [ready(v) for v in value]
    return value


def canonical(value):
    return json.dumps(ready(value), sort_keys=True, separators=(",", ":"))


def fingerprint(value):
    return sha256(canonical(value).encode()).hexdigest()


def relation(a, b):
    if a == b:
        return "SAME"
    return "ADJ" if set(PAIRS[a]) & set(PAIRS[b]) else "DISJ"


def orbit_partition(states, action):
    position = {state:i for i,state in enumerate(states)}
    unseen, blocks = set(states), []
    while unseen:
        representative = min(unseen)
        members = tuple(sorted({action(representative, g) for g in range(24)}))
        if not set(members) <= unseen:
            raise HistoryError("group orbits overlap")
        blocks.append(tuple(position[member] for member in members))
        unseen.difference_update(members)
    lookup = [None] * len(states)
    for b,members in enumerate(blocks):
        for i in members:
            lookup[i] = b
    return tuple(blocks), tuple(lookup)


@cache
def role_structure():
    triples = tuple(product(range(6), repeat=3))
    blocks, lookup = orbit_partition(triples, lambda t,g: tuple(SLOT_MAPS[g][x] for x in t))
    atlas = []
    for i,block in enumerate(blocks):
        h1,h2,e = triples[block[0]]
        descriptor = [relation(h1,h2), relation(h1,e), relation(h2,e)]
        common = set(PAIRS[h1]) & set(PAIRS[h2]) & set(PAIRS[e])
        discriminator = ("STAR" if common else "TRIANGLE") if descriptor == ["ADJ"]*3 else None
        atlas.append({
            "role_id":f"R{i:02d}", "representative":[h1,h2,e],
            "orbit":[triples[j] for j in block], "orbit_size":len(block),
            "rho12":descriptor[0], "rho1e":descriptor[1], "rho2e":descriptor[2],
            "ternary_discriminator":discriminator, "candidate_equals_h1":e==h1,
            "candidate_equals_h2":e==h2, "history_slots_equal":h1==h2,
            "vertex_union":sorted(set(PAIRS[h1]) | set(PAIRS[h2]) | set(PAIRS[e])),
            "existing_controller_membership":[name for name,condition in
                (("RECENT-REVERSAL",e==h1),("SECOND-RECENT",e==h2)) if condition],
        })
    return tuple(atlas), lookup


def role_of(h1,h2,e):
    return role_structure()[1][(h1*6+h2)*6+e]


def state_index(p,h1,h2):
    return (p*6+h1)*6+h2


@cache
def augmented_structure(depth=2):
    states = STATES if depth == 2 else H1_STATES
    def action(t,g):
        return (MASK_MAPS[g][t[0]],) + tuple(SLOT_MAPS[g][h] for h in t[1:])
    return orbit_partition(states, action)


def augmented_atlas():
    blocks,_ = augmented_structure()
    table = pair_classes()
    return [{
        "orbit_id":f"Z{b:03d}", "canonical_state":STATES[block[0]], "orbit_size":len(block),
        "graph_class":table.name_of[STATES[block[0]][0]],
        "edge_count":STATES[block[0]][0].bit_count(),
        "h1_present":bool(STATES[block[0]][0] >> STATES[block[0]][1] & 1),
        "h2_present":bool(STATES[block[0]][0] >> STATES[block[0]][2] & 1),
        "history_relation":relation(STATES[block[0]][1],STATES[block[0]][2]),
        "stabiliser_size":24//len(block), "member_indices":block, "member_hash":fingerprint(block),
    } for b,block in enumerate(blocks)]


@dataclass(frozen=True)
class RoleController:
    role: int
    family: str
    multiplier: str

    def __post_init__(self):
        if type(self.role) is not int or not 0 <= self.role < len(role_structure()[0]):
            raise HistoryError("unknown ordered H2 role")
        if self.family not in ("ANY","FORM","DISSOLVE"):
            raise HistoryError("unknown action family")
        if Q(self.multiplier) <= 0:
            raise HistoryError("positive multiplier required")

    def probabilities(self,p,h1,h2,full=False):
        if type(p) is not int or not 0 <= p < 64:
            raise HistoryError("pair mask out of range")
        for h in (h1,h2):
            if h is not None and (type(h) is not int or not 0 <= h < 6):
                raise HistoryError("history slot must be integer or unavailable")
        if h1 is None and h2 is not None:
            raise HistoryError("invalid sentinel order")
        m = Q(self.multiplier)
        weights = []
        for e in range(6):
            direction = "DISSOLVE" if p >> e & 1 else "FORM"
            selected = (h1 is not None and h2 is not None and role_of(h1,h2,e)==self.role
                        and (self.family=="ANY" or direction==self.family))
            weights.append(m if selected else Q(1))
        if full:
            weights += [Q(1)]*4
        total = sum(weights)
        return tuple(w/total for w in weights)

    def event_rows(self):
        return tuple(self.probabilities(*state) for state in STATES)


def kernel_from_events(events,depth=2):
    states = STATES if depth==2 else H1_STATES
    rows = []
    for state,values in zip(states,events):
        p,i = state[:2]
        row = {}
        for e,value in enumerate(values):
            target = state_index(p ^ (1<<e),e,i) if depth==2 else (p ^ (1<<e))*6+e
            row[target] = value
        if sum(row.values()) != 1 or min(row.values()) <= 0:
            raise HistoryError("positive stochastic row required")
        rows.append(row)
    return tuple(rows)


def quotient(rows,depth=2):
    blocks,lookup = augmented_structure(depth)
    result = []
    for block in blocks:
        expected = None
        for s in block:
            actual = defaultdict(Q)
            for t,w in rows[s].items():
                actual[lookup[t]] += w
            actual = dict(actual)
            if expected is not None and expected != actual:
                raise HistoryError("S4 aggregate row depends on representative")
            expected = actual
        result.append(expected)
    return tuple(result)


def residual(pi,rows):
    incoming = [Q(0)]*len(rows)
    for s,row in enumerate(rows):
        for t,w in row.items():
            incoming[t] += pi[s]*w
    return max(abs(a-b) for a,b in zip(incoming,pi))


def stationary(rows,algorithm="dixon"):
    n = len(rows)
    a = [[Q(int(i==j)) for j in range(n)] for i in range(n)]
    for source,row in enumerate(rows):
        for target,w in row.items():
            a[target][source] -= w
    a[-1] = [Q(1)]*n
    b = fmpq_mat([[int(i==n-1)] for i in range(n)])
    solution = fmpq_mat(a).solve(b,algorithm=algorithm)
    pi = tuple(solution[i,0] for i in range(n))
    if sum(pi)!=1 or min(pi)<=0 or residual(pi,rows):
        raise HistoryError("exact positive stationary solve failed")
    return pi


def lift(masses,depth=2):
    blocks,_ = augmented_structure(depth)
    pi = [Q(0)]*sum(map(len,blocks))
    for mass,block in zip(masses,blocks):
        for s in block:
            pi[s] = mass/len(block)
    return tuple(pi)


def project(pi,labels):
    out = defaultdict(Q)
    for mass,label in zip(pi,labels):
        out[label] += mass
    return dict(sorted(out.items()))


def material_projection(vector):
    table = pair_classes()
    return {"pair_mask":dict(enumerate(vector)),
            "edge_count":project(vector,[p.bit_count() for p in range(64)]),
            "graph_class":project(vector,table.name_of)}


def mpq(q):
    return mp.mpf(int(q.numerator))/int(q.denominator)


@cache
def ln(q):
    return mp.log(mpq(q))


def kl(left,right):
    if left == right:
        return mp.mpf(0)
    return mp.fsum(mpq(a)*ln(a/right[key]) for key,a in left.items() if a)


def js(left,right):
    if left == right:
        return mp.mpf(0)
    terms = []
    for k in left.keys() | right.keys():
        a,b = left.get(k,Q(0)),right.get(k,Q(0))
        if a:
            terms.append(mpq(a)*ln(2*a/(a+b))/2)
        if b:
            terms.append(mpq(b)*ln(2*b/(a+b))/2)
    return mp.fsum(terms)


def number(value):
    return mp.nstr(value,PRECISION)


def distribution_comparison(left,right):
    a,b = material_projection(left),material_projection(right)
    class_counts = {pair_classes().name_of[p]:p.bit_count() for p in range(64)}
    shape_equal = all(a["graph_class"][c]*b["edge_count"][class_counts[c]] ==
                      b["graph_class"][c]*a["edge_count"][class_counts[c]] for c in class_counts)
    density_equal = a["edge_count"] == b["edge_count"]
    classification = ("MATERIAL_SILENT" if a["pair_mask"]==b["pair_mask"] else
                      "DENSITY_ONLY" if shape_equal else "SHAPE_ONLY" if density_equal else "DENSITY_AND_SHAPE")
    total,density = kl(a["graph_class"],b["graph_class"]),kl(a["edge_count"],b["edge_count"])
    conditional = mp.fsum(mpq(a["graph_class"][c])*ln(
        a["graph_class"][c]*b["edge_count"][class_counts[c]] /
        (b["graph_class"][c]*a["edge_count"][class_counts[c]])) for c in class_counts)
    gap = max(abs(total-density-conditional),abs(total-kl(a["pair_mask"],b["pair_mask"])))
    if gap > mp.mpf("1e-25"):
        raise HistoryError("stationary projection chain failed")
    return {"material_class":classification,"pair_equal":left==right,"edge_equal":density_equal,
            "conditional_shape_equal":shape_equal,"KL_pair":number(total),"KL_edge":number(density),
            "KL_shape_given_edge":number(conditional),"JS_pair":number(js(a["pair_mask"],b["pair_mask"])),
            "chain_gap":number(gap),"edge_hash":fingerprint(a["edge_count"]),
            "graph_class_hash":fingerprint(a["graph_class"])}


def stationary_information(pi):
    p = project(pi,[s[0] for s in STATES])
    ph1 = project(pi,[(s[0],s[1]) for s in STATES])
    h1h2 = project(pi,[(s[1],s[2]) for s in STATES])
    h1 = project(pi,[s[1] for s in STATES])
    h2 = project(pi,[s[2] for s in STATES])
    i_p_h1 = mp.fsum(mpq(v)*ln(v/(p[a]*h1[b])) for (a,b),v in ph1.items())
    i_cond = mp.fsum(mpq(v)*ln(v*h1[i]/(ph1[p_,i]*h1h2[i,j]))
                     for (p_,i,j),v in zip(STATES,pi))
    i_joint = mp.fsum(mpq(v)*ln(v/(p[p_]*h1h2[i,j])) for (p_,i,j),v in zip(STATES,pi))
    i_h1h2 = mp.fsum(mpq(v)*ln(v/(h1[i]*h2[j])) for (i,j),v in h1h2.items())
    experienced = mp.fsum(mpq(v)*ln(v*6/ph1[p_,i]) for (p_,i,j),v in zip(STATES,pi))
    if abs(i_joint-i_p_h1-i_cond) > mp.mpf("1e-25"):
        raise HistoryError("history information chain failed")
    return {k:number(v) for k,v in {"I_P_H1":i_p_h1,"I_P_H2_given_H1":i_cond,
            "I_P_H1_H2":i_joint,"I_H1_H2":i_h1h2,
            "experienced_H2_KL_uniform":experienced}.items()}


def covariance_check(events):
    comparisons = 0
    for g,(sm,mm) in enumerate(zip(SLOT_MAPS,MASK_MAPS)):
        for s,(p,i,j) in enumerate(STATES):
            target = events[state_index(mm[p],sm[i],sm[j])]
            if any(events[s][e] != target[sm[e]] for e in range(6)):
                raise HistoryError("generated kernel violates label covariance")
            comparisons += 6
    return comparisons


def analyse_stationary(controller, independent_solve=False):
    events = controller.event_rows()
    rows = kernel_from_events(events)
    covariance = covariance_check(events)
    quotient_rows = quotient(rows)
    orbit_pi = stationary(quotient_rows)
    if independent_solve and stationary(quotient_rows,"fflu") != orbit_pi:
        raise HistoryError("independent fraction-free solve differs")
    pi = lift(orbit_pi)
    if residual(pi,rows):
        raise HistoryError("full 2304-state sparse residual is nonzero")
    components = strongly_connected_components([tuple(row.items()) for row in rows])
    if len(components)!=1 or period_of(components[0],[tuple(row.items()) for row in rows])!=2:
        raise HistoryError("positive-support communicating structure differs")
    material = tuple(sum(pi[state_index(p,i,j)] for i in range(6) for j in range(6)) for p in range(64))
    if any(material[p] != material[mm[p]] for mm in MASK_MAPS for p in range(64)):
        raise HistoryError("stationary material S4 invariance failed")
    ph1 = tuple(sum(pi[state_index(p,i,j)] for j in range(6)) for p,i in H1_STATES)
    ku,kpi = [],[]
    strict_witness = None
    for p,i in H1_STATES:
        local = [events[state_index(p,i,j)] for j in range(6)]
        if strict_witness is None:
            for j in range(1,6):
                if local[j] != local[0]:
                    strict_witness = {"P":p,"h1":i,"h2_A":0,"h2_B":j,"row_A":local[0],"row_B":local[j]}
                    break
        ku.append(tuple(sum(row[e] for row in local)/6 for e in range(6)))
        kpi.append(tuple(sum(pi[state_index(p,i,j)]*local[j][e] for j in range(6))/ph1[p*6+i] for e in range(6)))
    ku,kpi = tuple(ku),tuple(kpi)
    ku_rows,kpi_rows = kernel_from_events(ku,1),kernel_from_events(kpi,1)
    ku_pi = lift(stationary(quotient(ku_rows,1)),1)
    if residual(ku_pi,ku_rows) or residual(ph1,kpi_rows):
        raise HistoryError("H1 comparator stationary residual")
    for p,i in H1_STATES:
        for e in range(6):
            joint = sum(pi[state_index(p,i,j)]*events[state_index(p,i,j)][e] for j in range(6))
            if joint != ph1[p*6+i]*kpi[p*6+i][e]:
                raise HistoryError("Kpi H1 adjacent law does not match")
    marginal_u = tuple(sum(ku_pi[p*6+i] for i in range(6)) for p in range(64))
    if controller.family=="ANY" and material != (Q(1,64),)*64:
        raise HistoryError("history-only uniform-material theorem failed")
    # Column balance of the joint product law is an independent ANY check.
    history = tuple(sum(pi[state_index(p,i,j)] for p in range(64)) for i,j in product(range(6),repeat=2))
    product_pi = tuple(history[i*6+j]/64 for p,i,j in STATES)
    if controller.family=="ANY" and (pi != product_pi or residual(product_pi,rows)):
        raise HistoryError("history-only product stationarity failed")
    result = {
        "controller":{"role":controller.role,"family":controller.family,"m":controller.multiplier},
        "clock":CLOCK,"state_count":2304,"transitions":13824,"orbit_count":len(orbit_pi),
        "kernel_fingerprint":fingerprint(events),"covariance_comparisons":covariance,
        "quotient_kernel":[sorted(row.items()) for row in quotient_rows],
        "stationary_orbit_masses":orbit_pi,"stationary_history_pair":history,
        "stationary_P":material,"stationary_P_H1":ph1,
        "stationary_material_projections":material_projection(material),
        "full_stationary_residual":Q(0),"communicating_classes":1,"period":2,
        "unique_stationary":True,"quotient_exact":True,"stationary_S4_invariant":True,
        "strict_H2":"STRICT_H2" if strict_witness else "H1_COMPILABLE",
        "H1_projection_strong_lumpability":strict_witness is None,"strict_H2_witness":strict_witness,
        "neutral_comparison":distribution_comparison(material,(Q(1,64),)*64),
        "stationary_information":stationary_information(pi),
        "KU_H1":{"event_rows":ku,"stationary_orbit_masses":project(ku_pi,augmented_structure(1)[1]),
                 "stationary_P":marginal_u,"full_stationary_residual":Q(0)},
        "uniform_H1_comparison":distribution_comparison(material,marginal_u),
        "Kpi_H1":{"event_rows":kpi,"stationary_P_H1":ph1,"stationary_residual":Q(0),
                  "one_time_gap":Q(0),"adjacent_law_gap":Q(0)},
        "independent_fraction_free_solve":independent_solve,
    }
    return result,(pi,events,ph1,kpi)
