#Παρ 18 Αύγ 2017 02:19:17 ΜΜ EEST 



#!usr/bin/python
import sys
import re
import math
import mmap
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

def draw_graph(states,graph_tuple):

    # extract nodes from graph
    nodes = states[0:-1]
    #print nodes
    # create networkx graph
    G=nx.MultiDiGraph()

    # add nodes
    for node in nodes:
       G.add_node(node)

    # add edges
    for edge in graph_tuple:
        print edge
        if len(edge)==2:
            G.add_edge(edge[0], edge[1])
        else:
            G.add_edge(edge[0], edge[1])
            G.add_edge(edge[0], edge[2])
    # draw graph
    pos = nx.spectral_layout(G)
    plt.axis('off')
    nx.draw_networkx(G, pos,with_labels=True,
                    arrows=True,
                    node_size=500,
                    font_size=8,
                    font_color='k',
                    node_color='r')


    # show graph
    plt.show()

num_of_states=int(sys.argv[1]) #number of states without others statement
states=[];
lines_after_when=[];
transition=[];
graph_trans=[[] for x in range(num_of_states+1)]; #including others statement

i=0;
k=0;
j=0;

with open("final_system_new/metric_fsm.vhd") as openfile_2:
    lines=openfile_2.readlines()
    for i in range(0,len(lines)):
        line=lines[i]
        if "when" in line:
            st8=line.split()
            states.append(st8[1])
            y=lines[i+1].split();
            if y[0]=='if':
                tr1=lines[i+2].split();
                graph_trans[k].append(states[k])
                if tr1[0]=='if':
                    trans1=lines[i+3].split();
                    trans2=lines[i+5].split();
                    trans3=lines[i+8].split();
                    transition.append(trans1[1][2:-1])
                    transition.append(trans2[1][2:-1])
                    transition.append(trans3[1][2:-1])
                    graph_trans[k].append(transition[j])
                    graph_trans[k].append(transition[j+1])
                    graph_trans[k].append(transition[j+2])
                    k=k+1
                    j=j+3
                    print graph_trans
                elif tr1[0]=='next_state':
                    trans1=lines[i+2].split();
                    trans2=lines[i+4].split();
                    transition.append(trans1[1][2:-1])
                    transition.append(trans2[1][2:-1])
                    graph_trans[k].append(transition[j])
                    graph_trans[k].append(transition[j+1])
                    k=k+1;
                    j=j+2;
                
     
            elif y[0]=='next_state':
                transition.append(y[1][2:-1])
                graph_trans[k].append(states[k])
                graph_trans[k].append(transition[j])
                k=k+1;
                j=j+1;




graph_tuple=[tuple(l) for l in graph_trans[0:-1]]
#print graph_tuple

# draw_graph(states,graph_tuple)



f=Digraph('finite_state_machine',filename='fsm.gv',engine='circo') #dot,fdp,neato,circo
f.attr(randir='LR',size='8,5')
f.attr('node',shape='circle',splines='curved',len='5,0')

for edge in graph_tuple:
    print edge
    if len(edge)==2:
        f.edge(edge[0],edge[1])
    elif len(edge)==3:
        f.edge(edge[0], edge[1])
        f.edge(edge[0], edge[2])
    else:
    	f.edge(edge[0], edge[1])
        f.edge(edge[0], edge[2])
        f.edge(edge[0], edge[3])
		
f.view()
