from pm4py.objects.log.obj import EventLog, Trace, Event 
from pm4py import write_xes

from typing import List
from math import log
from random import randint, choice, random
from string import ascii_lowercase
from datetime import datetime, timedelta
from os.path import join
from copy import deepcopy

WRK_DIR = join(".")
LOG_ONE_FILE = join(WRK_DIR,"log_1.xes")
LOG_TWO_FILE = join(WRK_DIR,"log_4.xes")
LOG_THREE_FILE_A = join(WRK_DIR,"log_2.xes")
LOG_THREE_FILE_B = join(WRK_DIR,"log_5.xes")
LOG_THREE_FILE_C = join(WRK_DIR,"log_3.xes")

TS_ONE = datetime.now()
TS_TWO = TS_ONE + timedelta(days=1)
TS_THREE = TS_TWO + timedelta(days=1)
TS_FOUR = TS_THREE + timedelta(days=1)

def gen_d1(act:str) -> int:
    "CONTINOUS BETWEEN 5 to 10 (INCLUSIVE)"
    if (act == "B"):
        return randint(5,6)
    if (act == "C"):
        return randint(7,8)
    return randint(9,10)

def gen_d2():
    "LITERAL, many options (lower)"
    return choice(ascii_lowercase)

def gen_d3():
    "LITERAL only 3 options (upper)"
    options = ascii_lowercase.upper()[:3]
    return choice(options) *2

def gen_d4():
    "CONTINOUS BETWEEN 1 to 100 (INCLUSIVE)"
    return randint(1,100) 

def gen_d5():
    "CONTINOUS BETWEEN 10 to 25 (INCLUSIVE)"
    return randint(10,25) 

def gen_d6():
    "BOOLEAN"
    x = (random()* 3) + 1.0
    return log((5*x)/10.0) >= 0.0

def mut_trace(trace:Trace, mut:int) -> List[Trace]:
    traces = []
    for trace_no in range(mut):
        events = []
        for ev in trace:
            attrs = []
            for key,val in ev._dict.items():
                if key == "concept:name":
                    attrs.append((key,val))
                else:
                    attrs.append((key,val()))
            events.append(Event(attrs))
        traces.append(Trace(events))
    return traces

FREQ_MUT = 100
COMMON_MUT = 3 * FREQ_MUT
UNCOMMON_MUT = 2 * FREQ_MUT
RARE_MUT = 1 * FREQ_MUT

def create_log_one() -> EventLog:
    """
    Generates a log with data variables:\n
    d1(A), d2(A->B), d3(A->C|A->D), d4(E), d5(E->F), d6(E->G)).\n
    Log has the following traces:
      -> B ->   -> F -> 
    A -> C -> E -> G -> 
      -> D ->   -> H -> 
     - A,B,E,F^3 X
     - A,B,E,G^2 X
     - A,B,E,H^1 X
     - A,C,E,F^3 X
     - A,C,E,G^2 X
     - A,C,E,H^1 X
     - A,D,E,F^3 
     - A,D,E,G^2
     - A,D,E,H^1
    """
    log = EventLog(**{
        "attributes" : {
            "concept:name" : "DAC LOG ONE"
        }
    })

    traces = mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda : gen_d1("B") ),("d2",gen_d2),("time:timestamp", lambda : TS_ONE)]),
                Event([("concept:name","B"),("time:timestamp",lambda : TS_TWO)]),
                Event([("concept:name","E"),("d4",gen_d4),("d5",gen_d5),("time:timestamp", lambda : TS_THREE)]),
                Event([("concept:name","F"),("time:timestamp",lambda : TS_FOUR)]),
            ]
        ), COMMON_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("B")),("d2",lambda :gen_d2()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","B"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("d6",lambda :gen_d6()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","G"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), UNCOMMON_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("B")),("d2",lambda :gen_d2()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","B"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","H"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), RARE_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("C")),("d3",lambda :gen_d3()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","C"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("d5",lambda :gen_d5()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","F"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), COMMON_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("C")),("d3",lambda :gen_d3()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","C"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("d6",lambda :gen_d6()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","G"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), UNCOMMON_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("C")),("d3",lambda :gen_d3()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","C"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","H"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), RARE_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("D")),("d3",lambda :gen_d3()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","D"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("d5",lambda :gen_d5()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","F"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), COMMON_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("D")),("d3",lambda :gen_d3()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","D"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("d6",lambda :gen_d6()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","G"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), UNCOMMON_MUT) + mut_trace(Trace(
            [
                Event([("concept:name","A"),("d1",lambda :gen_d1("D")),("d3",lambda :gen_d3()),("time:timestamp",lambda :TS_ONE)]),
                Event([("concept:name","D"),("time:timestamp",lambda :TS_TWO)]),
                Event([("concept:name","E"),("d4",lambda :gen_d4()),("time:timestamp",lambda :TS_THREE)]),
                Event([("concept:name","H"),("time:timestamp",lambda :TS_FOUR)]),
            ]
        ), RARE_MUT)

    for i,t in enumerate(traces):
        t._attributes["concept:name"] = f"trace {i+1:03d}"

    log._list = traces
    return log

def make_log_one() -> EventLog:
    print("making log one...")
    log = create_log_one()
    write_xes(log, LOG_ONE_FILE)
    return log

def make_log_two(log):
    print("making log two...")
    clog = deepcopy(log)
    def check(t:Trace) -> bool:
        checker = True
        for e,act in zip(t,["A","C","E","G"]):
            checker = checker and e["concept:name"] == act 
        return checker
    clog._list = [ 
        t 
        for t 
        in log._list 
        if check(t)
    ]
    clog._attributes["concept:name"] = "DAC LOG FOUR"
    write_xes(clog, LOG_TWO_FILE)

def make_log_three(log):
    print("making log three...")
    log_a = deepcopy(log)
    log_b = create_log_one()
    log_a._list = log_a._list + log_a._list
    log_a._attributes["concept:name"] = "DAC LOG TWO - ENLARGED A"
    write_xes(log_a, LOG_THREE_FILE_A)
    log_a._list = deepcopy(log._list) + log_b._list
    log_a._attributes["concept:name"] = "DAC LOG FIVE - TWO SAMPLE LOG"
    write_xes(log_a, LOG_THREE_FILE_B)
    log_a._list = deepcopy(log._list)
    log_a._list = log_a._list + log_a._list + log_a._list + log_a._list
    log_a._attributes["concept:name"] = "DAC LOG THREE - ENLARGED B"
    write_xes(log_a, LOG_THREE_FILE_C)


if __name__ == "__main__":
    eventlog = make_log_one()
    make_log_two(eventlog)
    make_log_three(eventlog)