# VIAL Foundation Change Proposal

# FCP-004 — VIAL Success Metrics

**Version:** 1.0.0
**Status:** Draft
**Type:** Foundation Change Proposal
Depends On:
- FCP-002A
- FCP-003
**Related:** ADR-0002, VCG-001, TDOC-00 through TDOC-09

---

# 1. Abstract

FCP-004 defines the measurement framework used to determine whether VIAL achieves its architectural objectives.

VIAL SHALL NOT consider an architectural improvement successful merely because it:

* uses fewer agents;
* uses fewer tokens;
* executes faster;
* costs less.

A valid improvement must preserve or improve organizational effectiveness while reducing unnecessary cognitive and operational cost.

The fundamental objective is:

```text
Maximum Organizational Value
        /
Minimum Necessary Cognitive Cost
```

---

# 2. Purpose

This specification establishes measurable criteria for evaluating VIAL implementations.

The metrics SHALL support comparison across:

* different VIAL implementations;
* different models;
* different execution strategies;
* different organization sizes;
* different workloads;
* baseline multi-agent architectures.

---

# 3. Measurement Philosophy

VIAL adopts the following principle:

> An optimization is successful only when it reduces resource consumption without producing unacceptable degradation in organizational capability.

Therefore:

```text
Efficiency ≠ Cost Reduction Alone
```

and:

```text
Performance ≠ Speed Alone
```

---

# 4. Success Dimensions

VIAL success SHALL be evaluated across at least the following dimensions:

```text
1. Cognitive Efficiency
2. Token Efficiency
3. Compute Efficiency
4. Communication Efficiency
5. Decision Quality
6. Context Efficiency
7. Latency
8. Cost
9. Auditability
10. Scalability
11. Reliability
12. Recovery
13. Interoperability
```

---

# 5. Primary Metric Categories

Metrics are divided into:

```text
Primary
Secondary
Diagnostic
```

Primary metrics determine architectural success.

Secondary metrics provide supporting evidence.

Diagnostic metrics help explain performance differences.

---

# 6. Organizational Value

The central evaluation concept is Organizational Value.

Conceptually:

```text
OV =
Task Success
+
Decision Quality
+
Goal Achievement
+
Constraint Compliance
```

The exact calculation SHALL depend on workload.

---

# 7. Cognitive Cost

Cognitive Cost represents the resources consumed to produce organizational cognition.

Conceptually:

```text
CC =
Token Cost
+
Inference Cost
+
Communication Cost
+
Synchronization Cost
+
Validation Cost
+
Memory Cost
```

Not every component must be measured identically.

---

# 8. Cognitive Efficiency

The principal VIAL efficiency metric is:

```text
Cognitive Efficiency = Organizational Value / Cognitive Cost
```

Higher values indicate better efficiency.

---

# 9. Token Consumption

The benchmark SHALL measure:

```text
Input Tokens
Output Tokens
Total Tokens
Repeated Tokens
Context Tokens
Reasoning Tokens
```

where the execution environment exposes such measurements.

---

# 10. Token Redundancy

Token Redundancy measures information unnecessarily transmitted or regenerated.

Conceptually:

```text
Token Redundancy =
Repeated Context Tokens
/
Total Context Tokens
```

The objective is:

```text
Lower is better
```

---

# 11. Context Reuse

Context Reuse measures how often validated organizational information can be reused rather than reconstructed.

Conceptually:

```text
Context Reuse =
Reused Context
/
Total Required Context
```

Higher values indicate better reuse.

---

# 12. Context Efficiency

Context Efficiency measures useful contextual information relative to total contextual information supplied.

```text
Context Efficiency =
Relevant Context
/
Total Context
```

The objective is to maximize relevant information while minimizing unnecessary information.

---

# 13. Communication Efficiency

The benchmark SHALL measure communication overhead between execution resources.

Metrics include:

```text
Messages
Message Tokens
Payload Size
Round Trips
Synchronization Events
Duplicate Messages
```

---

# 14. Communication Redundancy

```text
Communication Redundancy =
Redundant Communication
/
Total Communication
```

Lower is better.

---

# 15. Reasoning Duplication

VIAL SHALL measure unnecessary repetition of equivalent reasoning.

Conceptually:

```text
Reasoning Duplication =
Repeated Reasoning Work
/
Total Reasoning Work
```

This metric is particularly important for comparing VIAL against conventional multi-agent architectures.

---

# 16. Agent Utilization

The benchmark MAY measure:

```text
Agents Activated
Agents Required
Average Active Agents
Idle Agents
Specialized Agents
```

However:

> Fewer agents SHALL NOT automatically be considered better.

The objective is efficient execution, not minimizing agent count.

---

# 17. Model Utilization

The benchmark SHOULD measure:

```text
Model Calls
Tokens per Call
Average Model Size
Reasoning Time
Model Switching
Fallback Calls
```

This enables evaluation of heterogeneous execution strategies.

---

# 18. Deterministic Work Ratio

VIAL SHOULD measure the percentage of operations handled deterministically.

```text
Deterministic Work Ratio =
Deterministic Operations
/
Total Operations
```

A higher ratio MAY indicate efficient avoidance of unnecessary AI inference.

However, this metric SHALL NOT reward inappropriate removal of reasoning.

---

# 19. Decision Quality

Decision Quality is a primary metric.

Depending on the workload, it MAY include:

```text
Accuracy
Precision
Recall
Constraint Compliance
Goal Achievement
Human Evaluation
Task Completion
```

The metric SHALL be workload-specific.

---

# 20. Quality Preservation

Any optimization SHALL be evaluated against a quality baseline.

Conceptually:

```text
Quality Delta =
VIAL Quality
-
Baseline Quality
```

An efficiency improvement accompanied by unacceptable quality degradation SHALL NOT be considered successful.

---

# 21. Quality-Adjusted Efficiency

The recommended comparison metric is:

```text
Quality-Adjusted Efficiency =
Decision Quality
/
Cognitive Cost
```

This prevents token optimization from becoming the sole objective.

---

# 22. Latency

The benchmark SHALL measure:

```text
Time to First Result
Total Execution Time
Decision Latency
State Update Latency
Coordination Latency
```

Where appropriate, measurements SHOULD include:

```text
P50
P95
P99
```

---

# 23. Cost

The benchmark SHOULD calculate total operational cost.

Conceptually:

```text
Total Cost =
Model Cost
+
Compute Cost
+
Storage Cost
+
Network Cost
+
Infrastructure Cost
+
Human Validation Cost
```

---

# 24. Cost per Successful Task

A key economic metric is:

```text
Cost per Successful Task =
Total Cost
/
Successfully Completed Tasks
```

This is preferred over raw cost because a cheaper system that fails more often may be economically inferior.

---

# 25. Energy Efficiency

Where measurement is available, VIAL MAY measure:

```text
Energy per Task
Energy per Decision
Energy per Successful Task
```

This metric becomes increasingly relevant for large-scale deployments.

---

# 26. Auditability

Auditability SHALL be measurable.

Metrics MAY include:

```text
Trace Completeness
Decision Traceability
State Reconstruction Accuracy
Evidence Coverage
Provenance Coverage
Audit Query Latency
```

---

# 27. Trace Completeness

Conceptually:

```text
Trace Completeness =
Auditable Required Events
/
Total Required Events
```

Higher is better.

---

# 28. State Reconstruction

A benchmark SHOULD test whether the organizational state can be reconstructed from the retained information.

Conceptually:

```text
Reconstruction Accuracy =
Correctly Reconstructed State
/
Expected State
```

A system that cannot reconstruct important organizational transitions SHALL receive reduced auditability scores.

---

# 29. Reliability

Reliability metrics SHOULD include:

```text
Successful Executions
Failed Executions
Timeouts
Invalid State Transitions
Protocol Errors
Unexpected Terminations
```

---

# 30. Failure Isolation

The benchmark SHOULD test whether failure of one execution resource affects organizational continuity.

Example:

```text
Agent A fails
        ↓
Organization remains valid
        ↓
Agent B assumes Role
        ↓
Execution continues
```

This is a core TDOC property.

---

# 31. Recovery Time

Measure:

```text
Recovery Time Objective
Recovery Success Rate
State Loss
Context Loss
Decision Loss
```

A successful recovery SHOULD preserve authoritative organizational state.

---

# 32. Scalability

VIAL SHALL be evaluated at increasing organizational workloads.

Example dimensions:

```text
10 tasks
100 tasks
1,000 tasks
10,000 tasks
100,000 tasks
```

The exact scale depends on available infrastructure.

---

# 33. Scaling Efficiency

The benchmark SHOULD evaluate how resource consumption grows as workload increases.

Conceptually:

```text
Scaling Efficiency =
Workload Growth
/
Resource Growth
```

The objective is to avoid disproportionate growth in:

* token consumption;
* communication;
* synchronization;
* memory;
* cost.

---

# 34. Context Scaling

A critical VIAL metric is the relationship between organization size and execution context.

The desired behavior is:

```text
Organization Size ↑
        ↓
Execution Context
does NOT grow proportionally
```

when the task itself remains bounded.

This is one of the central hypotheses of VIAL.

---

# 35. Communication Scaling

Similarly:

```text
Organization Size ↑
        ↓
Communication Overhead
should remain bounded or sublinear
```

where the workload permits.

---

# 36. Audit Scaling

Auditability SHALL also be evaluated at scale.

The system SHOULD avoid:

```text
Audit Cost ∝ Full Context × Every Operation
```

when references and structured provenance can provide equivalent traceability.

---

# 37. Interoperability

Interoperability metrics SHOULD include:

```text
Protocol Compatibility
Schema Compatibility
Cross-Implementation Success
State Exchange Success
Error Interpretation
```

---

# 38. Conformance

Performance SHALL NOT determine protocol conformance.

A system may be:

```text
Fast
but Non-Conformant
```

or:

```text
Slower
but Fully Conformant
```

Conformance and performance are separate dimensions.

---

# 39. Baseline

Every major benchmark SHALL define a baseline.

The baseline SHOULD represent a credible alternative architecture.

Possible baseline categories include:

```text
Single-Agent
Conventional Multi-Agent
Centralized Orchestrator
VIAL
```

The exact baseline SHALL be documented.

---

# 40. Controlled Comparison

Comparisons SHOULD control for:

```text
Same Task
Same Dataset
Same Success Criteria
Equivalent Model Capability
Equivalent Tool Access
Equivalent External Conditions
```

Otherwise, benchmark results may be misleading.

---

# 41. Benchmark Repetition

Results SHOULD be based on multiple executions.

Single-run results SHALL NOT be considered sufficient evidence for important architectural claims.

---

# 42. Statistical Reporting

Benchmarks SHOULD report:

```text
Mean
Median
P95
P99
Standard Deviation
Success Rate
```

where appropriate.

---

# 43. Variance

AI systems may produce variable results.

Therefore, benchmark evaluation SHOULD account for:

```text
Output Variance
Latency Variance
Token Variance
Decision Variance
```

---

# 44. Composite VIAL Score

VIAL MAY define a composite score.

A conceptual model is:

```text
VIAL Score =
Quality
×
Efficiency
×
Reliability
×
Auditability
```

The exact weighting SHALL NOT be finalized in FCP-004.

Weights must be validated experimentally.

---

# 45. No Single-Metric Optimization

VIAL explicitly rejects optimization against a single metric.

For example:

```text
Minimum Tokens
```

is insufficient.

Likewise:

```text
Minimum Latency
```

is insufficient.

A successful implementation must balance:

```text
Quality
Efficiency
Reliability
Governance
Auditability
Cost
```

---

# 46. Pareto Evaluation

VIAL SHOULD use Pareto analysis when comparing architectures.

An implementation may be considered superior when it achieves:

```text
Lower Cost
+
Lower Token Usage
+
Equal or Better Quality
```

without unacceptable degradation in other critical dimensions.

---

# 47. Efficiency Frontier

Benchmark reports SHOULD identify the efficiency frontier.

Example:

```text
             Quality
                ↑
                │       ● VIAL
                │
                │   ●
                │
                │ ● Baseline
                └────────────────→ Cost
```

The objective is not simply minimum cost.

It is the best achievable quality/cost relationship.

---

# 48. Benchmark Workloads

VIAL benchmarks SHOULD eventually include diverse workloads:

```text
Information Retrieval
Planning
Decision Making
Data Validation
Multi-Step Reasoning
Industrial Operations
Monitoring
Incident Response
Knowledge Management
Long-Running Organizations
```

---

# 49. Industrial Workloads

Industrial scenarios SHOULD receive special attention because they provide measurable operational conditions.

Examples:

```text
Production Monitoring
Alarm Analysis
Maintenance Planning
Quality Control
Process Optimization
Resource Allocation
Incident Management
```

These workloads can test VIAL's organizational cognition model under real operational constraints.

---

# 50. Long-Running Organization Test

VIAL SHALL eventually include a long-running benchmark.

The objective is to evaluate whether organizational cognition remains stable over:

```text
Hours
Days
Weeks
```

or longer simulated periods.

Metrics SHOULD include:

```text
Memory Growth
Context Growth
Token Growth
State Consistency
Decision Quality
Audit Integrity
```

---

# 51. Memory Growth

A critical metric is:

```text
Memory Growth Rate
```

The benchmark SHALL investigate whether organizational Memory grows unnecessarily with operational history.

---

# 52. Context Growth

Similarly:

```text
Context Growth Rate
```

SHALL be measured independently from Memory growth.

The desired property is:

```text
Historical Complexity ↑
        ↓
Execution Context
remains bounded when possible
```

---

# 53. Token Growth

The benchmark SHOULD evaluate:

```text
Tokens per Task
```

as organizational history increases.

This directly tests the VIAL hypothesis that persistent organizational cognition can reduce repeated context transmission.

---

# 54. Organizational Continuity

A continuity test SHOULD evaluate whether replacing execution resources affects organizational performance.

Example:

```text
Phase 1
Agent A

        ↓ replacement

Phase 2
Agent B
```

The benchmark compares:

```text
State Continuity
Decision Continuity
Goal Continuity
Memory Continuity
Performance
```

---

# 55. Agent Replacement Test

The system SHOULD pass a continuity test if an execution resource can be replaced without losing authoritative organizational cognition.

---

# 56. Knowledge Reuse

The benchmark SHOULD measure whether previously validated Knowledge can be reused without repeated expensive reasoning.

Conceptually:

```text
Knowledge Created
      ↓
Validated
      ↓
Reused N times
```

Metrics:

```text
Reuse Count
Avoided Inference
Avoided Tokens
Decision Quality
```

---

# 57. Context Cache Effectiveness

Where implementations use context caching, measure:

```text
Cache Hit Rate
Avoided Tokens
Avoided Latency
Invalidation Rate
Stale Context Rate
```

Caching SHALL NOT be considered successful if it causes incorrect decisions through stale information.

---

# 58. Governance Efficiency

Governance itself creates cost.

Therefore measure:

```text
Policy Evaluation Cost
Authorization Cost
Validation Cost
Audit Cost
Escalation Cost
```

The objective is:

```text
Strong Governance
with
Minimal Unnecessary Overhead
```

---

# 59. Human-in-the-Loop Efficiency

When human validation is required, measure:

```text
Human Interventions
Average Review Time
Escalation Rate
Approval Rate
Rejected Decisions
Cost per Human Review
```

---

# 60. Benchmark Integrity

Benchmark implementations SHALL NOT optimize specifically for known benchmark cases in a way that does not generalize.

Benchmark datasets SHOULD include unseen scenarios.

---

# 61. Reproducibility

A benchmark report SHOULD contain:

```text
Implementation Version
Protocol Version
Model Version
Dataset Version
Hardware
Configuration
Parameters
Random Seeds
Workload
Evaluation Method
```

---

# 62. Benchmark Artifact

Each official benchmark SHOULD produce a machine-readable result artifact containing at least:

```text
benchmark_id
implementation
version
workload
configuration
metrics
timestamp
environment
result
```

---

# 63. Minimum Success Criteria

A VIAL implementation SHALL NOT be declared superior solely because of lower resource consumption.

At minimum, a claimed improvement SHOULD demonstrate:

```text
No unacceptable quality degradation
+
Measured efficiency improvement
+
Reproducible result
```

---

# 64. Strategic Success Condition

The ultimate VIAL success condition is:

```text
Higher Organizational Capability
+
Lower Cognitive Waste
+
Lower Operational Cost
+
Greater Auditability
+
Greater Scalability
```

---

# 65. Core VIAL Hypothesis

FCP-004 formalizes the primary architectural hypothesis:

> Organizational cognition can be made more efficient by separating persistent organizational cognition from temporary execution context and by minimizing repeated cognitive work.

This hypothesis SHALL be tested empirically.

---

# 66. Falsifiability

VIAL SHALL allow its own architectural hypotheses to be disproven.

If controlled experiments demonstrate that:

```text
VIAL
```

does not provide measurable advantages over credible alternatives under defined workloads, the architecture SHALL be reconsidered.

Benchmark results SHALL NOT be manipulated to confirm the hypothesis.

---

# 67. Success Matrix

| Dimension        | Metric                | Direction |
| ---------------- | --------------------- | --------- |
| Quality          | Decision Quality      | ↑         |
| Tokens           | Total Tokens          | ↓         |
| Context          | Context Redundancy    | ↓         |
| Reasoning        | Reasoning Duplication | ↓         |
| Communication    | Message Overhead      | ↓         |
| Cost             | Cost/Successful Task  | ↓         |
| Latency          | P95 Latency           | ↓         |
| Reliability      | Success Rate          | ↑         |
| Audit            | Trace Completeness    | ↑         |
| Recovery         | Recovery Success      | ↑         |
| Scalability      | Resource Growth       | ↓         |
| Reuse            | Knowledge Reuse       | ↑         |
| Governance       | Policy Compliance     | ↑         |
| Continuity       | State Preservation    | ↑         |
| Interoperability | Compatibility         | ↑         |

---

# 68. Measurement Priority

When metrics conflict, VIAL SHALL prioritize:

```text
1. Safety
2. Correctness
3. Governance
4. Organizational Capability
5. Reliability
6. Auditability
7. Efficiency
8. Cost
9. Raw Performance
```

Optimization SHALL NOT sacrifice higher-priority properties merely to improve a lower-priority metric.

---

# 69. Relationship to Previous Foundation

The current foundation becomes:

```text
TDOC
 ↓
FCP-002A
 ↓
ADR-0002
 ↓
FCP-003
Design Constraints
 ↓
FCP-004
Success Metrics
```

This preserves the intended progression:

```text
Theory
   ↓
Architecture
   ↓
Constraints
   ↓
Measurement
```

Only after these foundations are established should the protocol design be finalized.

---

# 70. Future Work

FCP-004 prepares the following future specifications:

```text
FCP-005
Efficiency Model

FCP-006
Conformance & Validation

FCP-007
Benchmark Specification
```

The exact numbering of future documents SHALL be confirmed through the project's document registry.

---

# 71. Acceptance Criteria

FCP-004 may be accepted when:

* primary metrics are approved;
* baseline methodology is defined;
* quality criteria are established;
* token measurement is reproducible;
* cost measurement is defined;
* auditability is measurable;
* scalability tests are defined;
* benchmark falsifiability is preserved.

---

# 72. Decision

VIAL SHALL evaluate architectural improvements using measurable, reproducible and multi-dimensional Success Metrics rather than relying on qualitative claims.

---

# 73. Final Principle

The purpose of VIAL is not to create the architecture that uses the fewest tokens.

It is to create the architecture that produces the **highest useful organizational cognition for the lowest necessary total cost**, while remaining:

```text
Auditable
Governable
Reliable
Interoperable
Scalable
Economically Viable
```

---

# End of FCP-004
