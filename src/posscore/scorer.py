from .tokenizers import clean_str
import string
import spacy
import gensim
import gensim.downloader as api
from gensim.utils import simple_preprocess

import numpy as np
from numpy import dot
from numpy.linalg import norm

import math


class POSSCORE:

    def __init__(self):
        print('=======loading embedding=========')
        self.nlp = spacy.load("en_core_web_sm")
        self.embedding_model = api.load("fasttext-wiki-news-subwords-300")
        print('=======complete embedding initialization======')
    
    def __preprocess(self, sentence):
        s = clean_str(sentence.strip())
        temp_s = s.translate(str.maketrans('', '', string.punctuation)) # remove punctuation\n",
        return temp_s

    def __extract_pos_pair(self, sentence):
        doc = self.nlp(sentence)
        res = []
        for w in doc:
            res.append(w.text + '__$$__' + w.pos_)
        return res


    def __get_sent_vector(self, sentence):
        words = [w for w in sentence if w in self.embedding_model.vocab]
        if len(words) >= 1:
            return np.mean(self.embedding_model[words], axis=0)
        else:
            return []
    
    def __get_ea_score(self, ref_text_list, cand_text_list):
        res = None
        temp_ref = ' '.join(ref_text_list)
        temp_cand = ' '.join(cand_text_list)
        ref_mean_matrix = self.__get_sent_vector(simple_preprocess(temp_ref))
        cand_mean_matrix = self.__get_sent_vector(simple_preprocess(temp_cand))
        
        if(len(ref_mean_matrix) == len(cand_mean_matrix) and len(cand_mean_matrix) > 0):
            res = dot(ref_mean_matrix, cand_mean_matrix)/(norm(ref_mean_matrix) * norm(cand_mean_matrix))
        else:
            res = None
        return res
        
    def __split_text_pos_list(self, pair_list, tag_set):
        text_pos_list = []
        text_nonpos_list = []
        tag_pos_list = []
        tag_nonpos_list = []
        
        
        for item in pair_list:
            text, pos = item.split('__$$__')
            if(pos in tag_set):
                text_pos_list.append(text)
                tag_pos_list.append(pos)
            else:
                text_nonpos_list.append(text)
                tag_nonpos_list.append(pos)
        return (text_pos_list, text_nonpos_list, tag_pos_list, tag_nonpos_list)
    
    
    def __weight_fun(self, ref_tag_list, cand_tag_list, ref_len, cand_len):
        r_ref = len(ref_tag_list) / ref_len
        r_cand = len(cand_tag_list) / cand_len
        res = math.exp(1 - r_ref / r_cand)
        return res

    def get_posscore(self, reference, candidate,  pos_tag_set=['ADJ', 'ADV', 'VERB', 'PROPN', 'NOUN']):
        score = None
    
        ref_pair_list = self.__extract_pos_pair(self.__preprocess(reference))
        cand_pair_list = self.__extract_pos_pair(self.__preprocess(candidate))
        
        ref_len = len(ref_pair_list)
        cand_len = len(cand_pair_list)
        
        if(ref_len > 0 and cand_len > 0):
            ref_info = self.__split_text_pos_list(ref_pair_list, pos_tag_set)
            cand_info = self.__split_text_pos_list(cand_pair_list, pos_tag_set)
        
            pos_score = self.__get_ea_score(ref_info[0], cand_info[0])
            nonpos_score = self.__get_ea_score(ref_info[1], cand_info[1])
            
            pos_weight = 1
            
            if(pos_score == None):
                pos_score = 0
            if(nonpos_score == None):
                nonpos_score = 0
            if(len(cand_info[2]) > 0 and len(ref_info[2]) > 0):    
                pos_weight = self.__weight_fun(ref_info[2], cand_info[2], ref_len, cand_len)
            
            score = pos_weight * pos_score + 1.0 * nonpos_score
        
        return score

if __name__ == '__main__':
    pos_tag_set = ['ADJ', 'ADV', 'VERB', 'PROPN', 'NOUN']
    reference = 'i like sports , football , hockey , soccer i also find swimming interesting as well .'
    candidate1 = 'i like hockey and soccer . what teams do you support ?'
    candidate2 = 'i have never swam competitively , but i did nt have it . i do like it though .'
    pos = POSSCORE()
    a = pos.get_posscore(reference, candidate1, pos_tag_set)
    b = pos.get_posscore(reference, candidate2, pos_tag_set)
    print(a)


