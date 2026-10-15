def pl_true(sentence, model): 
    if isinstance(sentence, str): 
        return model.get(sentence, False) 
    op = sentence[0] 
    if op == 'not': 
        return not pl_true(sentence[1], model) 
    elif op == 'and': 
        return all(pl_true(arg, model) for arg in sentence[1:]) 
    elif op == 'or': 
        return any(pl_true(arg, model) for arg in sentence[1:]) 
    elif op == 'implies': 
        return (not pl_true(sentence[1], model)) or pl_true(sentence[2], model) 
    elif op == 'iff': 
        return pl_true(sentence[1], model) == pl_true(sentence[2], model) 
    return False 

def get_symbols(sentence): 
    if isinstance(sentence, str): 
        return {sentence} 
    symbols = set() 
    for arg in sentence[1:]: 
        symbols.update(get_symbols(arg)) 
    return symbols 

def tt_entails(kb, alpha): 
    symbols = sorted(list(get_symbols(kb) | get_symbols(alpha))) 
    print(f"{' | '.join(symbols)} || KB    | alpha | Match") 
    print("-" * (len(symbols) * 4 + 25)) 
    return tt_check_all(kb, alpha, symbols, {}) 

def tt_check_all(kb, alpha, symbols, model): 
    if not symbols: 
        kb_val = pl_true(kb, model) 
        alpha_val = pl_true(alpha, model) 
        # Match checks if KB -> Alpha holds (is true unless KB is True and Alpha is False)
        match = "OK" if ( kb_val and alpha_val) else "FAIL" 
        row_vals = [str(model[sym])[0] for sym in sorted(model.keys())] 
        print(f"{' | '.join(row_vals)} || {str(kb_val)[0]:<5} | {str(alpha_val)[0]:<5} | {match}") 
        if kb_val: 
            return alpha_val 
        return True 
    
    P = symbols[0] 
    rest = symbols[1:] 
    
    model_true = model.copy() 
    model_true[P] = True 
    res_true = tt_check_all(kb, alpha, rest, model_true) 
    
    model_false = model.copy() 
    model_false[P] = False 
    res_false = tt_check_all(kb, alpha, rest, model_false) 
    
    return res_true and res_false 


kb_expr = ('and', ('implies', 'P', 'Q'), ('implies', 'Q', 'R'), 'P') 

alpha_expr = 'R' 

entails = tt_entails(kb_expr, alpha_expr) 
print(f"\nEntailment holds: {entails}")
