# State and quotient diagrams

Generated from synthesis.py. Coordinate/projection/input arrows describe
representation roles, not causal interventions. T arrows denote stochastic
kernels. H and eta are not presumed independent; eta is not executed.

## State Taxonomy

```mermaid
flowchart TB
  X["Ordinary X"]
  H["Historical H"]
  ETA["Candidate constraint eta (not executed)"]
  Z["Augmented represented Z"]
  Y["Raw observation Y"]
  B["Strong refinement block B"]
  BN["Next Markov predictive block"]
  YF["Finer observation"]
  YC["Coarser observation"]
  BF["Fine strong refinement"]
  BC["Coarse strong refinement"]
  X -->|"coordinate"| Z
  H -->|"coordinate"| Z
  ETA -.->|"candidate coordinate"| Z
  Z -->|"phi"| Y
  Z -->|"rho_Y"| B
  B -->|"observation"| Y
  B -->|"quotient kernel"| BN
  YF -->|"coarsening f"| YC
  BF -->|"induced strong quotient"| BC
```

## Predictive Quotient Square

```mermaid
flowchart LR
  ZT["Z_t"]
  ZN["Z_(t+1)"]
  BT["B_t"]
  BN["B_(t+1)"]
  ZT -->|"T"| ZN
  ZT -->|"rho_Y"| BT
  ZN -->|"rho_Y"| BN
  BT -->|"bar-T_Y"| BN
```

## Raw Observation Square

```mermaid
flowchart LR
  ZT["Z_t"]
  ZN["Z_(t+1)"]
  YT["Y_t"]
  YN["Y_(t+1)"]
  ZT -->|"T"| ZN
  ZT -->|"phi"| YT
  ZN -->|"phi"| YN
  YT -.->|"no guaranteed first-order kernel"| YN
```

## History Constraint Roles

```mermaid
flowchart TB
  PAST["Past ordinary trajectory"]
  H["H_t path summary"]
  X["Current X_t"]
  ETA["Candidate eta_t"]
  META["Fixed common meta-programme"]
  LAW["Event law"]
  PAST -->|"summary"| H
  H -->|"input"| LAW
  X -->|"input"| LAW
  ETA -->|"constraint configuration"| LAW
  META -->|"update semantics"| ETA
```

The quotient square asserts T D_rho = D_rho bar-T. The dotted raw
observation arrow does NOT assert the existence of a first-order kernel.
Coarsening of observations induces strong quotient maps by CL-T60/T61.
