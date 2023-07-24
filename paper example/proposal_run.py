from pmkoalas.conformance.dataaware import compute_guard_precision,compute_guard_recall
from pmkoalas.models.petrinet import parse_pnml_for_dpn
from pmkoalas.read import read_xes_complex

from os.path import join 

WORKING_DIR = join(".", "paper example")

EXAMPLE_MODELS = [
    join(WORKING_DIR, f"paper_example_dpn_{letter}.pnml")
    for letter 
    in ["a","b","c"]
]
EXAMPLE_LOG = join(WORKING_DIR, "paper_example_log.xes")

def compute_measurements():
    log = read_xes_complex(EXAMPLE_LOG)
    for model,label in zip(EXAMPLE_MODELS, ["a", "b", "c"]):
        recall = compute_guard_recall(log, parse_pnml_for_dpn(model))
        prec = compute_guard_precision(log, parse_pnml_for_dpn(model))
        print(f"computed measurements for example model {label} are : grec - {recall:.3f} , gprec {prec:.3f}")

if __name__ == "__main__":
    compute_measurements()