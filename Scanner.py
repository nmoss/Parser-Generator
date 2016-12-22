import Regex

class Token:

    def __init__(self, literal, token_category):
        self.string_literal = literal
        self.token_category = token_category

class Lexeme:

    def __init__(self, lexical_category, regex):
        self.lexical_category = lexical_category
        self.dfa = Regex.get_matcher(regex)

    def match(self, pattern):
        return self.dfa.match_input(pattern)

class Scanner:

    def __init__(self):
        self.lexemes = []
        self.lexemes.append(Lexeme("initlit", "[0-9][0-9]*"))
        self.lexemes.append(Lexeme("floatlit", "[0-9][0-9]*.[0-9]*"))
        keywords = "array|begin|break|do|else|end|enddo|endif|float|for|func|if|in|int|let|of|then|to|type|var|while|,|:|;|\\(|\\)|\\[|\\]|\\{|\\}|\\.|\\+|\\-|\\*|/|=|<>|<|>|<=|>=|&|\\||:="
        self.lexemes.append(Lexeme("keyword", keywords))
        self.lexemes.append(Lexeme("id", "(__*[a-zA-Z0-9][a-zA-Z0-9]*_*)|[a-zA-Z]([a-zA-Z0-9]|_)*"))
        self.stack = []

    def get_lexeme_matches(self, token):
        for lexeme in self.lexemes:
            if(lexeme.match(token)):
                return lexeme
        return Lexeme("ERROR", "$")

    def nextWord(self, current_token, matched_tokens):
        lexical_type = self.get_lexeme_matches(current_token)
        if(lexical_type.lexical_category != "ERROR"):
            self.stack = []
            self.stack.append(lexical_type)
            return current_token
        if(len(self.stack) != 0):
            lexical_type = self.stack.pop()
            valid_token = current_token[0:len(current_token)-1]
            matched_tokens.append(Token(valid_token, lexical_type.lexical_category))
            invalid_token = current_token[len(current_token)-1:len(current_token)]
            if(invalid_token == " " or invalid_token == "\n"):
                return ""
            self.nextWord(invalid_token, matched_tokens)
        return current_token

    def scan(self, filename):
        matched_tokens = []
        tigerfile = open(filename, 'r')
        token = ""
        for line in tigerfile:
            for character in line:
                token = token + character
                token = self.nextWord(token, matched_tokens)
            token = self.nextWord(token, matched_tokens)
        return matched_tokens









