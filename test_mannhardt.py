from pmkoalas._logging import info, enable_logging
from mannhardt.measure import guard_recall,guard_precision

from time import time
from os.path import join 
from math import sqrt

AXS_FOLD = join(".", "axioms")
AX_3_FOLD = join(AXS_FOLD, "axiom 3")
AX_3_LOG = join(AX_3_FOLD, "log_1.xes")
AX_3_MODELS = [ 
    join(AX_3_FOLD, f"ax3_model_{i}.pnml")
    for i 
    in range(1,7)
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
AX_7B_LOG = join(AX_7_FOLD, "log_3.xes")
AX_7_MODELS = [
    join(AX_7_FOLD, f"ax7_model_{i}b.pnml")
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
AX_8_NEG_MODELS = [ 
    join(AX_8_FOLD, f"ax8_model_{i}.pnml")
    for i
    in range(5,6)
]
AX_9_FOLD = join(AXS_FOLD, "axiom 9")
AX_9_MODEL = join(AX_9_FOLD, "ax9_model_1.pnml")
AX_9_LOGS = [ 
    join(AX_9_FOLD, f"log_{i}.xes")
    for i 
    in range(1,4)
]

AX_RERUNS = 11
OPTIMISED_RUN = True

@enable_logging
def axiom_3():
    info("testing axiom 3 for grec_M.")
    log = AX_3_LOG
    mean_computes = []
    mean_runtimes = []
    for test_no,model_file in enumerate(AX_3_MODELS):
        results = []
        ctimes = []
        for run in range(1,AX_RERUNS):
            info(f"computing run {run}...")
            stime = time()
            res = guard_recall(log,model_file)
            ctimes.append(time() - stime)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        info(f"results for model {test_no+1} of axiom 3 are :: {mean=} | {std=}.")
        info(f"unique results observed :: {set(results)}.")
        runtime = sum(ctimes)/ len (ctimes)
        mean_runtimes.append(f"{runtime:.1f} seconds")
        info(f"average compute time for runs :: {runtime:.1f} seconds.")
        mean_computes.append((mean, std))
    info(f"average runtimes for tests : {mean_runtimes}")
    info("testing completed for axiom three, to adhere the following series" + 
          " must be strictly increasing from left to right")
    info(f"outcome (mean,std) :: {mean_computes}")

@enable_logging
def axiom_4():
    info("testing axiom 4 for grec_M.")
    results = []
    log = AX_4_LOG
    model = AX_4_MODEL
    runtimes = []
    for run in range(1,AX_RERUNS):
        info(f"computing run {run}...")
        stime = time()
        res = guard_recall(log,model)
        runtimes.append(time() - stime)
        results.append(res)
    mean = sum(results) / len(results)
    std = [ (res - mean) ** 2 for res in results ]
    std = sum(std) / len(std)
    std = sqrt(std)
    info(f"results of testing axiom 4 are :: {mean=} | {std=}.")
    info(f"unique results observed :: {set(results)}.") 
    runtimes = sum(runtimes)/len(runtimes)
    info(f"average  compute time for runs :: {runtimes:.1f} seconds.")
    info("testing completed for axiom four, to adhere the measure must " +
         "return zero.")
    info(f"outcomes :: {set(results)}")

@enable_logging
def axiom_6():
    info("testing axiom 6 for grec_M.")
    model = AX_6_MODEL
    mean_computes = []
    mean_runtimes = []
    for test_no, logfile in enumerate(AX_6_LOGS):
        results = []
        runtimes = []
        for run in range(1,AX_RERUNS):
            info(f"computing run {run}...")
            stime = time()
            res = guard_recall(logfile,model)
            runtimes.append(time() - stime)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        runtimes = sum(runtimes) / len(runtimes)
        info(f"results for log {test_no+1} of axiom 6 are :: {mean=} | {std=}.")
        info(f"unique results observed :: {set(results)}.")
        info(f"mean compute time between runs :: {runtimes:.1f} seconds")
        mean_runtimes.append(f"{runtimes:.1f}")
        mean_computes.append((mean,std))
    info(f"average runtimes for tests : {mean_runtimes}")
    info("testing completed for axiom six, to adhere the following series" + 
          " must contain the same value for each step")
    info(f"outcome (mean,std) :: {mean_computes}")

@enable_logging
def axiom_7():
    info("testing axiom 7 for gprec_M.")
    mean_runtimes = []
    mean_computes = []
    log = AX_7B_LOG
    for test_no,model_file in enumerate(AX_7_MODELS):
        results = []
        runtimes = []
        for run in range(1,AX_RERUNS):
            info(f"computing run {run}...")
            stime = time()
            res = guard_precision(log, model_file)
            runtimes.append(time() - stime)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        info(f"results for model {test_no+1} of axiom 7 are :: {mean=} | {std=}.")
        info(f"unique results observed :: {results}.")
        runtime = sum(runtimes) / len(runtimes)
        info(f"mean compute time between runs :: {runtime:.1f} secs")
        mean_runtimes.append(runtime)
        mean_computes.append((mean, std))
    info(f"average runtimes for tests : {mean_runtimes}")
    info("testing completed for axiom seven, to adhere the following series" + 
          " must be strictly increasing from right to left")
    info(f"outcome (mean,std) :: {mean_computes}")


@enable_logging
def axiom_8():
    info("testing axiom 8 for gprec_M.")
    log = AX_8_LOG
    mean_computes = []
    mean_runtimes = []
    mean_neg_computes = []
    mean_neg_runtimes = []
    # should be 1.0
    for test_no,model_file in enumerate(AX_8_MODELS):
        results = []
        runtimes = []
        for run in range(1,AX_RERUNS):
            info(f"computing run {run}...")
            stime = time()
            res = None
            try:
                res = guard_precision(log, model_file)
            except Exception as e:
                res = -1
                info(f"Failed to compute a precision measure for model {test_no}")
            runtimes.append(time() - stime)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        info(f"results for model {test_no+1} of axiom 8 are :: {mean=} | {std=}.")
        info(f"unique results observed :: {results}.")
        runtime = sum(runtimes) / len(runtimes)
        info(f"mean compute time between runs :: {runtime:.1f} secs")
        mean_runtimes.append(runtime)
        mean_computes.append((mean, std))
    # shouldn't be 1.0
    for test_no,model_file in enumerate(AX_8_NEG_MODELS):
        results = []
        runtimes = []
        for run in range(1,AX_RERUNS):
            info(f"computing run {run}...")
            stime = time()
            res = guard_precision(log, model_file)
            runtimes.append(time() - stime)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        info(f"results for model {test_no+1} of axiom 8 are :: {mean=} | {std=}.")
        info(f"unique results observed :: {results}.")
        runtime = sum(runtimes) / len(runtimes)
        info(f"mean compute time between runs :: {runtime:.1f} secs")
        mean_neg_runtimes.append(runtime)
        mean_neg_computes.append((mean, std))
    info(f"average runtimes for tests : {mean_runtimes+mean_neg_runtimes}")
    info("testing completed for axiom eight, to adhere the following series" + 
          " must only return the max of the measure (1.0)")
    info(f"outcome (mean,std) :: {mean_computes}")
    info("Furthermore, to adhere the following series" + 
          " must not return the max of the measure (1.0)")
    info(f"outcome (mean,std) :: {mean_neg_computes}")

@enable_logging
def axiom_9():
    info("testing axiom 9 for gprec_M.")
    mean_computes = []
    mean_runtimes = []
    for test_no, logfile in enumerate(AX_9_LOGS):
        results = []
        runtimes = []
        for run in range(1,AX_RERUNS):
            log = logfile
            info(f"computing run {run}...")
            stime = time()
            res = guard_precision(log, AX_9_MODEL)
            runtimes.append(time() - stime)
            results.append(res)
        mean = sum(results) / len(results)
        std = [ (res - mean) ** 2 for res in results ]
        std = sum(std) / len(std)
        std = sqrt(std)
        info(f"results for log {test_no+1} of axiom 9 are :: {mean=} | {std=}.")
        info(f"unique results observed :: {set(results)}.")
        runtime = sum(runtimes) / len(runtimes)
        info(f"mean compute time between runs :: {runtime:.1f} secs")
        mean_computes.append((mean,std))
        mean_runtimes.append(runtime)
    info(f"average runtimes for tests : {mean_runtimes}")
    info("testing completed for axiom nine, to adhere the following series" + 
        " must contain the same value for each step")
    info(f"outcome (mean,std) :: {mean_computes}")

if __name__ == "__main__":
    # guard-recall testing
    axiom_3(debug=True)
    axiom_4(debug=True)
    axiom_6(debug=True)
    # guard-precision testing
    axiom_7(debug=True)
    axiom_8(debug=True)
    axiom_9(debug=True)
    pass