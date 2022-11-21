# Data-Aware Process Conformance:
## Translating Process Conformance Propositions
An unpublished evaluation for data-aware process conformance concerned with the 
decision layer of a process model.


## Abstract

Process conformance measures aim to quantify the quality of a process model 
compared to an event log, in terms of the modelled behaviour and the observed 
behaviour.Governing these measures is a collection of propositions or axioms, 
that clarify the interpretation of measurements between a process model and event logs.
However, these proposition have only considered desirable qualities for process 
conformance measures when considering a language of process activities (a set 
containing sequences of allowable steps focused on process activities) from a 
process model and event log. In this paper, we set out to extend this discussion 
to a more expressive language which  considers the data perspective, choices and 
process activities of a process. We contribute new quality propositions for process 
conformance that aim to include the data perspective of process when comparing a 
process model and an event log. In particular, we focus on quality propositions 
that would allow process conformance to offer a rich comparison of decision mining 
techniques.Finally, we propose two data-aware process conformance measures and 
evaluate our proposed measures alongside existing measures do indeed conform to 
our translated propositions.

## Decision Layer vs Compliance Layer vs Data Perspective

### Decision layer
![decision_layer](./assets/decision_layer_venn.png)

### Compliance Layer
![compliance_layer](./assets/compliance_venn.png)

### Data perspective
![data_perspective](./assets/data_venn.png)
# Evaluation

To run the jupyter notebook for reproducing the testing conducted, ensure that
you use a python 3.9.7 installation and reproduce the a virtual environment using 
pipenv, i.e. pipenv install from the root of this repo. See pipenv for more 
information.

All event logs used in the evaluation (and the script to generate logs) can be 
found in the folder `logs`.
All process models used in the evaluation were generated using ProM and the "Edit 
DPN (Text Language based)" plug-in authored by F.Mannhardt and can be found in
the `models` folder. 