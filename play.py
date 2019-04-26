from graphviz import Digraph
import os

def parse(text):
      
    f = open("parse.in", "w")
    f.write(text)
    f.close()
    
    os.system("./run_pipeline.sh parse.in 1> parse.out 2> err.out")
    f = open("parse.out", "r")
    parsed = f.readlines()
    f.close()
    
    parts = {'sent':[], 'terms':[], 'props':[]}
    for i in xrange(len(parsed)):
        if '\t' in parsed[i]:
            parts['terms'].append(parsed[i].strip())
        elif ':(' in parsed[i]:
            prop = parsed[i].strip().split(':(')
            verb = prop[0]
            args = prop[1][:-1].split(' , ')
            arg_dic = {}
            for arg in args:
                arg = arg.split(':')
                if len(arg) > 1:
                    arg_dic[arg[0]] = arg[1]
                else:
                    arg_dic[arg[0]] = ''
            parts['props'].append((verb , arg_dic))
    
        elif "/" not in parsed[i]:
            parts['sent'].append(parsed[i].strip())
        

    return parts

def parse_lvl2(text):
    parsed =  parse(text)
    parsed_lvl2 = {'sent':parsed['sent'], 'terms':parsed['terms'], 'props':[]}
    for prop in parsed['props']:
        verb = prop[0]
        args = prop[1]
        print args
        args_prop = {}
        for role in args.keys():
            if len(args[role].split()) > 2:
                parsed = parse(args[role])
                args_prop[role] = parsed['props']
            else:
                args_prop[role] = args[role]
        prop = (verb, args_prop)
        parsed_lvl2['props'].append(prop)
    return parsed_lvl2



if __name__ == "__main__":
    parsed = parse("The fluffy cat sat on the blue mat")

    
    
    g = Digraph('G', filename='hello.gv')
    
    ###source
    src_indicators = ["subj"]
    src = ''
    ###targ
    targ_indicators = ["prep_in", "prep_on"]
    targ = ''

    prop = parsed['props'][0]
    (frame, args) = prop
    roles = args.keys()
    for role in roles:
        print type(args[role])
        
        g.node(args[role])
        if role in src_indicators:
            src = role
        if role in targ_indicators:
            targ = role
    if src != '' and targ != '':
        g.edge(args[src], args[targ], frame)







    




    g.view()
















