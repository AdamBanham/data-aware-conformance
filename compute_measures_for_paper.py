from pmkoalas.models.petrinet import parse_pnml_for_dpn
from pmkoalas.read import read_xes_complex

# import measures
## guard recall measures
from pmkoalas.conformance.dataaware import compute_guard_recall as grec
from deleoni.measure import guard_recall as grecD
from mannhardt.measure import guard_recall as grecM
from felli.cocomot import guard_recall as grecF
grecs = [
    ('grec' , lambda l,m: grec(read_xes_complex(l), parse_pnml_for_dpn(m))),
    ('grecD', grecD),
    ('grecM', grecM),
    ('grecF', lambda l,m: grecF(m,l))
]
## guard precision measures
from pmkoalas.conformance.dataaware import compute_guard_precision as gprec
from mannhardt.measure import guard_precision as gprecF
gprecs = [
    ('gprec', lambda l,m: gprec(read_xes_complex(l), parse_pnml_for_dpn(m))),
    ('gprecM', gprecF)
]


from os.path import join 

WORKING_DIR = join(".", "paper example")

EXAMPLE_MODELS = [
    join(WORKING_DIR, f"paper_example_dpn_{letter}.pnml")
    for letter 
    in ["a","b","c"]
]
EXAMPLE_LOG = join(WORKING_DIR, "paper_example_log.xes")

RERUNS = 10

def find_std(measures):
    from math import sqrt
    mean = sum(measures) / len(measures)
    std = [ (res - mean) ** 2 for res in measures ]
    std = sum(std) / len(std)
    std = sqrt(std)
    return mean,std

def compute_measurements():
    results = {
        'a' : {},
        'b' : {},
        'c' : {}
    }
    for model,label in zip(EXAMPLE_MODELS, ["a", "b", "c"]):
        print(f"running measures over example model {label}...")
        ## compute guard-recall for model and log pair 
        for name,func in grecs:
            measures = []
            for rerun in range(RERUNS):
                measures.append(func(EXAMPLE_LOG, model))
            mean,std = find_std(measures)
            uniques = set(measures)
            print(f"computed measurement for example model {label} for {name} is: ({mean=:.3f},{std=:.3f},{uniques=})")
            results[label][name] = f"({mean=:.3f},{std=:.3f},{uniques=})"
        ## compute guard_recall for model and log pair
        for name,func in gprecs:
            measures = []
            for rerun in range(RERUNS):
                measures.append(func(EXAMPLE_LOG, model))
            mean,std = find_std(measures)
            uniques = set(measures)
            print(f"computed measurement for example model {label} for {name} is: ({mean=:.3f},{std=:.3f},{uniques=})")
            results[label][name] = f"({mean=:.3f},{std=:.3f},{uniques=})"
    print()
    print("*********************************")
    print(str(results).replace("},","}\n"))
    print("*********************************")

if __name__ == "__main__":
    compute_measurements()