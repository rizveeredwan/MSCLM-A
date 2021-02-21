# next word suggestion generation using KENLM
# requirement: An Arpa File

# libraries
import sys
from os import path,mkdir,listdir,remove,rename
import functools
import queue
import platform
from time import process_time

def compare(list1,list2):
    if(list1<list2):
        return -1
    elif(list1>list2):
        return 1
    return 0

class WordTrie:
    def __init__(self,prob,backoff_weight, ptr):
        self.child={}
        self.prob=prob
        self.ptr=ptr
        self.backoff_weight = backoff_weight

class MSCLM_A:
    def __init__(self,arpa_file_directory,memory_usage):
        self.python_version = self.GetPythonVersion()
        # apra file directory: after training using KENLM, probabilities will be stored here
        self.arpa_file_directory = arpa_file_directory
        self.n_gram = 0 # number of grams in arpa file
        if(path.exists('Tmp/sorted_lm_data.txt') and path.exists('Tmp/word_pointers.txt')):
            while True:
                v = input("Required files are already found. Do you want to build again?(y/n): ")
                if(v.strip().lower() == 'y'):
                    self.ArpaFileCheck()
                    print("Arpa to sorted text conversion started")
                    self.ArpaToText_ExternalFileSort(memory_usage) # 500*1024.0
                    print("Arpa to sorted text conversion completed")
                    print("Found {} gram".format(self.n_gram))
                    break
                elif(v.strip().lower() == 'n'):
                    print("using previously prepared files")
                    self.ExtractingNGram()
                    print("Found {} gram".format(self.n_gram))
                    break
                else:
                    print("input not properly given.")
        else:
            self.ArpaFileCheck()
            print("Arpa to sorted text conversion started")
            self.ArpaToText_ExternalFileSort(500*1024.0)
            print("Arpa to sorted text conversion completed")
            print("Found {} gram".format(self.n_gram))
        # word pointer memory and time consumption
        self.word_ptr_memory = 0
        self.word_ptr_read_time_consumption = 0
        # sorted file DS time consumption
        self.sorted_file_build_up_time_consumption = 0
        self.trie_root=WordTrie(0,0,0)
        self.SearchInit()

    def MergeSortFiles(self,file_names,number_of_comb):
        line_end_character = 1
        if(platform.system() == 'Windows'):
            line_end_character = 2
        q = queue.PriorityQueue()
        for file_name in file_names:
            f = open(file_name,'r',encoding='UTF-8')
            line = f.readline()
            if(line != ""):
                q.put([line.strip(),f,len(line.strip().split(" "))])
        final_file = open('Tmp/sorted_lm_data.txt','w',encoding='UTF-8')
        word_ptr_file = open('Tmp/word_pointers.txt','w',encoding='utf-8')
        byte_count = 0
        ct = 0
        percentage_read = [0,10,20,30,40,50,60,70,80,90,100]
        ptr_per_read = 1
        while q.empty() == False:
            small = 0
            u = q.get()
            final_file.write(u[0]+'\n')
            if(u[2]==3): # single word
                word_ptr_file.write(u[0]+" "+str(byte_count)+'\n')
            byte_count = byte_count + len(u[0].encode('utf-8'))+line_end_character
            line = u[1].readline()
            if(line != ""):
                q.put([line.strip(),u[1],len(line.strip().split(" "))])
            ct = ct + 1
            if((ct*100.0)/number_of_comb >= percentage_read[ptr_per_read]):
                print("Merging completed for {}%".format(percentage_read[ptr_per_read]))
                ptr_per_read = 1+ptr_per_read
        final_file.close()
        word_ptr_file.close()

    def ExtractingNGram(self):
        try:
            init_block=False
            line = ""
            self.n_gram=0
            # file split and individual file sort
            with open(self.arpa_file_directory,'rb') as i_f:
                for line in i_f:
                    try:
                        line = line.decode('utf-8')
                    except Exception as e:
                        print("error = ",e)
                        continue
                    try:
                        l = line.strip()
                        l = l.split(' ')
                        # print(l)
                    except Exception as e:
                        print("error = ",e)
                        continue
                    if(l[0] == '\data\\'):
                        init_block = True
                    elif(l[0] == 'ngram' and init_block == True):
                        # init block
                        self.n_gram = self.n_gram+1
                    else:
                        break
                i_f.close()
        except Exception as e:
            print(e)

    def ArpaToText_ExternalFileSort(self, threshold):
        self.sorted_file_build_up_time_consumption = process_time()
        if(path.exists('Tmp/')):
            for files in listdir('Tmp/'):
                remove('Tmp/'+files)
            remove('Tmp/')
            mkdir('Tmp')
        else:
            mkdir('Tmp')
        try:
            data_block,init_block=False,False
            ct = 0
            number_of_comb = 0
            percentage_read = [0,10,20,30,40,50,60,70,80,90,100]
            ptr = 1
            size_cal = 0
            line = ""
            data = []
            file_names = []
            index = 0
            f_ptr = open('Tmp/temp_'+str(index)+'.txt','w',encoding='utf-8')
            file_names.append('Tmp/temp_'+str(index)+'.txt')
            # file split and individual file sort
            q=queue.PriorityQueue()
            with open(self.arpa_file_directory,'rb') as i_f:
                for line in i_f:
                    ct = ct + 1
                    if(number_of_comb>0):
                        per = (ct * 100.0)/(number_of_comb)
                        if(ptr<len(percentage_read) and per >= percentage_read[ptr]):
                            print("Completed Reading (%) = ",percentage_read[ptr])
                            ptr = ptr + 1
                    try:
                        line = line.decode('utf-8')
                    except Exception as e:
                        print("error = ",e)
                        continue
                    try:
                        l = line.strip()
                        l = l.split(' ')
                        # print(l)
                    except Exception as e:
                        print("error = ",e)
                        continue
                    if(l[0] == '\data\\'):
                        init_block = True
                    elif(l[0] == '\end\\'):
                        while (q.empty()==False):
                            l = q.get()
                            f_ptr.write(l)
                        f_ptr.close()
                        print('Tmp/temp_'+str(index)+'.txt is sorted and written')
                        break
                    if(l[0] == 'ngram' and init_block == True):
                        # init block
                        number_of_comb = number_of_comb + int(int(l[1].split('=')[1]))

                    elif('-grams' in l[0]):
                        # data block
                        init_block == False
                        data_block = True
                        desired_n = int(l[0].split('-grams')[0].split('\\')[1])
                        self.n_gram = desired_n
                    elif(data_block == True):
                        try:
                            l = line.strip()
                            l = l.replace('\t'," ")
                            l = l.split(" ")
                            prob = float(l[0].strip())
                            prob = str(prob)
                            try:
                                backoff_weight = str(float(l[len(l)-1].strip()))
                                # print("bk off = ",backoff_weight)
                            except Exception as e:
                                backoff_weight = str(0)

                            line = ""

                            for i in range(1,desired_n+1):
                                if(i==1):
                                    line = l[i].strip()
                                else:
                                    line = line + " " +l[i].strip()
                            line = line + " "+prob+" "+backoff_weight+'\n'
                            size_cal = size_cal + sys.getsizeof(line)
                            #print("size cal = ",size_cal/1024.0,threshold)
                            if((size_cal/1024.0)>threshold):
                                while (q.empty()==False):
                                    l = q.get()
                                    f_ptr.write(l)
                                f_ptr.close()
                                print('Tmp/temp_'+str(index)+'.txt is sorted and written')
                                size_cal = sys.getsizeof(line)
                                index = index + 1
                                f_ptr = open('Tmp/temp_'+str(index)+'.txt','w',encoding='utf-8')
                                file_names.append('Tmp/temp_'+str(index)+'.txt')
                                data.clear()
                            q.put(line)
                        except Exception as e:
                            print(e)

                f_ptr.close()
            # merge sort
            print("Merging started")
            self.MergeSortFiles(file_names,number_of_comb)
            for i in file_names:
                remove(i)
            del file_names
            self.sorted_file_build_up_time_consumption = process_time() - self.sorted_file_build_up_time_consumption

        except Exception as e:
            print("error = ",e)
            raise Exception(e)

    def FindingNextWord(self,word_group,byte_count,previous_prob,top_k):
        sentence = " ".join([i for i in word_group])
        sentence = sentence.strip()
        #debug: print("sentence ",sentence,byte_count,previous_prob)
        q = queue.PriorityQueue()
        try:
            f = open('Tmp/sorted_lm_data.txt','rb')
            f.seek(byte_count,0)
            byte = f.readline() # reading current line
            string = byte.decode('utf-8')
            while True:
                byte = f.readline()
                string = byte.decode('utf-8')
                if(sentence in string):
                    line = string.strip().split(" ")
                    sen = " ".join([line[i] for i in range(0,len(line)-2)])
                    sen = sen.strip()
                    prob = float(line[len(line)-2])
                    q.put([abs(previous_prob)+abs(prob),sen])
                else:
                    break
            f.close()
            res = []
            while q.empty()!=True:
                u = q.get()
                u[0] = u[0]*-1.0
                res.append([u[0],u[1]])
                if(len(res) == top_k):
                    break
            return res
        except Exception as e:
            print(e)
            return []

    def CheckAlreadyCalculate(self,words):
        prob,start_ptr=None,None
        trie_node = self.trie_root
        idx = 0
        while True:
            next = trie_node.child.get(words[0].strip())
            if( next != None):
                idx = idx + 1
                if(idx == len(words)):
                    return next.prob,next.backoff_weight,next.ptr
                trie_node = next
            else:
                return None,None,None

    def FindProbabilityOfNGram(self,words):
        # print(words)
        # trimming the n-gram
        known_words=[]
        sz = len(words)
        for i in range(len(words)-1,-1,-1):
            if(self.trie_root.child.get(words[i]) != None):
                known_words.append(words[i])
            else:
                break
        known_words.reverse()
        words = known_words
        if(len(words) == 0): # no ngram solution is possible
            return None,None,None,sz

        # finding the start pointer to search
        sz = len(words)
        start_ptr = None
        prob = None
        prob,backoff_weight,start_ptr = self.CheckAlreadyCalculate(words)
        if(prob != None):
            return prob,backoff_weight,start_ptr,sz
        for i in range(len(words)-2,-1,-1):
            prob,backoff_weight,start_ptr = self.CheckAlreadyCalculate(words[0:i+1])
            if(prob != None):
                break
        if(start_ptr == None):
            return None,None,None,sz

        # got a start ptr to work on
        word_string1 = " ".join([words[i] for i in range(0,len(words))])
        word_string1 = word_string1.strip()
        f = open('Tmp/sorted_lm_data.txt','rb')
        f.seek(start_ptr,0) # previous data is read and omitted
        byte = f.readline() # current gram is read
        start_ptr = start_ptr + len(byte) # pointer is shifted
        while True:
            try:
                byte = f.readline() # possible candidate
                string = byte.decode('utf-8')
                if(string == ""): # whole file reading is complete
                    f.close()
                    return None,None,None,sz
                string = string.strip().split(" ")
                word_string2 = " ".join([string[i] for i in range(0,len(string)-2)])
                word_string2 = word_string2.strip()
                if(word_string2 == word_string1):
                    prob = float(string[len(string)-2])
                    f.close()
                    return prob,backoff_weight,start_ptr,sz
                elif(word_string2 < word_string1):
                    start_ptr = start_ptr + len(byte)
                elif(word_string2 >word_string1):
                    return None,None,None,sz
            except Exception as e:
                print(e)
                return None,None,None,sz
        f.close()

    def SearchInit(self):
        self.word_ptr_read_time_consumption = process_time()
        fw = open('Tmp/word_pointers.txt','r',encoding='UTF-8')
        print("loading pointer informations")
        f = open('Tmp/sorted_lm_data.txt','rb')
        for line in fw:
            l = line.strip().split(" ")
            assert(len(l)==4)
            v = WordTrie(float(l[1].strip()),float(l[2].strip()),int(l[3])) #prob, backoff_weight, byte offset
            self.trie_root.child[l[0].strip()]=v
        self.word_ptr_memory = sys.getsizeof(self.trie_root)/(1024.0*1024.0)
        self.word_ptr_read_time_consumption = process_time() - self.word_ptr_read_time_consumption
        print("pointer information loading completed.")


    def BackoffAddNecessary(self,len_words,i,last_succ_n_gram_len):
        max_possible_n_gram = i-max(0,i-self.n_gram+1)+1
        if(last_succ_n_gram_len == max_possible_n_gram): # exact probability for n gram is calculated
            return False
        return True # exact is not calculated, smaller gram is considered

    def SentenceCompletion(self,sentence,top_k):
        starting_time = process_time()
        words = sentence.strip().split(" ")
        total_prob = 0
        prob,start_ptr = None,None
        last_succ_n_gram_len = self.n_gram-1
        for i in range(0,len(words)):
            j = min(self.n_gram,last_succ_n_gram_len)+1
            while (j>0):
                #debug: print("j = ",j,words[max(0,i-j+1):i+1])
                prob,backoff_weight,start_ptr,last_succ_n_gram_len = self.FindProbabilityOfNGram(words[max(0,i-j+1):i+1])
                # print(prob,backoff_weight,start_ptr,last_succ_n_gram_len)
                if(prob != None):
                    total_prob = total_prob + prob
                    if(self.BackoffAddNecessary(len(words),i,last_succ_n_gram_len)): # shorter n-gram is calculated, so adding backoff_weight
                        total_prob = total_prob + backoff_weight
                    break
                else:
                    j = last_succ_n_gram_len-1

            if(prob == None):
                #debug: print(["<unk>"])
                prob,backoff_weight,start_ptr,last_succ_n_gram_len = self.FindProbabilityOfNGram(['<unk>'])
                total_prob = total_prob + prob
                last_succ_n_gram_len = 0
                total_prob = total_prob + backoff_weight
                #debug: print("prob = ",prob)
        try:
            result = self.FindingNextWord(words[max(0,len(words)-last_succ_n_gram_len):len(words)],start_ptr,total_prob,top_k)
            end_time = process_time()
            result_object={}
            result_object['input'] = sentence
            result_object['suggestions'] = result
            result_object['processing time'] = end_time-starting_time
            return result_object
        except Exception as e:
            # debug: print(e)
            end_time = process_time()
            result_object={}
            result_object['input'] = sentence
            result_object['suggestions'] = []
            result_object['processing time'] = end_time-starting_time
            return result_object

    def ArpaFileCheck(self):
        file_name = self.arpa_file_directory.split('.')
        if(len(file_name)>0 and file_name[len(file_name)-1].lower() == 'arpa'):
            if(path.exists(self.arpa_file_directory) == False):
                raise Exception("Arpa File Not Found")
                sys.exit(0)
        else:
            raise Exception("File Extension is not 'arpa'")
            # exiting the system
            sys.exit(0)
    def GetPythonVersion(self):
        return sys.version_info
    def PrintStatus(self):
        print("Memory usage by word pointer trie: {} MB".format(self.word_ptr_memory))
        print("Time usage to build word pointer trie {} seconds".format(self.word_ptr_read_time_consumption))
        print("File Search space processing time {} seconds".format(self.sorted_file_build_up_time_consumption))
