# -*- coding: utf-8 -*-
from nltk.corpus.reader.wordnet import WordNetCorpusReader
class JapaneseWordNetCorpusReader(WordNetCorpusReader):
    def __init__(self, root, filename):
        WordNetCorpusReader.__init__(self, root, root)
        import codecs
        f=codecs.open(filename, encoding="utf-8")
        self._jword2offset = {}
        for line in f:
            _cells = line.strip().split('\t')
            _offset_pos = _cells[0]
            _word = _cells[1]
            if len(_cells)>2: _tag = _cells[2]
            _offset, _pos = _offset_pos.split('-')
            try:
              self._jword2offset[_word].append({'offset': int(_offset), 'pos': _pos})
            except:
              self._jword2offset[_word]=[{'offset': int(_offset), 'pos': _pos}]

    def synsets(self, word):
        if word in self._jword2offset:
            results = [ ]
            for offset in (self._jword2offset[word]):
                results.append(WordNetCorpusReader._synset_from_pos_and_offset(
                self, offset['pos'], offset['offset']
                ))
            return results
        else:
            return None

    def calcSimilarity(self, word1, word2, calcType="max"):
        synsets1 = self.synsets(word1)
        synsets2 = self.synsets(word2)
        if synsets1 is None or synsets2 is None:
            return (0, None, None)
        maxSynset1 = None
        madSynset2 = None
        maxSim = 0
        for syn1 in synsets1:
            for syn2 in synsets2:
                s = syn1.path_similarity(syn2)
                if s is not None:
                    if s > maxSim:
                        maxSynset1 = syn1
                        maxSynset2 = syn2
                        maxSim = s
        try:
            return (maxSim, maxSynset1, maxSynset2)
        except UnboundLocalError:
            return (0, None, None)
