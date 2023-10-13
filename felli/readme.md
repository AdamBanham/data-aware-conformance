# We do not claim any of the work in this folder to be our own.

We have included a static version of the cocomot framework that was used
to perform our testing of a proposed conformance checking measure, in-line
with other works.

For the most recent version of cocomot, see: https://github.com/bytekid/cocomot

# Proposed Guard Recall

We have lightly touched the work in this folder so that it "runs", though
many other bugs may exist but we don't explore any deeper than needed to get
a working solution.

The following code snippet should be used to call our proposed measure:
```python3
from felli.cocomot import guard_recall
from os.path import join

# filepath to the model
dpn = join(...)
# filepath to the log
log = join(...)
# call function to return a measurement
measurement = guard_recall(dpn, log)

```

# CoCoMoT
Conformance checking of data Petri nets (DPNs) by an SMT encoding.

## Requirements
The script is written for python3, and requires currently the following:
 * yices bindings (https://github.com/SRI-CSL/yices2_python_bindings)
 * Z3 bindings (https://github.com/Z3Prover/z3)
 * pm4py v2.2.19.2 (https://pm4py.fit.fraunhofer.de/)
