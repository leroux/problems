class Solution:

    def encode(self, strs: List[str]) -> str:
        # length-prefix each str
        # e.g. ["foo", "bazbar"] -> "3:foo6:bazbar"
        s = ''
        for st in strs:
            s += str(len(st))
            s += ':'
            s += st
        return s

    def decode(self, s: str) -> List[str]:
        strs = []
        i = 0
        j = 0
        while i < len(s):
            '''
            3:foo6:bazbar
            ^^   ^ 
            ||   |
            ij   j+l+1
            '''
            if s[j] == ':':
                l = int(s[i:j])
                strs.append(s[j+1:j+1+l])
                i = j+1+l
                j = i
            j += 1
        return strs
        

