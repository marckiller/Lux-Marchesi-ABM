import math
import numpy as np


class Functions:
    """Package for functions and mathematical expresions that are used in simulation. Natation as in Lux-Marchesi paper. 
    All mtehods are operating based on parameters dictionary"""

    @staticmethod
    def U_1(pms):
        dp_dt = pms['dp_dt']
        x = (pms["num_noise_optimist"] - pms["num_noise_pessimist"])/(pms["num_noise_optimist"] + pms["num_noise_pessimist"])
        a = (pms["alpha2"]*dp_dt/(pms["v1"]*pms["market_price"]))
        return pms["alpha1"]*x + a
    
    @staticmethod
    def pi_plus_minus(pms):
        N = pms['N']
        nc = pms["num_noise_optimist"] + pms["num_noise_pessimist"]
        return pms["v1"]*nc*(1/N)*math.exp(Functions.U_1(pms))
    
    @staticmethod
    def pi_minus_plus(pms):
        N = pms['N']
        nc = pms["num_noise_optimist"] + pms["num_noise_pessimist"]
        return pms["v1"]*nc*(1/N)*math.exp((-1)*Functions.U_1(pms))

    @staticmethod
    def pi_plus_f(pms):
        N = pms['N']
        return (pms["v2"]/N)*pms["num_noise_optimist"]*math.exp(Functions.U_21(pms))

    @staticmethod
    def pi_f_plus(pms):
        N = pms['N']
        return (pms["v2"]/N)*pms["num_fundamentalists"]*math.exp((-1)*Functions.U_21(pms))

    @staticmethod
    def pi_minus_f(pms):
        N = pms['N']
        return (pms["v2"]/N)*pms["num_noise_pessimist"]*math.exp(Functions.U_22(pms))
        
    @staticmethod
    def pi_f_minus(pms):
        N = pms['N']
        return (pms["v2"]/N)*pms["num_fundamentalists"]*math.exp((-1)*Functions.U_22(pms))

    @staticmethod
    def U_21(pms):
        dp_dt = pms['dp_dt']
        r = pms["R"]*pms["market_value"]
        denominator = r + dp_dt/(pms["v2"]**2)
        profits = pms["s"]*abs((pms["market_value"]-pms["market_price"])/pms["market_value"])
        return pms["alpha3"]*(((denominator)/pms["market_price"]) -pms["R"] - profits)

    @staticmethod
    def U_22(pms):
        dp_dt = pms['dp_dt']
        r = pms["R"]*pms["market_value"]
        denominator = r + dp_dt/(pms["v2"]**2)
        profits = pms["s"]*abs((pms["market_value"]-pms["market_price"])/pms["market_value"])
        return pms["alpha3"]*(pms["R"] - ((denominator)/pms["market_price"]) - profits)

    @staticmethod
    def ED(pms):
        ED_c = (pms["num_noise_optimist"] + pms["num_noise_pessimist"])*pms["t_c"]
        ED_f = pms["num_fundamentalists"]*pms["gamma"]*(pms["market_value"]-pms["market_price"])/pms["market_price"]
        ED = ED_c + ED_f
        #print(ED)
        return ED
    
    @staticmethod
    def prob_price_increase(pms, mu):
        #Atention! There is parameter mu in paper and not sure what does it mean
        a = pms["beta"]*(Functions.ED(pms) + mu)
        p_price_up = max(0, a)
        return p_price_up

    @staticmethod
    def prob_price_decrease(pms, mu):
        #Atention! There is parameter mu in paper and not sure what does it mean
        a = pms["beta"]*(Functions.ED(pms) + mu)
        p_price_down = (-1)*min(0, a)
        return p_price_down

    @staticmethod
    def probablistic_value_change(pms):
        mu, sigma = pms['value_change_mu'], pms['value_change_sigma'] # mean and standard deviation
        a = np.random.normal(mu, sigma)
        return pms["market_value"]*math.exp(a) #think it's ok. check
    
 #   @staticmethod
 #   def create_dict_of_probabilities(pms, dp_dt):
 #       """Most complex function that uses all other. It creates dictionary of transition probabilities. That dictionary is later passed to Agent object to potentialy change hist strategy"""
 #       dictionary = {'pi_plus_minus': Functions.pi_plus_minus(pms, dp_dt),
 #                     'pi_minus_plus': Functions.pi_minus_plus(pms, dp_dt),
 #                     'pi_plus_f': Functions.pi_plus_f(pms, dp_dt),
 #                     'pi_f_plus': Functions.pi_f_plus(pms, dp_dt),
 #                     'pi_minus_f': Functions.pi_minus_f(pms, dp_dt),
 #                     'pi_f_minus': Functions.pi_f_minus(pms, dp_dt),
 #                     'pi_price_up': Functions.prob_price_increase(pms),
 #                     'pi_pirce_down': Functions.prob_price_decrease(pms)}
 #       return dictionary



    




