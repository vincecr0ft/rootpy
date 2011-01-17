import os
import re
import ROOT

class Cut(ROOT.TCut):
    """
    A wrapper class around ROOT.TCut which implements logical operators
    """  
    def __init__(self, cut = ""):
        
        if type(cut) is file:
            cut = "".join(line.strip() for line in cut.readlines())
        elif isinstance(cut, Cut):
            cut = cut.GetTitle()
        ROOT.TCut.__init__(self, cut)
    
    def __and__(self, other):
        """
        Return a new cut which is the logical AND of this cut and another
        """
        if not self:
            return other
        if not other:
            return self
        return Cut("(%s)&&(%s)"% (self, other))

    def __mul__(self, other):

        return self.__and__(other)
    
    def __or__(self, other):
        """
        Return a new cut which is the logical OR of this cut and another
        """
        if not self:
            return other
        if not other:
            return self
        return Cut("(%s)||(%s)"% (self, other))
    
    def __add__(self, other):
        
        return self.__or__(other)

    def __neg__(self):
        """
        Return a new cut which is the negation of this cut
        """
        if not self:
            return Cut()
        return Cut("!(%s)"% self)

    def __pos__(self):
        
        return Cut(self)
    
    def __str__(self):
        
        return self.__repr__()
    
    def __repr__(self):
        
        return self.GetTitle()
         
    def __nonzero__(self):
        """
        A cut evaluates to False if it is empty (null cut).
        This has no affect on its actual boolean value within the context of
        a ROOT.TTree selection.
        """
        return str(self) != ''
    
    def safe(self):
        """
        Returns a string representation with special characters
        replaced by safer characters for use in filenames for example.
        """
        if not self:
            return ""
        string = str(self)
        string = string.replace("==", "-eq-")
        string = string.replace("<=", "-leq-")
        string = string.replace(">=", "-geq-")
        string = string.replace("<", "-lt-")
        string = string.replace(">", "-gt-")
        string = string.replace("&&", "-and-")
        string = string.replace("||", "-or-")
        string = string.replace("(", "L")
        string = string.replace(")", "R")
        return string

    def latex(self):
        """
        Returns a string representation for use in LaTeX
        """ 
        if not self:
            return ""
        string = str(self)
        string = string.replace("==", "=")
        string = string.replace("<=", "\leq")
        string = string.replace(">=", "\geq")
        string = string.replace("&&", " and ")
        string = string.replace("||", " or ")
        return string