# POSSCORE

### Overview

POSSCORE is an automatic evaluation metric, which is described in the paper [POSSCORE: A Simple Yet Effective Evaluation of Conversational Search with Part of Speech Labelling](https://arxiv.org/pdf/2109.03039.pdf) (CIKM 2021).

If you find this repo useful, please cite:
```
@article{liu2021posscore,
  title={POSSCORE: A Simple Yet Effective Evaluation of Conversational Search with Part of Speech Labelling},
  author={Liu, Zeyang and Zhou, Ke and Mao, Jiaxin and Wilson, Max L},
  journal={arXiv preprint arXiv:2109.03039},
  year={2021}
}
```

### Installation
* Python version >= 3.6
* spaCy version >= 2.3

1. Install spaCy with pip by:

```sh
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

The more details about the installation of spaCy is shown in [spaCy](https://spacy.io/usage). 

Note: different versions of spaCy may influence the final posscore since the spaCy models may change in different versions. In the original paper, the version of spaCy we used is 2.3.

2. Install from pypi with pip by 

```sh
pip install posscore
```

### Usage
#### Python Function
```python
from posscore import scorer
s = scorer.POSSCORE() # init POSSCORE
s.get_posscore(str_reference, str_candidate)
```
Example:
```python
from posscore import scorer
s = scorer.POSSCORE() # init POSSCORE

reference = 'i like sports , football , hockey , soccer i also find swimming interesting as well .'
candidate1 = 'i like hockey and soccer . what teams do you support ?'
candidate2 = 'i have never swam competitively , but i did nt have it . i do like it though .'

print(s.get_posscore(reference, candidate1))
#output: 0.528
print(s.get_posscore(reference, candidate2))
#output: 0.178

```
The default POS tag list is ['ADJ', 'ADV', 'VERB', 'PROPN', 'NOUN'] (please see [the paper](https://arxiv.org/pdf/2109.03039.pdf)). You can also customize the selected tag list:
```python
from posscore import scorer
s = scorer.POSSCORE() # init POSSCORE
pos_tag_set = ['ADJ', 'VERB', 'PROPN', 'NOUN']
s.get_posscore(str_reference, str_candidate, pos_tag_set)

```

All the available POS tags in POSSCORE are introduced in [Universal POS tags](https://universaldependencies.org/docs/u/pos/).

