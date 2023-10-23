# Conformance Checking for Decision Mining: An Axiomatic Approach

An unpublished evaluation for data-aware process conformance using counter-examples for axioms.
## Abstract

Process mining, a branch of data mining, uses the observed historical 
executions of business processes (as recorded in an event log) to uncover and 
describe their behaviour as a process model. The goal of conformance checking 
is to ensure that the model is of high quality, and is a good representation 
of the event log, thus assuring a solid foundation for subsequent analysis of 
the process. To date, few conformance checking discussions have considered 
model quality beyond what is determined by the execution order of process 
activities. Decision mining aims to uncover rules that guide the execution of 
processes, and hence, to discover overt and tacit decisions that may be 
considered business rules. Decision mining techniques generate data-aware 
models where process activities are annotated with data-driven expressions to 
represent the decision-making of a process. Such models are thus more 
expressive than those that represent only process activities. With the current 
notions of conformance checking, it is unclear what properties determine the 
quality of these data-aware process models.To address this gap, we establish 
qualities for data-aware conformance checking that consider both process 
activities and the data-driven execution described in models, such that we can 
always identify the highest quality model from a collection when given an event 
log. Our major contribution is threefold: i) we present a generalised theory 
focusing on abstracting the representation of data-aware models, ii) using 
this theory we present a set of nine axioms that prescribe desirable properties 
for data-aware conformance checking, and from which, model quality can be 
ascertained, and iii) we define two measures for model recall and precision 
which quantify the quality of data-aware models. Using our set of axioms as 
a yardstick, we compared our proposed recall and precision measures with 
existing measures. Our experimental results show that existing measures 
exhibited limited adherence to our axioms; while, our two proposed measures 
exhibited high adherence to our axioms.

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
testing to be performed. As these techniques are run from a compiled a jar from 
the ProM framework (see the [java folder](java/readme.md) for more information).
In order to rerun these experiements, an executable is required to be compiled as
the python implementation is a little wrapper around the java code used to call
these techniques.

To reperform testing over the counter-examples for guard-recall or guard-precision
techniques, run one of the following python scripts in the root directory after
activting the pipenv shell (`pipenv shell`).
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

### Recomputing measures over paper example

In the root directory, the python script `compute_measures_for_paper.py` when 
run within the pipenv virtual environment will recompute measurements over 
the counter-example in our paper's discussion.

### Paper Example - Series of Counterexamples
Both models and log, used in the paper as the series of counter examples for 
the axioms can be found in the `paper example` directory.

### Model Generation
All models were manually created for each counter-example using ProM and the 
"Edit DPN (Text Language based)" plug-in authored by F.Mannhardt.

### Log Generation
All logs were produced by running the `generate.py` script, more data attributes
then the d1 attribute can be found in the log but are not used in the testing.
