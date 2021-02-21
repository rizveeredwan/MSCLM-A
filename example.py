from MSCLM_A import MSCLM_A

# input parameters
arpa_file_directory = 'text.arpa'
maximum_memory_usage_during_external_merge_sort = 500 # in MB
punctuation_dependency =  False # no punctuation is kept and and considered there is no punctuation in the input sentence
top_k = 5 # maximum report top 5 suggestions with high log probability to complete the sentence

# object creation
msclm_a = MSCLM_A(arpa_file_directory,maximum_memory_usage_during_external_merge_sort)

# query code
input = 'রঞ্জনা আমি আর'
result_object = msclm_a.SuggestionGeneration(input,top_k,punctuation_dependency) # A bangla sentence
print(result_object)

# print consumption status
msclm_a.ConsumptionStatistics()
