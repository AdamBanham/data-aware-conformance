from unpublished.measures import reasoning_recall, reasoning_precision

from os.path import join 
from math import sqrt

AXS_FOLD = join(".", "axioms")
AX_3_FOLD = join(AXS_FOLD, "axiom 3")
AX_3_LOG = join(AX_3_FOLD, "log_1.xes")
AX_3_MODELS = [ 
    join(AX_3_FOLD, f"ax3_model_{i}.pnml")
    for i 
    in range(1,6)
]
AX_4_FOLD = join(AXS_FOLD, "axiom 4")
AX_4_LOG = join(AX_4_FOLD, "log_1.xes")
AX_4_MODEL = join(AX_4_FOLD, "ax4_model_1.pnml")
AX_6_FOLD = join(AXS_FOLD, "axiom 6")
AX_6_MODEL = join(AX_6_FOLD, "ax6_model_1.pnml")
AX_6_LOGS = [ 
    join(AX_6_FOLD, f"log_{i}.xes")
    for i 
    in range(1,4)
]
AX_7_FOLD = join(AXS_FOLD, "axiom 7")
AX_7_LOG = join(AX_7_FOLD, "log_1.xes")
AX_7_MODELS = [
    join(AX_7_FOLD, f"ax7_model_{i}.pnml")
    for i 
    in range(1,6)
]
AX_8_FOLD = join(AXS_FOLD, "axiom 8")
AX_8_LOG = join(AX_8_FOLD, "log_1.xes")
AX_8_MODELS = [ 
    join(AX_8_FOLD, f"ax8_model_{i}.pnml")
    for i
    in range(1,5)
]
AX_9_FOLD = join(AXS_FOLD, "axiom 9")
AX_9_MODEL = join(AX_9_FOLD, "ax9_model_1.pnml")
AX_9_LOGS = [ 
    join(AX_9_FOLD, f"log_{i}.xes")
    for i 
    in range(1,4)
]

def axiom_1():
    print("testing axiom 1 for unpublished measurement (grec_E).")

def axiom_3():
    print("testing axiom 3 for unpublished measurement (grec_E).")
    for test_no,model_file in enumerate(AX_3_MODELS):
        results = []
        for run in range(1,11):
            print(f"computing run {run}...")
            res = reasoning_recall(AX_3_LOG, model_file)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        print(f"results for model {test_no+1} of axiom 3 are :: {mean=} | {std=}.")
        print(f"unique results observed :: {set(results)}.")

def axiom_4():
    print("testing axiom 4 for unpublished measurement (grec_E).")
    results = []
    for run in range(1,11):
        print(f"computing run {run}...")
        res = reasoning_recall(AX_4_LOG, AX_4_MODEL)
        results.append(res)
    mean = sum(results) / len(results)
    std = [ (res - mean) ** 2 for res in results ]
    std = sum(std) / len(std)
    std = sqrt(std)
    print(f"results of testing axiom 4 are :: {mean=} | {std=}.")
    print(f"unique results observed :: {set(results)}.") 

def axiom_6():
    print("testing axiom 6 for unpublished measurement (grec_E).")
    for test_no, logfile in enumerate(AX_6_LOGS):
        results = []
        for run in range(1,11):
            print(f"computing run {run}...")
            res = reasoning_recall(logfile, AX_6_MODEL)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        print(f"results for log {test_no+1} of axiom 6 are :: {mean=} | {std=}.")
        print(f"unique results observed :: {set(results)}.")

def axiom_7():
    print("testing axiom 7 for unpublished measurement (gprec_F).")
    for test_no,model_file in enumerate(AX_7_MODELS):
        results = []
        for run in range(1,11):
            print(f"computing run {run}...")
            res = reasoning_precision(AX_7_LOG, model_file)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        print(f"results for model {test_no+1} of axiom 7 are :: {mean=} | {std=}.")
        print(f"unique results observed :: {results}.")

def axiom_8():
    print("testing axiom 8 for unpublished measurement (gprec_F).")
    for test_no,model_file in enumerate(AX_8_MODELS):
        results = []
        for run in range(1,11):
            print(f"computing run {run}...")
            res = reasoning_precision(AX_8_LOG, model_file)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        print(f"results for model {test_no+1} of axiom 8 are :: {mean=} | {std=}.")
        print(f"unique results observed :: {results}.")

def axiom_9():
    print("testing axiom 9 for unpublished measurement (gprec_F).")
    for test_no, logfile in enumerate(AX_9_LOGS):
        results = []
        for run in range(1,11):
            print(f"computing run {run}...")
            res = reasoning_precision(logfile, AX_9_MODEL)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        print(f"results for log {test_no+1} of axiom 9 are :: {mean=} | {std=}.")
        print(f"unique results observed :: {set(results)}.")

if __name__ == "__main__":
    # axiom_3()
    # axiom_4()
    # axiom_6()
    # axiom_7()
    # axiom_8()
    axiom_9()