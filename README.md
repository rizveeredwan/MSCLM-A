# MSCLM-A
- Memory flexible lanugage independent sentence completion using language model based on simply arpa file. 
- Main facility of this repository is the whole sentence completion operation is efficiently performed using Disk based operations and dependency over physical memory is significantly reduced. 

## Algorithm 
- Based on the provided arpa file, a sorted file data structure and a word index file is built. 
- Using external merge sort the sorted file data structure is built. Users can provide the maximum physical memory usage in this regard.  
- The implementation is stateful which means upon loading you can perform multiple queries. 

## Requirements
``` 
python 3.x 
```

``` 
Trained Arpa file generated through a LM 
```

## Installation 
Base and python libraries should be enough. Used libraries 
- sys, os, functools, queue, platform
- Trained Arpa file: [Arpa File Url](https://drive.google.com/file/d/1wjERbp4EYv7BCFAZ0DR908VgRiT_WNew/view?usp=sharing). Unzip it during usage.

## Usage 
```python
from MSCLM_A import MSCLM_A
arpa_file_directory = 'text.arpa'
maximum_memory_usage_during_external_merge_sort = 500 # in MB
msclm_a = MSCLM_A(arpa_file_directory,maximum_memory_usage_during_external_merge_sort)
# provide 'y' if you want to rebuild the sentence completion file data structure from arpa, otherwise give 'n'
print(msclm_a.SentenceCompletion('আমি বাংলায় গান')) # A bangla sentence
```
See [example.py](./example.py) for more.  

## Useful links 
- KENLM: https://github.com/kpu/kenlm 
- N-gram probability calculation: https://masatohagiwara.net/training-an-n-gram-language-model-and-estimating-sentence-probability.html 

## Contributors 
[Redwan Ahmed Rizvee](https://www.linkedin.com/in/redwan-ahmed-rizvee-303b68133/). 
For your queries or suggestion mail at (rizveeredwan.csedu@gmail.com) or pull issue.

## Citation 
Please cite this repository if you are using this to generate suggestion. Also cite [kenlm](https://kheafield.com/code/kenlm/) if you use it to generate the trained ARPA file from your sentence corpus.
