from MSCLM_A import MSCLM_A
arpa_file_directory = 'text.arpa'
maximum_memory_usage_during_external_merge_sort = 500 # in MB
msclm_a = MSCLM_A(arpa_file_directory,maximum_memory_usage_during_external_merge_sort)
top_k = 5 # maximum report top 5 suggestions with high log probability to complete the sentence
# provide 'y' if you want to rebuild the sentence completion file data structure from arpa, otherwise give 'n'
inputs = ['আমি বাংলায় গান', 'আমার ভাইয়ের রক্তে', 'রঞ্জনা আমি আর', 'মোদের গর্ব', 'সে যে বসে', 'জয় বাংলা' , 'দিন দুনিয়ার','আমার সোনার বাংলা', 'বাবা মা কে', 'এবারের সংগ্রাম', 'মায়ের পায়ের নিচে']
f = open('test_result.txt','w',encoding='utf-8')
for input in inputs:
    result_object = msclm_a.SentenceCompletion(input,top_k) # A bangla sentence
    print(result_object)
    f.write('{\n')
    f.write('input:'+result_object['input']+'\n')
    f.write('suggestions:\n')
    f.write('[\n')
    for i in range(0,len(result_object['suggestions'])):
        f.write(str(result_object['suggestions'][i])+'\n')
    f.write(']\n')
    f.write('processing time:'+str(result_object['processing time'])+'\n')
    f.write('}\n')
    f.write('\n')
f.close()
# print status
msclm_a.PrintStatus()
