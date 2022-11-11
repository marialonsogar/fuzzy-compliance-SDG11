import zadeh
import functools
import itertools
import numpy as np

COMPLIANCE_DEGREE = zadeh.FuzzyVariable(
    zadeh.FloatDomain("compliance_degree", 0, 100, 1000),
    {
        'SDG achieved': zadeh.SFuzzySet(75, 85),
        'Challenges remain': zadeh.BellFuzzySet(15, 15, 65),
        'Significant challenges remain': zadeh.BellFuzzySet(15, 15, 35),
        'Major challenges remain': zadeh.ZFuzzySet(15, 25),

    },
)

class VariableFIS:
    """
    Fuzzy Inference System definition allowing for non fixed set
    of input variables. Receives a dictionary of crisp input 
    values and build a FIS using the variables passed. 
    Returns a crisp output prediction. 

    Attributes:
        crisp_input: dictionary of crisp input values
    """

    def __init__(self, fuzzy_variables):
        self.fuzzy_variables = fuzzy_variables
        self.input_variables = {k: v for k, v in fuzzy_variables.items() if v['type'] == 'input'}
        self.output_variable = self.get_output_variable()
        self.rule_set = self.generate_rules()
        self.fis = zadeh.FIS(self.input_variables, self.rule_set, self.output_variable, defuzzification='centroid')
    
    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

    def get_output_variable(self):
        """
        Extract only the fuzzy variable from the output variable
        """
        output_variable = {k: v for k, v in self.fuzzy_variables.items() if v['type'] == 'output'}
        return list(output_variable.values())[0]['fuzzy_variable']

    def add_green_rule(self, weight=1):
        """
        Define the green rule as stated in the SDG report 2022 
        to avoid the 
        """
        # take input fuzzy variables in a list
        input_variables = [v['fuzzy_variable'] for v in self.input_variables.values()]       
        # define each individual antecedent for SDG achieved (green)
        antecedents = [(variable == "SDG achieved") for variable in input_variables]
        # combine fuzzy propositions in antecedents with AND operation
        antecedents = functools.reduce(lambda x, y: x & y, antecedents)
        # make fuzzy implication from antecedents
        green_rule = zadeh.FuzzyRule(antecedents, COMPLIANCE_DEGREE == "SDG achieved", weight=weight)
        return green_rule

    def add_red_rule(self, weight=1):
        """
        Define the red rule as stated in the SDG report 2022 
        to avoid the 
        """
        # take input fuzzy variables in a list
        input_variables = [v['fuzzy_variable'] for v in self.input_variables.values()]       
        # define each individual antecedent for SDG achieved (green)
        antecedents = [(variable == "Major challenges remain") for variable in input_variables]
        # make combinations with AND for every two possible combination of variables in input_variables
        antecedents = [functools.reduce(lambda x, y: x & y, combination) for combination in itertools.combinations(antecedents, 2)]
        # combine each two antecedents above with OR operation
        antecedents = functools.reduce(lambda x, y: x | y, antecedents)
        # make fuzzy implication from antecedents
        red_rule = zadeh.FuzzyRule(antecedents, COMPLIANCE_DEGREE == "Major challenges remain", weight=weight)
        return red_rule

    def generate_rules(self):
        """
        Generate rules for the FIS

        Returns:
            FuzzyRuleSet: list of rules
        """

        reversed = [zadeh.FuzzyRuleSet.automatic(
            input_var['fuzzy_variable'], self.output_variable, reverse=True, weight=input_var['weight'],
        ) for input_var in self.input_variables.values() if input_var['reverse']]        

        not_reversed = [zadeh.FuzzyRuleSet.automatic(
            input_var['fuzzy_variable'], self.output_variable, reverse=False, weight=input_var['weight'],
        ) for input_var in self.input_variables.values() if not input_var['reverse']]

        # added rules: if all input variables are 'SDG achieved' then, 'SDG achieved'
        try:   
            green_rule = self.add_green_rule(weight=1)
            red_rule = self.add_red_rule(weight=1)
        except Exception as e:
            print(e)
            green_rule = None
            red_rule = None


        if ((green_rule is not None) and (red_rule is not None)):
            rule_set = zadeh.FuzzyRuleSet(reversed + not_reversed + [green_rule] + [red_rule])
        else:
            rule_set = zadeh.FuzzyRuleSet(reversed + not_reversed)

        # for rule in rule_set:
        #     print(rule)
        return rule_set
    
    def _infer_input_variables_from_input(self, input):
        """
        Select input variables to match the ones of the input 

        Args:
            input (dict): input dictionary with the crisp inputs

        Returns:
            dict: dictionary with input variables
        """

        # if a key on input variables is not in the input, pop it 
        for key in list(self.input_variables.keys()):
            if key not in input:
                self.input_variables.pop(key)
    
    def predict(self, input):
        # if a value is nan or None, drop the item
        input = {k: v for k, v in input.items() if ((v is not None) and (not np.isnan(v)))} 
        # input = {k: v for k, v in input.items() if not np.isnan(v)}
        # select input variables for the given input
        self._infer_input_variables_from_input(input)
        # update rules
        self.rule_set = self.generate_rules()
        # update fis for this variables
        self.fis = zadeh.FIS(self.input_variables, self.rule_set, self.output_variable, defuzzification='centroid')
        return self.fis.get_crisp_output(input)

    def plot_rules(self, *args, **kwargs):
        return self.fis.plot_rules(*args, **kwargs)