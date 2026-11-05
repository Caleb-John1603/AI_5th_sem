import re
import matplotlib.pyplot as plt
import networkx as nx

class Term:
    def __init__(self, predicate, args):
        self.predicate = predicate
        self.args = list(args)

    def __repr__(self):
        return f"{self.predicate}({', '.join(self.args)})"

    def __eq__(self, other):
        return isinstance(other, Term) and self.predicate == other.predicate and self.args == other.args

    def __hash__(self):
        return hash((self.predicate, tuple(self.args)))

class Rule:
    def __init__(self, premises, conclusion):
        self.premises = premises  
        self.conclusion = conclusion  

    def __repr__(self):
        return f"{' & '.join(map(str, self.premises))} => {self.conclusion}"

def is_variable(arg):
    return isinstance(arg, str) and len(arg) > 0 and arg[0].islower()

def parse_term(term_str):
    term_str = term_str.strip()
    match = re.match(r"^([A-Za-z0-9_]+)\((.*)\)$", term_str)
    if not match:
        raise ValueError(f"Invalid term format: '{term_str}'. Expected format like Predicate(arg1, arg2)")
    predicate = match.group(1)
    args_str = match.group(2)
    args = [arg.strip() for arg in args_str.split(",") if arg.strip()]
    return Term(predicate, args)

def parse_rule(rule_str):
    if "=>" not in rule_str:
        raise ValueError(f"Invalid rule format: '{rule_str}'. Missing '=>' separator.")
    
    premise_part, conclusion_part = rule_str.split("=>")
    premise_strs = premise_part.split("&")
    premises = [parse_term(p) for p in premise_strs if p.strip()]
    conclusion = parse_term(conclusion_part)
    return Rule(premises, conclusion)

def unify_term(t1, t2, subst=None):
    if subst is None:
        subst = {}
    if t1.predicate != t2.predicate or len(t1.args) != len(t2.args):
        return None
    
    current_subst = dict(subst)
    for a1, a2 in zip(t1.args, t2.args):
        while a1 in current_subst:
            a1 = current_subst[a1]
        while a2 in current_subst:
            a2 = current_subst[a2]
            
        if a1 == a2:
            continue
        if is_variable(a1):
            current_subst[a1] = a2
        elif is_variable(a2):
            current_subst[a2] = a1
        else:
            return None
    return current_subst

def apply_subst(term, subst):
    new_args = []
    for arg in term.args:
        while arg in subst:
            arg = subst[arg]
        new_args.append(arg)
    return Term(term.predicate, new_args)

def standardize_variables(rule, counter):
    subst = {}
    new_premises = []
    for p in rule.premises:
        new_args = []
        for arg in p.args:
            if is_variable(arg):
                if arg not in subst:
                    subst[arg] = f"{arg}_{counter}"
                new_args.append(subst[arg])
            else:
                new_args.append(arg)
        new_premises.append(Term(p.predicate, new_args))
        
    new_conclusion_args = []
    for arg in rule.conclusion.args:
        if is_variable(arg):
            if arg not in subst:
                subst[arg] = f"{arg}_{counter}"
            new_conclusion_args.append(subst[arg])
        else:
            new_conclusion_args.append(arg)
            
    return Rule(new_premises, Term(rule.conclusion.predicate, new_conclusion_args))

def match_premises(premises, kb_facts, subst, matched_facts=None):
    if matched_facts is None:
        matched_facts = []
    if not premises:
        return [(subst, matched_facts)]
    
    first = premises[0]
    rest = premises[1:]
    results = []
    
    for fact in kb_facts:
        local_subst = unify_term(first, fact, subst)
        if local_subst is not None:
            updated_rest = [apply_subst(p, local_subst) for p in rest]
            for final_subst, facts_list in match_premises(updated_rest, kb_facts, local_subst, matched_facts + [fact]):
                results.append((final_subst, facts_list))
    return results

def forward_chaining(kb_rules, kb_facts, goal=None):
    facts = set(kb_facts)
    graph = nx.DiGraph()
    
    for fact in facts:
        graph.add_node(str(fact), type='fact')
        
    std_counter = 0
    new_derived = True
    
    print("\n--- Starting Forward Chaining Inference ---")
    
    while new_derived:
        new_derived = False
        new_facts_this_iteration = set()
        
        for rule in kb_rules:
            std_counter += 1
            std_rule = standardize_variables(rule, std_counter)
            
            matches = match_premises(std_rule.premises, list(facts), {})
            for subst, trigger_facts in matches:
                derived_fact = apply_subst(std_rule.conclusion, subst)
                
                if derived_fact not in facts and derived_fact not in new_facts_this_iteration:
                    print(f"Derived: {derived_fact} via Rule [{rule}] using facts {trigger_facts}")
                    new_facts_this_iteration.add(derived_fact)
                    new_derived = True
                    
                    rule_node_name = f"Rule_{std_counter}_{rule.conclusion.predicate}"
                    graph.add_node(rule_node_name, type='rule')
                    graph.add_node(str(derived_fact), type='fact')
                    
                    for tf in trigger_facts:
                        graph.add_edge(str(tf), rule_node_name)
                    graph.add_edge(rule_node_name, str(derived_fact))
                    
                    if goal and unify_term(derived_fact, goal) is not None:
                        print(f"Goal verified successfully!")
                        facts.update(new_facts_this_iteration)
                        return True, graph
                        
        facts.update(new_facts_this_iteration)
        
    if goal:
        print(f"Goal {goal} could not be proven.")
        return False, graph
    return True, graph

def plot_proof_graph(graph):
    if len(graph.nodes) == 0:
        print("Graph is empty. No steps to display.")
        return
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, k=0.7, seed=42)
    
    fact_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('type') == 'fact']
    rule_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('type') == 'rule']
    
    nx.draw_networkx_nodes(graph, pos, nodelist=fact_nodes, node_color='lightblue', node_shape='o', node_size=2200)
    nx.draw_networkx_nodes(graph, pos, nodelist=rule_nodes, node_color='lightcoral', node_shape='s', node_size=600)
    nx.draw_networkx_edges(graph, pos, arrowstyle="->", arrowsize=15, edge_color='gray')
    
    labels = {n: n if graph.nodes[n].get('type') == 'fact' else '=>' for n in graph.nodes}
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=9, font_weight='bold')
    
    plt.title("First-Order Logic Forward Chaining Proof Graph", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=================================================================")
    print("         Interactive FOL Forward Chaining & Graph Generator      ")
    print("=================================================================")
    print("Rules Notation Notes:")
    print("  - Variables must be a single lowercase letter (e.g., x, y, z)")
    print("  - Constants start with uppercase letters (e.g., West, Nono)")
    print("  - Terms look like: American(West)")
    print("  - Rules use '&' and '=>': Missile(x) & Owns(Nono, x) => Sells(West, x)")
    print("=================================================================\n")
    
    parsed_facts = []
    parsed_rules = []
    
    print("Step 1: Enter your base Facts (Type 'done' when finished):")
    while True:
        f_input = input("Fact: ").strip()
        if f_input.lower() == 'done':
            break
        if not f_input:
            continue
        try:
            parsed_facts.append(parse_term(f_input))
        except Exception as e:
            print(f"Error parsing fact: {e}. Try again.")

    print("\nStep 2: Enter your Knowledge Base Rules (Type 'done' when finished):")
    while True:
        r_input = input("Rule: ").strip()
        if r_input.lower() == 'done':
            break
        if not r_input:
            continue
        try:
            parsed_rules.append(parse_rule(r_input))
        except Exception as e:
            print(f"Error parsing rule: {e}. Try again.")

    print("\nStep 3: Enter the Goal atomic sentence you wish to verify:")
    while True:
        g_input = input("Goal Query: ").strip()
        if not g_input:
            continue
        try:
            goal_query = parse_term(g_input)
            break
        except Exception as e:
            print(f"Error parsing goal: {e}. Try again.")

    satisfied, proof_graph = forward_chaining(parsed_rules, parsed_facts, goal=goal_query)
    
    print(f"\nResult: Is Knowledge Base satisfied for the goal? {satisfied}")
    
    if len(proof_graph.edges) > 0:
        print("\nDisplaying derivation graph window...")
        plot_proof_graph(proof_graph)
    else:
        print("\nNo derivations were successfully generated to map a proof path graph.")
