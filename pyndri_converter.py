import struct
from collections import Counter
import os
import pyndri


class IndriConverter:
    def __init__(self, location):
        self.location = location
    
    def load_index(self):
        self.index = pyndri.Index(self.location)
        self.documents = {}
        for docid in range(self.index.document_base(), self.index.maximum_document()):
            docid, terms = self.index.document(docid)
            self.documents[docid] = terms

        self.dictionary = self.index.get_dictionary()
        

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
            for term in terms:
                termcount[term] += 1
        token2id, id2token, id2df = self.dictionary
        for token, tokenid in token2id.items():
            term_index.write(struct.pack('<IHII', dictionary.tell(), len(token), id2df[tokenid], termcount[tokenid]))
            dictionary.write(token.encode('utf-8'))
            dictionary.flush()
        data.close()
        doc_index.close()
        term_index.close()