from typing import Set,Iterable,List,Dict,Tuple,Union
from copy import deepcopy,copy
from logging import debug
from tempfile import mkdtemp
from itertools import product
from joblib import Parallel,delayed,Memory
from tqdm import tqdm


from expressions import ExpressionParser


class VariableDomain():
    """
    A representation of the observed domain for a data variable
    """

    def __init__(self, name:str) -> None:
        self._name = name 
        self._observed = set()
        self._types = set()

    def add(self, value:object):
        self._observed.add(value)
        self._types.add(type(value))

    def rng(self) -> Set:
        return copy(self._observed)

worker_pool = Parallel(n_jobs=-2,batch_size=50)
mem_cache = Memory(mkdtemp(), verbose=0)

@mem_cache.cache
def batch_jobber(states,exp) -> Set:
    accepted = set()
    try :
        parser = ExpressionParser(dict(states), exp)
        if parser.result():
            for state in states:
                accepted.add(state)
    except Exception as e:
        print(f"failed :: {e}")
    return accepted

class Expression():
    """
    A representation of reasoning extractable from a boolean logic expression.
    """

    def __init__(self, exp:str, domain_limits:Dict[str,object]=dict()) -> None:
        self._org_exp = exp 
        self._parser = ExpressionParser(dict(), exp)
        self._parsed_exp = None
        self._dom = self._find_dom(exp)
        self._rng = self._find_rng(exp,domain_limits)

    def _find_dom(self, exp:str) -> Set[str]:
        parser = ExpressionParser(dict(), exp)
        return parser.get_observed_vars()

    def _find_rng(self, exp:str, domain_limits:Dict[str,object]) -> Set[object]:
        print(f"find rng of :: {exp} | this may take some time...")
        accepted = set()
        require_variables = [ dl._name for dl in domain_limits.values() if dl._name in self._dom ]
        unrequired_vars = [ dl for dl in domain_limits.values() if dl._name not in require_variables ]
        generator = tqdm(list(product(*[ list(product([dl._name],dl.rng())) for dl in domain_limits.values() if dl._name in self._dom])),
            desc="testing")
        batches = worker_pool(delayed(batch_jobber)(states,exp) for states in generator)
        for batch in batches:
            accepted = accepted.union(batch)
        if len(self._dom) > 0 and len(require_variables) > 0 and len(accepted) > 0:
            for domain in unrequired_vars:
                values = domain.rng()
                accepted = accepted.union(set([ (domain._name,v) for v in values]))
        return accepted 

    def test_dom(self, data:Dict[str,object]) -> bool:
        obs_variables = data.keys()
        meets = True 
        for rd in self._dom:
            meets = meets and rd in obs_variables
        return meets 

    def test_rng(self, data:Dict[str,object]) -> bool:
        meets = self.test_dom(data)
        if not meets:
            return meets  
        for rd in self._dom:
            pair = (rd, data[rd])
            meets = meets and pair in self._rng
        return meets 
    
    def dom(self) -> Set:
        return self._dom

    def rng(self) -> Set:
        return self._rng
    
    def is_truth(self) -> bool:
        """
        TODO consider a more elgant solutions to determining if something is a
        truth for the observed state space.
        """
        if self._org_exp == 'true':
            return True
        return False

    def __str__(self) -> str:
        return self._org_exp

class Negation(Expression):
    """
    A representation of reasoning that is always false.
    """

    def __init__(self, domain_limits: Dict[str, object]) -> None:
        super().__init__("false", domain_limits)

    def _find_dom(self,exp: str) -> Set[str]:
        return set()

    def test_dom(self, data:Dict[str,object]) -> bool:
        return False

    def _find_rng(self,exp: str, domain_limits: Dict[str, object]) -> Set[object]:
        return set()

    def test_rng(self, data:Dict[str,object]) -> bool:
        return False

    def is_truth(self) -> bool:
        return False

class Truth(Expression):
    """
    A representation of reasoning that is always true.
    """

    def __init__(self, domain_limits: Dict[str, object]) -> None:
        super().__init__("true", domain_limits)

    def _find_rng(self,exp: str, domain_limits: Dict[str, object]) -> Set[object]:
        return set(
            product(*[ 
                list(product([dl._name],dl.rng())) 
                for dl 
                in domain_limits.values()
            ])
        )

    def test_rng(self, data:Dict[str,object]) -> bool:
        return True

    def is_truth(self) -> bool:
        return True

class Guard():
    """
    A representation of a guard in the form of boolean expression.
    """

    def __init__(self, exp:Expression) -> None:
        self._exp = exp

    def test_dom(self, data:Dict[str,object]) -> bool:
        return self._exp.test_dom(data) 

    def test_rng(self, data:Dict[str,object]) -> bool:
        return self._exp.test_rng(data) 

    def is_truth(self) -> bool:
        return self._exp.is_truth()

    def dom(self) -> Set:
        return self._exp.dom()

    def rng(self) -> Set:
        return self._exp.rng()

    def could_evalate(self, state:Dict) -> bool:
        return self._exp.test_dom(state)

    def is_supported(self, state:Dict) -> bool:
        supported = self.could_evalate(state)
        if not supported:
            return supported 
        for d in self.dom():
            supported = supported and (d,state[d]) in self.rng()
        return supported

    def __str__(self) -> str:
        return str(self._exp)


class Transition():
    """
    An atomic part of a process model (not related to representation).
    """
    
    def __init__(self, label:str, guard:Guard=None, domain_limits: Dict[str, object]=dict()) -> None:
        self._label = label
        self._guard = Truth(domain_limits) if guard == None else guard

    def test_guard(self, data:Dict[str,object]) -> bool:
        return self._guard(data) 

    def __eq__(self, __o: object) -> bool:
        if (isinstance(__o, Transition)):
            return self._label == __o._label
        return False

    def __str__(self) -> str:
        return f"{self._label}" 

    def __hash__(self) -> int:
        return hash(tuple([self._label]))

class Outcome(Transition):
    """
    An atomic part of a process model, but is an outcome of a choice.
    """

    def __init__(self, label: str, choice:object=None, guard:Guard=None, domain_limits: Dict[str, object]=dict())-> None:
        super().__init__(label,guard=guard,domain_limits=domain_limits)
        self._choice = choice

    def set_choice(self, choice:object):
        self._choice = choice

    def related_choice(self) -> object:
        return self._choice

    def __repr__(self) -> str:
        return f"([{self.__str__()}] from [{self._choice._label}])"

    def __hash__(self) -> int:
        return hash(tuple([self._label, self._choice.__hash__()]))

class IndifferentChoice():
    """
    Representation for the indifference of choice for a process model.
    """

    def __init__(self) -> None:
        pass

class Choice():
    """
    A repsentation of a choice, consisting of all 'transitions' involved and
    a set of outcome 'transitions'.
    """

    def __init__(self, label:str, parts:List[Transition], outcomes:List[Outcome]) -> None:
        self._label = label
        self._parts = parts 
        self._outcomes = outcomes

    def oth(self,outcome) -> List[object]:
        oth = [] 
        for outs in self._outcomes:
            if outs != outcome:
                oth.append(outs) 
        return oth

    def outcomes(self) -> Iterable[object]:
        for outcome in self._outcomes:
            yield outcome

    def parts(self) -> Iterable[object]:
        for part in self._parts:
            yield part 

    def contains(self, other:Transition) -> bool:
        return other in self._outcomes

    def __str__(self) -> str:
        repr = f"([{self._label}] -> ["
        for out in self._outcomes:
            repr += str(out) + ","
        return repr + "])"

    def __hash__(self) -> int:
        out_hashes = [ out._label for out in self._outcomes]
        return hash(tuple([self._label]+out_hashes))

    def __repr__(self) -> str:
        return self.__str__()

class ProcessModel():
    """
    A representation of a process model from a pnml file (expecting a Petri net
    with data).
    """

    def __init__(self, model_path:str, domain_limits:Dict[str,VariableDomain]=dict()) -> None:
        import pm4py
        self._petri_net, self._petri_net_im, self._petri_net_fm = pm4py.read_pnml(model_path)
        self._traces = set() # a nasty TODO
        self._limits = domain_limits
        self._find_choices(self._petri_net)
        self._handle_transitions(self._petri_net)
        self._build_part_mapping()
        self._find_domains()

    def _find_choices(self, model) -> None:
        self._choices = set()
        self._transitions = dict()
        for place in model.places:
            if len(place.out_arcs) > 1:
                outcomes = [] 
                for target in [ arc.target for arc in place.out_arcs ]:
                    if 'guard' in target.properties:
                        guard_str = target.properties['guard']
                    else:
                        guard_str = 'true'
                    if guard_str == "true":
                        expression = Truth(self._limits)
                    elif guard_str == "false":
                        expression = Negation(self._limits)
                    else:
                        expression = Expression(guard_str,domain_limits=deepcopy(self._limits))
                    outcome = Outcome(target.name, guard=Guard(expression))
                    outcomes.append(outcome)
                choice = Choice(place.name, outcomes, outcomes)
                for out in outcomes:
                    out.set_choice(choice)
                    self._transitions[out._label] = out
                self._choices.add(choice)

    def _handle_transitions(self, model) -> None: 
        for tran in model.transitions:
            if tran.name in self._transitions:
                continue
            if 'guard' in tran.properties:
                guard_str = tran.properties['guard']
            else:
                guard_str = 'true'
            if guard_str == "true":
                expression = Truth(self._limits)
            elif guard_str == "false":
                expression = Negation(self._limits)
            else:
                expression = Expression(guard_str,domain_limits=deepcopy(self._limits))
            self._transitions[tran.name] = Transition(tran.name,Guard(expression))

    def _build_part_mapping(self) -> None:
        self._part_to_choice = dict() 
        for name,tran in self._transitions.items():
            choicer = IndifferentChoice()
            for choice in self._choices:
                if choice.contains(tran):
                    choicer = choice 
                    break 
            self._part_to_choice[name] = (choicer, tran._guard)

    def _find_domains(self) -> None:
        self._var_domain = set()
        self._guard_domain = set()
        self._restricted_guard_domain = set()
        for _,(choice,guard) in self._part_to_choice.items():
            if not isinstance(choice,IndifferentChoice):
                self._var_domain = self._var_domain.union(guard.dom())
                self._guard_domain.add(guard)
                if (not guard.is_truth()):
                    self._restricted_guard_domain.add(guard)

    def variable_domain(self) -> Set[str]:
        return self._var_domain

    def choice_domain(self) -> Set[Choice]:
        return self._choices

    def guard_domain(self, restricted=True) -> Set[Guard]:
        if (restricted):
            return self._restricted_guard_domain
        return self._guard_domain


class EventLog():
    """
    A representation of an event log from an xes event log using pm4py.
    """

    _ignore_attrs = ["concept:event:id", "concept:name", "time:timestamp",]

    def __init__(self, log_path:str) -> None:
        import pm4py
        self._log = pm4py.read_xes(log_path)
        self._events = set()
        self._traces = set()
        self._trace_to_instances = dict()
        self._event_to_mapping = dict()
        self._limits = dict()
        self._find_traces(self._log)
        self._find_event_space(self._log)
        self._find_domains()
        
    def _find_traces(self, log) -> None:
        for inst in log:
            trace = tuple([e["concept:name"] for e in inst])
            self._traces.add(trace)
            if trace not in self._trace_to_instances:
                self._trace_to_instances[trace] = []
            self._trace_to_instances[trace].append(inst)

    def _find_event_space(self, log) -> None:
        count = 1
        for inst in log:
            data_state = dict()
            for ev in inst:
                ev["concept:event:id"] = count
                count += 1
                # build a history data state for each event
                before = deepcopy(data_state)
                after = deepcopy(data_state)
                after.update(ev._dict)
                self._event_to_mapping[ev] = (before,after)
                # update limits
                for key,val in after.items():
                    if key in self._ignore_attrs:
                        continue
                    if key not in self._limits:
                        self._limits[key] = VariableDomain(key)
                    self._limits[key].add(val)
                # set up for next event
                data_state = deepcopy(after)
                self._events.add(ev)
    
    def _find_domains(self):
        self._variable_domain = set(list(self._limits.keys()))

    def data_domain_limits(self) -> Dict[str,VariableDomain]:
        return self._limits

    def variable_domain(self) -> Set:
        return self._variable_domain

    def get_state(self, event) -> Dict:
        if event in self._events:
            return self._event_to_mapping[event]
        raise ValueError("Given an unseen event, no mapping exists.")

    def get_traces(self) -> List[Tuple[Tuple[str],int]]:
        trace_count = []
        for key,val in self._trace_to_instances.items():
            trace_count.append((key,len(val)))
        return trace_count

    def get_instances(self, trace:Tuple[str]) -> List:
        if trace not in self._trace_to_instances:
            print("no instances found for trace")
            return [] 
        return self._trace_to_instances[trace]


class Observation():
    """
    A representation of a observation, which consists of a likelihood, a data state,
    a choice, an outcome of that choice and the described guard.
    """

    def __init__(self, likelihood:float, data:Dict, choice:Choice, outcome:Outcome,
        guard:Guard) -> None:
        self.likelihood = likelihood
        self.data = data 
        self.choice = choice 
        self.outcome = outcome 
        self.guard = guard


class AlignmentController():
    """
    Wrapper around pm4py alignment function to make querying for a given trace
    instance a bit easier and simplier. Also handles the relative frequency of a
    transition in a process model.

    Expects a presentation of an event log and a representation of a process model.
    """

    def __init__(self, log:EventLog, model:ProcessModel) -> None:
        self._log = log._log 
        self._model = model._petri_net 
        self._im = model._petri_net_im 
        self._fm = model._petri_net_fm
        self.__compute_alignment()
        self.__compute_relative_frequency(log, model)

    def __compute_alignment(self):
        # compute alignments but this gives you back an alignment (maybe) for each trace instance
        # rather than one per trace (variant) and no indentifier back to data????
        from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
        aligned_traces = alignments.apply_log(self._log, self._model, self._im, 
            self._fm, parameters={'ret_tuple_as_trans_desc': True})
        # work them into a usage form trace -> alignment
        self._trace_to_align = dict()
        self._trace_to_fitness = dict()
        for alignment in aligned_traces:  
            indexed_trace = [ 
                tuple(alog.split("_")[1:] +[model]) 
                for ((alog,model),(log,_)) 
                in alignment['alignment']
                if log != ">>" and model != ">>"
            ]
            trace = tuple([ 
                log 
                for ((_,_),(log,_)) 
                in alignment['alignment']
                if log != ">>"
            ])
            if trace not in self._trace_to_align:
                self._trace_to_align[trace] = indexed_trace
                self._trace_to_fitness[trace] = alignment['fitness']
        
    def __compute_relative_frequency(self, log:EventLog, process_model:ProcessModel) -> None:
        """
        Computes the martix for the relative frequency for each choice and outcome of a choice.
        """
        self._count_choice = dict() 
        self._count_outcome = dict()
        #compute frequency count
        for trace,count in log.get_traces():
            alignment = self._trace_to_align[trace]
            for choice in process_model.choice_domain():
                outcomes = [ (out,out._label) for out in choice.outcomes() ] 
                if choice not in self._count_choice:
                    self._count_choice[choice] = 0
                for out,name in outcomes:
                    # print(f"computing count for {choice} -> {out} -> {name}")
                    # print(f"comparing with alignment :: {alignment}")
                    if out not in self._count_outcome:
                        self._count_outcome[out] = 0
                    if name in [ s[2] for s in alignment ]:
                        mut = len( [s[2] for s in alignment if s[2] == name])
                        self._count_outcome[out] += mut * count 
                for out,_ in outcomes:        
                    self._count_choice[choice] += self._count_outcome[out]
        # compute relative freq
        total_choices = sum(self._count_choice.values())
        self._rel_freq_choice = dict()
        self._rel_freq_outcome = dict()
        for choice,count in self._count_choice.items():
            global_freq = count / (total_choices * 1.0)
            self._rel_freq_choice[choice] = global_freq
            local_sum = sum([self._count_outcome[out] for out in choice.outcomes() ])
            for out in choice.outcomes():
                local_freq = self._count_outcome[out] / (local_sum * 1.0)
                self._rel_freq_outcome[out] = local_freq  
        if (len(self._rel_freq_choice.keys()) > 1):
            # check that rf is 1 over all choices
            # check that rf is 1 over all local outcomes of choices
            choice_freq = sum(self._rel_freq_choice.values())
            if abs(choice_freq - 1.0) > 0.01:
                raise ArithmeticError(f"Relative frequency for choices does not sum to 1.0 :: {choice_freq:.3f}")
            big_total = 0.0
            for choice,freq in self._rel_freq_choice.items():
                mini_total = 0.0
                for outcome in choice.outcomes():
                    mini_total += self._rel_freq_outcome[outcome] * freq
                if abs(mini_total - freq) > 0.01:
                    raise ArithmeticError(f"local sum of Relative frequencies choice*outcome does not sum to relative frequency :: {mini_total:.2f}, expected {freq:.3f}")
                big_total += mini_total
            if abs(big_total - 1) > 0.01:
                    raise ArithmeticError(f"Sum of Relative frequencies choice*outcome does not sum to 1.0 :: {big_total:.2f}")
            debug("choice relative frequency :: ",self._rel_freq_choice)
            debug("local outcome frequency :: ",self._rel_freq_outcome)

    def find_choice_points(self, trace:Tuple[str], choice:Choice) -> List[Tuple[int,Outcome]]:
        """
        Find the exact points in a trace that are related to a choice.
        """
        if trace not in self._trace_to_align:
            print(f"{trace} not found in {self._trace_to_align.keys()}")
            return []
        # find points of choice for given choice 
        points = [] 
        alignment = self._trace_to_align[trace]
        outs = [ (out,out._label) for out in choice.outcomes()]
        for outcome,name in outs:
            temp = [ (int(s[1]),outcome) for s in alignment if s[2] == name ]
            if len(temp) > 0:
                points = points + temp
        return points

    def relative_frequency(self, choice:Choice, outcome:Outcome) -> float:
        """
        Returns the relative frequency of seeing an outcome from a choice.
        """
        if choice not in self._rel_freq_choice:
            return 0.0
        else:
            if outcome not in self._rel_freq_outcome:
                return 0.0
        return self._rel_freq_choice[choice] * self._rel_freq_outcome[outcome]    

    def get_trace_likelihood(self, trace:Tuple[str]):
        """
        Returns the likelihood of seeing a trace.
        """
        if trace not in self._trace_to_fitness:
            return 0.0 
        return self._trace_to_fitness[trace]



def check_for_common_subset(log:EventLog, model:ProcessModel) -> Set[str]:
    """
    Performs a check to see if a common subset of data variables between
    log and model exists to conform with G3, returning the common subset.
    """
    print(f"domain of data variables for the log :: {log.variable_domain()}")
    print(f"domain of data variables for the process model :: {model.variable_domain()}")
    common_domain = model.variable_domain().intersection(log.variable_domain())
    if len(common_domain) == 0:
        if (len(model.guard_domain()) > 0):
            raise ValueError("Unable to measure as no common subset of variables exists.")

    return common_domain

def observation_function(log:EventLog, model:ProcessModel) -> Iterable[Tuple[
        Observation,AlignmentController]]:
    """
    For a given log and model, produces observations for each choice described in
    the model with the observed data from the log.

    Function yields a choice object, then a tuple containing the containing the 
    outcome object and all observed data instances for this outcome.
    """
    # perform alignment (may be expensive)
    aligner = AlignmentController(log, model)
    # produce observations
    gen = 0
    for trace,count in log.get_traces():
        for choice in model.choice_domain():
            choice_points = aligner.find_choice_points(trace, choice)
            debug(f"no of choice points found for {trace} :: {len(choice_points)}")
            for inst in log.get_instances(trace):
                for (eid,outcome) in choice_points:
                    before_state,_ = log.get_state(inst[eid])
                    obs = Observation(
                        aligner.get_trace_likelihood(trace),
                        deepcopy(before_state),
                        choice,
                        outcome,
                        outcome._guard
                    )
                    yield (obs, aligner) 
                    gen +=1
    print(f"total number of observations :: {gen}")


def reasoning_recall(log_path:str, model_path:str) -> float:
    """
    Computes reasoning recall for the given log and model, if possible, otherwise
    will intensionally throw an error to say this pair cannot be measured.

    Parameters
    ------------
    log_path:`str`
        path to xes log
    model_path:`str`
        path to petri with data as a pnml file
    """
    log = EventLog(log_path)
    model= ProcessModel(model_path, log.data_domain_limits())
    common_domain = check_for_common_subset(log, model)
    print(f"Found common set of variables :: {str(common_domain)}")
    print(f"Choice domain for the model is :: {str(model.choice_domain())}")
    # compute measure
    measure = 0.0
    total_freq = 0.0
    for obs,aligner in observation_function(log, model):
        b = 0 if obs.guard.is_truth() else 1
        b = b * (obs.likelihood if obs.guard.could_evalate(obs.data) else 0)
        rel_freq = aligner.relative_frequency(obs.choice, obs.outcome)
        obs_measure = rel_freq * b
        measure += obs_measure
        total_freq+=rel_freq
        debug(f"{str(obs.guard)=}|{obs.guard.is_truth()=}|{b=:.2f}|{rel_freq=:.2f}|{obs_measure=:.3f}|{total_freq=}|{measure=}")
    result = (1.0/total_freq) * measure if total_freq > 0 else 1.0
    print(f"Computed reasoning-recall :: {result:.3f}")
    return result

def reasoning_precision(log_path:str, model_path:str) -> float:
    """
    Computes reasoning precision for the given log and model, if possible, otherwise
    will intensionally throw an error to say this pair cannot be measured.

    Parameters
    ------------
    log_path:`str`
        path to xes log
    model_path:`str`
        path to petri with data as a pnml file
    """
    log = EventLog(log_path)
    model= ProcessModel(model_path, log.data_domain_limits())
    common_domain = check_for_common_subset(log, model)
    #compute measure
    measure = 0.0
    total_freq = 0.0
    for obs,aligner in observation_function(log, model):
        b = 0 if obs.guard.is_truth() else 1
        b = b * (obs.likelihood if (obs.guard.could_evalate(obs.data) and 
            obs.guard.is_supported(obs.data)) else 0)
        c = 1 + sum([ out._guard.is_supported(obs.data) for out in obs.choice.oth(obs.outcome)])
        rel_freq = aligner.relative_frequency(obs.choice, obs.outcome)
        obs_measure = rel_freq * b * (1.0/c)
        measure += obs_measure
        total_freq += rel_freq
        debug(f"{str(obs.guard)=}|{obs.guard.is_truth()=}|{b=:.2f}|{c=:.2f}|{rel_freq=:.2f}|{obs_measure=:.3f}|{total_freq=}")
    result = (1/total_freq) * measure if total_freq > 0 else 1.0
    print(f"Computed reasoning-precision :: {result:.3f}")
    return result



