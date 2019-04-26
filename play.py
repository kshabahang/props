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

def graph_prop(prop):

    (frame, args) = prop
    root = Digraph(frame, filename=frame + ".gv")
    root.node(frame)
    roles = args.keys()
    for role in roles:
        if type(args[role]) == str:
            #terminal
            root.node(args[role])
            root.edge(frame, args[role], role)
        elif type(args[role]) == list:
            child = args[role][0] #TODO: account for lists with more than one prop
            (frame_l2, args_l2) = child
            subgraph = Digraph(frame_l2)
            subgraph.node(frame_l2)
            for role_l2 in args_l2.keys():
                subgraph.edge(frame_l2, args_l2[role_l2], role_l2)
            root.subgraph(subgraph)
            root.edge(frame, frame_l2, role)

    return root


if __name__ == "__main__":
    parsed = parse_lvl2("Roger was driving his new car")
    props1 = parsed['props']
    parsed = parse_lvl2("Roger's car was a blue Tesla")
    props2 = parsed['props']

     













