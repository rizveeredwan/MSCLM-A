# MSCLM-A: Memory flexible language independent Sentence Completion using Language Model based on Arpa file.
- Memory flexible lanugage independent sentence completion using language model based on simply arpa file. 
- Main facility of this repository is the whole sentence completion operation is efficiently performed using Disk based operations and dependency over physical memory is significantly reduced. The solution is efficient in resource constrained environment along with having least depedency over external libraries.

## Algorithm 
- Based on the provided arpa file, a sorted file data structure and a word index file is built. 
- Using external merge sort the sorted file data structure is built. Users can provide the maximum physical memory usage in this regard.  
- The implementation is stateful which means upon loading you can perform multiple queries. The sorted file data structure and word index file need to be built only once from arpa file. 

## Complexity Analysis 
 - Suppose, the apra file contained total `N` number of word combinations and the data is chunked into three files containing ``n1``,``n2`` and ``n3`` number of combinations. Each chunk is sorted in ``O(nlogn)`` complxity and written in temporary file in ``O(n)`` complexity. Final external merge sort complexity is ``O(NlogN)``.
 - Probability searching during query is disk and word pointer based. Efficiently redundant bytes are skipped and searching is performed. 

## Requirements
``` 
python 3.x 
```

``` 
Trained Arpa file generated through a LM 
```

## Installation 
Base and python libraries should be enough. Used libraries 
- sys, os, functools, queue, platform, time.
- Trained Arpa file: [Arpa File Url](https://drive.google.com/file/d/1wjERbp4EYv7BCFAZ0DR908VgRiT_WNew/view?usp=sharing). Unzip it during usage.
- Just simply clone this repository using 
```
git clone https://github.com/rizveeerprojects/MSCLM-A.git
```

## Usage 
### How to run 
```python
from MSCLM_A import MSCLM_A
arpa_file_directory = 'text.arpa'
maximum_memory_usage_during_external_merge_sort = 500 # in MB
msclm_a = MSCLM_A(arpa_file_directory,maximum_memory_usage_during_external_merge_sort)
top_k = 5 # maximum report top 5 suggestions with high log probability to complete the sentence
# provide 'y' if you want to rebuild the sentence completion file data structure from arpa, otherwise give 'n'
result_object = msclm_a.SentenceCompletion('আমার সোনার বাংলা',top_k) # A bangla sentence
print(result_object)
```
See [example.py](./example.py) for more.  

### See Consumption Status 
```python
# print status
msclm_a.PrintStatus()
```
### Returned suggestions 
```
{
'input': 'আমার সোনার বাংলা', 
'suggestions': [[-6.6096342770000005, 'আমার সোনার বাংলা আমি তোমায়'], 
                [-6.643474670000001, 'আমার সোনার বাংলার মানুষগুলো যেন'], 
                [-6.643531660000001, 'আমার সোনার বাংলার বীরেরা </s>'], 
                [-6.64698682, 'আমার সোনার বাংলা আবার কলঙ্কিত'], 
                [-6.647443705000001, 'আমার সোনার বাংলা ভুলিনি তোমায়']], 
'processing time': 1.15625
}
```
In each suggestion, first value indicates the log probability of the complete sentence if this suggestion is added. The second value is the suggestion. ``</s>`` indicates sentence completion is expected. 'processing time' indicates the time in seconds to perform the disk based query. 

## Useful links 
- KENLM: https://github.com/kpu/kenlm 
- N-gram probability calculation: https://masatohagiwara.net/training-an-n-gram-language-model-and-estimating-sentence-probability.html 

## Contributors 
[Redwan Ahmed Rizvee](https://www.linkedin.com/in/redwan-ahmed-rizvee-303b68133/). 
For your queries or suggestion mail at (rizveeredwan.csedu@gmail.com) or create issue.
Special thanks to [Muntasir Wahed](https://www.linkedin.com/in/immuntasir/) to help me in raw data collection and preprocessing along with introducing to me to kenlm. Also thanks to Shakur Shams Mullick who asked the question and from where the work was motivated.

## Citation 
Please cite this repository if you are using this to generate suggestion. Also cite [kenlm](https://kheafield.com/code/kenlm/) if you use it to generate the trained Arpa file from your sentence corpus.
