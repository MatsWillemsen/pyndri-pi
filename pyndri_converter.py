import struct
from collections import Counter, OrderedDict
import os
import pyndri


class IndriConverter:
    def __init__(self, location):
        self.location = location
    
    def load_index(self):
        self.index = pyndri.Index(self.location)
        self.documents = OrderedDict()
        for docid in range(self.index.document_base(), self.index.maximum_document()):
            docid, terms = self.index.document(docid)
            self.documents[docid] = terms
        self.dictionary = self.index.get_dictionary()
        self.term_frequencies = self.index.get_term_frequencies()
        

    def save_index(self, location):
        os.chdir(location)
        with open('manifest', 'wb') as manifest:
            manifest.write(struct.pack('<QQQ', self.index.document_count(), self.index.unique_terms(), self.index.total_terms()))
        data = open('data', 'wb')
        doc_index = open('document_index', 'wb')
        term_index = open('term_index', 'wb')
        dictionary = open('dictionary', 'wb')
        termcount = Counter()
        for docid, terms in self.documents.items():
            doc_index.write(struct.pack('<I', data.tell()))
            data.write(struct.pack('<HI', len(docid), len(terms)))
            data.write(docid.encode('utf-8'))
            data.write(struct.pack('<{}I'.format(len(terms)), *terms))
            data.flush()
        token2id, id2token, id2df = self.dictionary
        for token, tokenid in sorted(token2id.items(), key=lambda x: x[1]):
            term_index.write(struct.pack('<IHII', dictionary.tell(), len(token), id2df[tokenid], self.term_frequencies[tokenid]))
            dictionary.write(token.encode('utf-8'))
            dictionary.flush()
        data.close()
        doc_index.close()
        term_index.close()

converter = IndriConverter('/Users/mats/OneDrive/Persoonlijk/Studie/MSc Information Studies/Structured Unstructured/index')
converter.load_index()
converter.save_index('converted_ordered/')