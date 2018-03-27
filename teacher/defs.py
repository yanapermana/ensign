import bbcodepy

class YoutubeTag(bbcodepy.Tag):
	def to_html(self):
		attributes = {
		'src': 'https://www.youtube.com/embed/' + self.get_content(True).strip(),
		'width': self.params.get('width', 427),
		'height': self.params.get('height', 240)
		}
		return '<iframe %s frameborder="0" allowfullscreen></iframe>' % self.renderer.html_attributes(attributes)

class UlTag(bbcodepy.Tag):
	def to_html(self):
		new = bbcodetohtml(self.get_content(True).strip())
		new = new.replace('</li><br />','</li>')
		return '<ul>%s</ul>' % new

class OlTag(bbcodepy.Tag):
	def to_html(self):
		new = bbcodetohtml(self.get_content(True).strip())
		new = new.replace('</li><br />','</li>')
		return '<ol>%s</ol>' % new

class LiTag(bbcodepy.Tag):
	def to_html(self):
		return '<li>%s</li>' % self.get_content(True).strip()

class LeftTag(bbcodepy.Tag):
	def to_html(self):
		new = bbcodetohtml(self.get_content(True).strip())
		new = new.replace('</p><br />','</p>'); print new
		return '<p style="display:inline;" align="left">%s</p>' % new

class RightTag(bbcodepy.Tag):
	def to_html(self):
		new = bbcodetohtml(self.get_content(True).strip())
		new = new.replace('</p><br />','</p>'); print new
		return '<p style="display:inline;" align="right">%s</p>' % new

class CenterTag(bbcodepy.Tag):
	def to_html(self):
		new = bbcodetohtml(self.get_content(True).strip())
		new = new.replace('</p><br />','</p>'); print new
		return '<p style="display:inline;" align="center">%s</p>' % new

class JustifyTag(bbcodepy.Tag):
	def to_html(self):
		new = bbcodetohtml(self.get_content(True).strip())
		new = new.replace('</p><br />','</p>'); print new
		return '<p style="display:inline;" align="justify">%s</p>' % new

def bbcodetohtml(bbcode):
	parser = bbcodepy.Parser()
	parser.register_tag('youtube', YoutubeTag)
	parser.register_tag('ul', UlTag)
	parser.register_tag('ol', OlTag)
	parser.register_tag('li', LiTag)
	parser.register_tag('left', LeftTag)
	parser.register_tag('right', RightTag)
	parser.register_tag('center', CenterTag)
	parser.register_tag('justify', JustifyTag)
	return parser.to_html(bbcode)

# print bbcodetohtml('[youtube]http://www.youtube.com/v/XGSy3_Czz8k[/youtube]')
# text = '[ol][li]x[/li][li]y[/li][li]z[/li][/ol]'
# print bbcodetohtml(text)
# END FUNCTION

# <=================================== BOYER-MOORE ===================================> #
# Boyer Moore String Search implementation in Python
# Ameer Ayoub <ameer.ayoub@gmail.com>

# Generate the Bad Character Skip List
def generateBadCharShift(term):
    skipList = {}
    for i in range(0, len(term)-1):
        skipList[term[i]] = len(term)-i-1
    return skipList

# Generate the Good Suffix Skip List
def findSuffixPosition(badchar, suffix, full_term):
    for offset in range(1, len(full_term)+1)[::-1]:
        flag = True
        for suffix_index in range(0, len(suffix)):
            term_index = offset-len(suffix)-1+suffix_index
            if term_index < 0 or suffix[suffix_index] == full_term[term_index]:
                pass
            else:
                flag = False
        term_index = offset-len(suffix)-1
        if flag and (term_index <= 0 or full_term[term_index-1] != badchar):
            return len(full_term)-offset+1

def generateSuffixShift(key):
    skipList = {}
    buffer = ""
    for i in range(0, len(key)):
        skipList[len(buffer)] = findSuffixPosition(key[len(key)-1-i], buffer, key)
        buffer = key[len(key)-1-i] + buffer
    return skipList
    
# Actual Search Algorithm
def BMSearch(haystack, needle):
    goodSuffix = generateSuffixShift(needle)
    badChar = generateBadCharShift(needle)
    i = 0
    while i < len(haystack)-len(needle)+1:
        j = len(needle)
        while j > 0 and needle[j-1] == haystack[i+j-1]:
            j -= 1
        if j > 0:
            badCharShift = badChar.get(haystack[i+j-1], len(needle))
            goodSuffixShift = goodSuffix[len(needle)-j]
            if badCharShift > goodSuffixShift:
                i += badCharShift
            else:
                i += goodSuffixShift
        else:
            return i
    return -1

def unitestcase():
    block = "This is a simple example"
    print "This is an example search on the string \"", block, "\"."
    print "ple  :", BMSearch(block, "ple ")
    print "example :", BMSearch(block, "example")
    print "simple :", BMSearch(block, "simple")
    print " imple :", BMSearch(block, " imple")

# <=================================== BOYER-MOORE ===================================> #