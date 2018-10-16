from nltk.tokenize import TweetTokenizer

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        # create an empty dict
        self.dictionary = {}
        
        # open file, add every line not starting with ';' to dict (and strip all white space); give line a value (positive in this case)
        # with: "After the statement is executed, the file is always closed, even if a problem was encountered while processing the lines."
        with open(positives) as file:
            for line in file:
                if line.startswith(';') == False:
                    self.dictionary[line.strip()] = 1

        with open(negatives) as file:
            for line in file:
                if line.startswith(';') == False:
                    self.dictionary[line.strip()] = -1

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # instantiate tokenizer
        tokenizer = TweetTokenizer()
        
        # tokenize text, or, split text into a list of strings
        tokens = tokenizer.tokenize(text)

        sum = 0

        # compare every word in tokens to dictionary; if found, add value of word to sum
        for word in tokens:
            if str.lower(word) in self.dictionary:
                sum += self.dictionary[str.lower(word)]  # {}???
        return sum
