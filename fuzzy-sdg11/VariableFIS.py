import zadeh 
from typing import Dict, Any, List

class VariableFIS:
    """
    Fuzzy Inference System definition allowing for non fixed set
    of input variables. Receives a dictionary of crisp input 
    values and build a FIS using the variables passed. 
    Returns a crisp output prediction. 

    Attributes:
        crispy_input: dictionary of crisp input values


    """
    def __init__(self, crisp_input: Dict[str, float], fuzzy_variables: Dict[str, Any]):
        self.crisp_input = crisp_input
        self.fuzzy_variables = fuzzy_variables
        self.fis = self.build_fis()

    def build_fis(self, input_variables:Any=None):
        """
        Build a FIS using the variables passed in the crisp input
        dictionary 
        """
        # get the fuzzy variables of the system
        if input_variables is None:
            input_variables = self.fuzzy_variables.values()
        # build the FIS
        fis = zadeh.FIS()
        
        return FIS(input_variables, self.crisp_input)


    def __call__(self, *args, **kwargs):
        return self.fis.get_crisp_output(*args, **kwargs)[self.variable]

    def plot(self, *args, **kwargs):
        return self.fis.plot_rules(*args, **kwargs)

