import os, sys, time
import subprocess
import turicreate
import random
import getopt


def usage():
  print (sys.argv[0] + " --graph <graph> --app <app> [--threads <threads>] [--verbose] [--pbsim]")
  print (sys.argv[0] + " -g <graph> -a <app> [-t <threads>] [-v] [-s]")
  print ("graph: wiki/twitter (default: wiki)")
  print ("app: pagerank/connectedcomp/graphcol/labelprop (default: pagerank)")
  print ("pbsim: simulation mode (default: no simulation)")

def do_load_graph_twitter():
  # Load data
  print "[PB]: Loading Twitter graph"
  if os.path.exists(data_w_path_edges):
    print "[PB]: Loading graph from local path"
    edges = turicreate.SFrame.read_csv(data_w_path_edges, header=False)
    edges = edges.rename({'X1':'src_node', 'X2':'dst_node'})
    print edges
  else:
    print "[PB-ERROR]: Can't find data! " + data_w_path_edges
    exit(1)

  if os.path.exists(data_w_path_nodes):
    print "[PB]: Loading graph from local path"
    nodes = turicreate.SFrame.read_csv(data_w_path_nodes, header=False)
    nodes = nodes.rename({'X1':'node_id'})
    print nodes
  else:
    print "[PB-ERROR]: Can't find nodes data! " + data_w_path_nodes
    exit(1)

  # Create graph 
  sg = turicreate.SGraph()
  sg = sg.add_vertices(nodes, vid_field='node_id')
  sg = sg.add_edges(edges, src_field='src_node', dst_field='dst_node')
  return sg

def do_load_graph_wiki():
  print "[PB]: Loading Wiki graph"
  if os.path.exists(data_w_path):
    print "[PB]: Loading graph from local path"
    sg = turicreate.load_sgraph(data_w_path)
  else:
    sg = turicreate.load_sgraph(url)
    sg.save(data_w_path)
  return sg

def init_label(vid):
  x = random.random()
  if x > 0.9:
    return 0
  elif x < 0.1:
    return 1
  else:
    return None

def do_prepare(sg, app):
  if app == "connectedcomp":
    print "[PB]: Running ConnectedComponents"
  elif app == "graphcol":
    print "[PB]: Running GraphColoring"
  elif app == "labelprop":
    print "[PB]: Running LabelPropagation"
    sg.vertices['labels'] = sg.vertices['__id'].apply(init_label, int)
  else:
    print "[PB]: Running PageRank"

def do_load_graph(graph):
  if graph == "twitter":
    return do_load_graph_twitter()
  else:
    return do_load_graph_wiki()


try:
  opts, args = getopt.getopt(sys.argv[1:], "hsg:a:t:v:p:o:", ["help", "graph=", "app=", "threads=", "pinpath=", "outdir="])
except getopt.GetoptError as err:
  # print help information and exit:
  print(err) # will print something like "option -a not recognized"
  usage()
  sys.exit(2)
graph='wiki'
app='pagerank'
verbose = False
threads = 20
for o, a in opts:
  if o in ("-v", "--verbose"):
    verbose = True
  elif o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-g", "--graph"):
    graph = a
  elif o in ("-a", "--app"):
    app = a
  elif o in ("-t", "--threads"):
    threads = int(a)
  elif o in ("-p", "--pinpath"):
    pinpath = a
  elif o in ("-o", "--outdir"):
    outpath = a
  else:
    assert False, "unhandled option"


home=pinpath + '/../../../apps/turi/'
data_file = 'US_business_links'
data_w_path=home + data_file

url = 'https://static.turi.com/datasets/' + data_file

home_twitter=home + 'Twitter-dataset/data/'
data_file_edges = 'edges.csv'
data_file_nodes = 'nodes.csv'
data_w_path_edges=home_twitter + data_file_edges
data_w_path_nodes=home_twitter + data_file_nodes

pid=str(os.getpid())
print "[PB]: My pid is " + pid

turicreate.config.set_runtime_config('TURI_DEFAULT_NUM_PYLAMBDA_WORKERS', threads)

sg = do_load_graph(graph)
do_prepare(sg, app)

f = None
p = subprocess.Popen('#PINPATH/pin -pid #PID -t #PINPATH/../../pintool_fast.so -num_buffers_per_app_thread 18 -num_processing_threads 1 -o #OPATH -debug_out 0 -emit_trace 0 -window_size 10 -record_byte 1 -instrument_reads 0'.replace('#PID', pid).replace('#PINPATH', pinpath).replace('#OPATH', outpath + '/' + graph + '/' + app + '/turi_' + app), shell = True, stdout = f, stderr = f)

if app == "connectedcomp":
  turicreate.connected_components.create(sg)
elif app == "graphcol":
  turicreate.graph_coloring.create(sg)
elif app == "labelprop":
  turicreate.label_propagation.create(sg, label_field='labels')
else:
  turicreate.pagerank.create(sg, max_iterations=10, verbose=verbose)

print "[PB]: Done"

