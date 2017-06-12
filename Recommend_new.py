import pickle
import time
import sys
import numpy as np;
from sklearn.decomposition import PCA, FactorAnalysis
import MinHeap as mh;
import Node;
import random;
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from math import*

print time.strftime('%X %x %Z');
in_fp = open("topic_dist.out", 'rb');
n_doc = 0;
result = [];
total_docs = 100000;
n_dim = 100;
test_size = 1000;
i = 0;
n_iter = 0;
n_docs_per_iter = 100000;

def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)
      
def FindCosineSim(x,y):
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

k_nearest = 10;
n_random_pts = 100;
x = np.zeros((n_random_pts, n_dim), dtype=np.float);
y = np.zeros((total_docs, n_dim), dtype=np.float);

ind_fp = open('topic_indexes1.txt' , 'r')
random_pts = [];
for line in ind_fp:
    index = long(line) - 1;
    random_pts.append(index);
    random_pts.sort();

output = np.zeros((n_random_pts, k_nearest + 1) , dtype = np.long);
min_heaps = [];

for i in xrange(n_random_pts):
    output[i][0] = random_pts[i];
    min_heaps.append(mh.MinHeap());

t_i = 0
f_i = 0;
total_iterations = 20;
one_cycle_iterations = 4;

rand_i = 0;
while t_i < total_iterations:
    i = 0;
    f_i = 0;
    while f_i < one_cycle_iterations:
        try:
            doc = pickle.load(in_fp);
            n_iter += 1;
            n_doc = len(doc);
            #n_doc = total_docs
            doc_i = 0;
            while doc_i < n_doc:
                if random_pts[rand_i] == i + n_docs_per_iter*t_i:
                    j = 0;
                    for key,val in doc[doc_i]:
                        x[rand_i][j] = val;
                        j+=1;
                    rand_i += 1;
                    print rand_i;
                i+=1;
                doc_i+=1;
        except:
            break;
        f_i += 1;
    t_i += 1;

print "finished finding random points."

in_fp.close();
in_fp = open("topic_dist.out", 'rb');

t_i = 0;
while t_i < total_iterations:
    i = 0;
    f_i = 0;
    while f_i < one_cycle_iterations:
        try:
            doc = pickle.load(in_fp);
            n_iter += 1;
            n_doc = len(doc);
            #n_doc = total_docs
            doc_i = 0;
            while doc_i < n_doc:
                j = 0;
                for key,val in doc[doc_i]:
                    y[i][j] = val;
                    j+=1;
                i+=1;
                doc_i+=1;
        except:
            break;
        f_i += 1;

    for rand_i in xrange(n_random_pts): 
        min_heap = min_heaps[rand_i];
        a = x[rand_i];
        r_pt = random_pts[rand_i];
        for j in xrange(i):
            if (r_pt == j + n_docs_per_iter*t_i):
                continue;
            b = y[j];
            cosine_sim = FindCosineSim(a, b);
            heap_size = min_heap.GetSize();
            if heap_size < k_nearest:
                node = Node.Node(cosine_sim, j + n_docs_per_iter*t_i);
                min_heap.AddElements(node);
            else:
                head = min_heap.ReturnHead();
                if cosine_sim > head.GetKey():
                    node = Node.Node(cosine_sim, j + n_docs_per_iter*t_i);
                    #print "popped = " , head.GetValue() , " , added = " , j;
                    min_heap.AddAtHead(node);
           # min_heap.PrintElements(); 
            #print '\n';
    print 'iteration 0 completed : '  ,
    print time.strftime('%X %x %Z');
    t_i += 1;

for rand_i in xrange(n_random_pts):
    print  'heap = ' , rand_i , 'size = ' , min_heap.GetSize();
    min_heap = min_heaps[rand_i];
    #print 'min_heap : ' , rand_i , ' , size = ' , min_heap.GetSize();
    for col in range(1, 11):
        node = min_heap.pop();
        #print node.GetKey() , ' , ' , node.GetValue();
        output[rand_i][col] = node.GetValue();
    rand_i += 1;
print output[0:5];

#fp_o = open('file_array' , 'w');
#print output[0:10];
np.save('output.npy', output);
#fp_i = open('file_array.npy' , 'rb');
#y =  np.load(fp_i);
#print y;
#print y[1];
#print y[2];
#print y[3];
print time.strftime('%X %x %Z');
