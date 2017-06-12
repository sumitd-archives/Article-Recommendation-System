import gensim
import pickle
import time
from gensim.corpora import MmCorpus 
print time.strftime('%X %x %Z');
fp = open("./_bow.mm", 'rb')
lda = gensim.models.ldamodel.LdaModel.load('lda_model.out' , mmap='r');
bow_array = MmCorpus('./_bow.mm');
tdfp = open("topic_dist.out", 'w');
index = 0;
global_bow = [];
local_bow = [];
batch_documents = [];
max_size = 25000;
first_commit = True;
while 1:
    try:
        #print index;
        local_bow = bow_array[index];
        #print local_bow;
        #print '\n\n';
        complete_dist = [];
        curr_key = 0;
        try:
            topic_dist = lda[local_bow];
            for key,val in topic_dist:
                while (curr_key < key):
                    complete_dist.append((curr_key, 0));
                    curr_key += 1;
                complete_dist.append((key, val));
                curr_key += 1;
            while (curr_key < 100):
                complete_dist.append((curr_key, 0));
                curr_key += 1;
            
            batch_documents.append(complete_dist);
            if len(batch_documents) >= max_size:
                pickle.dump(batch_documents, tdfp);
                if first_commit: 
                    print time.strftime('%X %x %Z');
                    first_commit = False;
                batch_documents = [];
           #print index;
        except:
            index += 1;
            continue;
            #print cur_doc_num;
        local_bow= [];
    except:
        print "outer break"
        print index;
        break;
    index += 1;

if len(batch_documents) > 0:
    pickle.dump(batch_documents, tdfp);
    batch_documents = [];
tdfp.close();
print "index = ";
print index;
print '\n';
tdfp_i = open("topic_dist.out", 'rb');
print len(pickle.load(tdfp_i));
print '\n';
#while 1:
#    try:
#        global_bow.append(pickle.load(tdfp_i));
#    except (EOFError):
#        break;
#tdfp_i.close();
#print "\n\n";
#print len(global_bow);
print time.strftime('%X %x %Z')
#print global_bow;
#    print topic_dist;
