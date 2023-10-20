# Conformance Checking for Decision Mining: An Axiomatic Approach

An unpublished evaluation for data-aware process conformance using counter-examples for axioms.
## Abstract

Process mining, a branch of data mining, uses the observed historical executions 
of business processes (as recorded in an event log) to uncover and describe 
their behaviour as a process model. The goal of conformance checking is to 
ensure that the model is of high quality, and is a good representation of the 
event log, thus assuring a solid foundation for subsequent analysis of the 
process. To date, little conformance checking discussions have considered model 
quality beyond what is determined by the execution order of process activities. 
However, data-aware models that include data to determine what activity should 
occur next at runtime are more expressive than those that represent only 
process activities, which reveals a gap in the current discussion. That is, it 
is unclear, for models that expresses not only the execution order of process 
activities, but includes the data that guide the execution, what properties 
determine the quality of the model. To address this gap, we establish the 
qualities for data-aware conformance checking, which considers process 
activities and the data-driven execution described in models. These qualities 
are directly relevant to decision mining techniques, which annotate process 
activities in models with data-driven expressions to represent the 
decision-making of a process. Our major contribution is threefold: i) we 
present a generalised theory focusing on abstracting the representation of 
data-aware models, ii) using this theory we present a set of nine axioms that 
prescribe desirable properties for data-aware conformance checking, and from 
which, model quality can be ascertained, and iii) we define two measures for 
model recall and precision which quantify the quality of data-aware models.
Using our set of axioms as a yardstick, we compared our proposed recall and 
precision measures with existing measures. Our experimental results showed that 
existing measures exhibited limited adherence to our axioms; while, our two 
proposed measures exhibited high adherence to our axioms.

## Proposed Implementation

Our proposed implementation of guard-recall and guard-precision has been 
introduced in a python library called 
[pmkoalas](https://github.com/AdamBanham/koalas).
However, we have included a static version of our implementation within this
repo in the folder pmkoalas, so that reproduction can be done without the need
of finding an explicit version on pypi.  

To compute guard-recall or guard-precision using our implementation, use
the following snippet.
```python3
from pmkoalas.conformance.dataaware import compute_guard_recall,compute_guard_precision
from pmkoalas.read import read_xes_complex
from pmkoalas.models.petrinet import parse_pnml_for_dpn

log = read_xes_complex(path_to_log)
dpn = parse_pnml_for_dpn(path_to_dpn)

grec = compute_guard_recall(log, dpn)
gprec = compute_guard_precision(log, dpn)
```

## Evaluation

To reproduce the python virtual environment, where we use `pipenv` using 
python 3.11, run `pipenv sync` from the root directory.

This environment has all the python requirements to rerun testing, but testing
for Felli, de Leoni and Mannhardt will require additional attention.

For Felli, see the additional requirements in [this readme](felli/readme.md), 
which includes installing the appropriate binaries for z3 and yices.

For de Leoni and Mannhardt, note that you must have java 8 on path for the 
testing to be performed. As these techniques were extracted as a jar from the 
ProM framework (see the [java folder](java/readme.md) for more information).

To reperform testing over the counter-example for guard-recall or guard-precision
techniques, run one of the following python scripts in the root directory after
activting the pipenv shell (pipenv shell).
 - `py test_proposal.py` to rerun testing against the proposed implementation
    of guard-recall and guard-precision.
 - `py test_felli.py` to rerun testing against the proposed guard-recall 
    measure using the CoCoMoT framework 
 - `py test_deleoni.py` to rerun testing against the existing technique proposed
    by de Leoni as a guard-recall technique.
 -  `py test_deleoni.py` to rerun testing against the existing techniques proposed
    by Mannhardt for a guard-recall and guard-precision technique.

## Historical Execution of Testing

In the root directory, you will find our historical recordings of standard out
for our testing scripts in files with the extension `.stdout'.

### Paper Example - Series of Counterexamples
The models used in the paper as an example of a series of counterexamples for axioms
 can be found in the `paper example` directory.

### Model generation
All models were manually created for each counter-example using ProM and the 
"Edit DPN (Text Language based)" plug-in authored by F.Mannhardt.
