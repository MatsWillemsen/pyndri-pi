from collections import namedtuple
import os
from struct import unpack

class Index:
    def __init__(self, location):
        self.index = self.load_index(location)
        self.doc_index = open(os.path.join(location, 'document_index'), 'rb')
        self.data = open(os.path.join(location, 'data'), 'rb')
        self.term_index = open(os.path.join(location, 'term_index'),'rb')
        self.dictionary = open(os.path.join(location,'dictionary'), 'rb')
        self._fill_dictionary()
    
    def load_index(self, location):
        manifest = namedtuple('manifest', 'document_count unique_terms total_terms')
        contents = open(os.path.join(location, 'manifest'), 'rb').read()
        self.manifest = manifest._make(unpack('<QQQ', contents))
    
    def document(self, doc_id):
        self.doc_index.seek(doc_id * 4)
        location = unpack('<I',self.doc_index.read(4))[0]
        self.data.seek(location)
        id_len, term_len = unpack('<HI', self.data.read(6))
        ext_document_id = self.data.read(id_len).decode('utf-8')
        terms = tuple(unpack('<I', self.data.read(4))[0] for _ in range(term_len))
        return (ext_document_id, terms)
    
    def document_base(self):
        return 0
    
    def maximum_document(self):
        return self.manifest.document_count
    
    def document_count(self):
        return self.manifest.document_count
    
    def document_length(self, doc_id):
        self.doc_index.seek(doc_id * 4)
        location = unpack('<I',self.doc_index.read(4))[0]
        self.data.seek(location)
        id_len, term_len = unpack('<HI', self.data.read(6))
        return term_len
    
    def total_terms(self):
        return self.manifest.total_terms
    
    def unique_terms(self):
        return self.manifest.unique_terms
    
    def term_count(self, term):
        return self.term_frequencies[term]

    def _fill_dictionary(self):
        self.token2id = {}
        self.id2token = {}
        self.id2df = {}
        self.term_frequencies = {}
        for x in range(self.manifest.unique_terms):
            dict_pos, token_len, id_df, termcount = unpack('<IHII', self.term_index.read(14))
            self.dictionary.seek(dict_pos)
            token = self.dictionary.read(token_len).decode('utf-8')
            self.token2id[token] = x
            self.id2token[x] = token
            self.id2df[x] = id_df
            self.term_frequencies[x] = termcount

    def get_dictionary(self):
        return self.token2id, self.id2token, self.id2df
    
    def get_term_frequencies(self):
        return self.term_frequencies