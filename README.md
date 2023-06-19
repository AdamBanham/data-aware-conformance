# Data-Aware Process Conformance: Nine Axioms

An unpublished evaluation for data-aware process conformance using counter-examples for axioms.
## Abstract

Process mining studies the observed historical executions (i.e. an event log) of 
business processes to uncover their behaviour. Process conformance metrics aim 
to quantify the quality of a process model compared with an event log, typically 
in terms of described and observed behaviours. Guiding these metrics is a collection 
of propositions, that establish the basis for interpreting conformance measurements 
between a process model and an event log. Existing work on conformance propositions has
studied how to evaluate process conformance metrics against the qualities instilled 
by these propositions. However, much of the existing discussion has only considered 
control-flow aspects of a process. Thus, in this paper, we consider data-aware process 
conformance, which studies how the observed data is used to form expressions. 
To date, there been little discussion of the qualities that a data-aware conformance 
measure should hold. Hence, it is challenging to quantify the quality of data-aware
process models. Therefore, we propose nine quality axioms to trigger a discussion 
on the qualities that should be instilled in data-aware process conformance measures. 
To address these axioms, we evaluate whether our notion of data-aware process
conformance is supported by existing metrics.

## Evaluation

To generate the logs used for counter-examples, create a virtual python environment 
using pipenv and then run the `generate.py` script in the root directory.
All data (logs and models) used as counter-examples for each axiom can be found in 
the `axioms` folder, where for each axiom has a sub folder containing the relevant 
logs and models.
Our record of analysis for all four possible candidiates in the submitted paper 
can be found in the excel spreadsheet `axioms_counter_examples.xlsx`, in the root 
directory.

### Paper Example - Series of Counterexamples
The models used in the paper as an example of a series of counterexamples for axioms
 can be found in the `paper example` directory.

### Model generation
All models were manually created for each counter-example using ProM and the 
"Edit DPN (Text Language based)" plug-in authored by F.Mannhardt.
