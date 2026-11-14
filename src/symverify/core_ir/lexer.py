from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum): # restricted types so no random stuff can be typed 
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    NUM = auto()
    EXP = auto()
    IDENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

@dataclass # defines valid contents for a Token class
class Token:
    kind: TokenType
    content: int | float | str | None = None

OPERATIONS = {"+": TokenType.ADD, 
              "-": TokenType.SUB, 
              "*": TokenType.MUL, 
              "/": TokenType.DIV, 
              "(": TokenType.LPAREN, 
              ")": TokenType.RPAREN, 
              "^": TokenType.EXP} # valid options for special characters 

def tokenize(text: str) -> list[Token]:
    i = 0
    results: list[Token] = []
    
    while(i < len(text)):
        if text[i].isspace():
            i += 1
        elif text[i].isdigit():
            foundDecimal = False
            temp = i
            while temp < len(text) and (text[temp].isdigit() or text[temp] == '.'):
                if text[temp] == '.':
                    if foundDecimal: 
                        raise SyntaxError(f"Double decimal found inside of digit at {temp}")
                    else: 
                        foundDecimal = True
                temp += 1
            if foundDecimal:
                results.append(Token(TokenType.NUM, float(text[i:temp])))
            else:
                results.append(Token(TokenType.NUM, int(text[i:temp])))
            i = temp
        elif text[i].isalpha():
            temp = i
            while temp < len(text) and text[temp].isalpha():
                temp += 1
            results.append(Token(TokenType.IDENT, text[i:temp]))
            i = temp
        elif text[i] in OPERATIONS:
            results.append(Token(OPERATIONS[text[i]]))
            i += 1
        else:
            raise SyntaxError(f"Unknown Character at {i}")
        
    results.append(Token(TokenType.EOF))
    return results


                
        
             

