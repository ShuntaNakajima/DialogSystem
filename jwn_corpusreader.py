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

        pos1s = [x.pos for x in synsets1]
        pos2s = [x.pos for x in synsets2]

        #入力に名詞以外が入っている場合
        if 'n' not in pos1s or 'n' not in pos2s:
            alt_word1 = []
            alt_word2 = []
            if 'a' in pos1s or 's' in pos1s:
                alt_word = [word1[:-1] + "さ", word1[:-1] + "み", word1[:-1] + "け", word1[:-1] + "げ"]
            if 'a' in pos2s or 's' in pos1s:
                alt_word = [word2[:-1] + "さ", word2[:-1] + "み", word2[:-1] + "け", word2[:-1] + "げ"]
            maxResult = (0, None, None)
            for a_w1 in alt_word1:
                for a_w2 in alt_word2:
                    r = self.calcSimilarity(a_w1, a_w2)
                    if r[0] > maxResult[0]:
                        maxResult = r
            return maxResult
            
                
        #入力が名詞だけの場合
        else:
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

    def maxSimilaryWord(self, baseWord, compareWords):
        maxWord = None
        maxSim = 0
        for w in compareWords:
            r, _, __ = self.calcSimilarity(baseWord, w)
            if r > maxSim:
                maxWord = w
                maxSim = r
        return (maxWord, maxSim)
