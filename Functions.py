import math
import numpy as np


class Functions:
    """Package for functions and mathematical expresions that are used in simulation. Natation as in Lux-Marchesi paper. 
    All mtehods are operating based on parameters dictionary"""

    @staticmethod
    def U_1(pms, dp_dt, N):
        x = (pms["num_noise_optimist"] - pms["num_noise_pessimist"])/N
        a = (pms["alpha2"]*dp_dt/(pms["v1"]*pms["market_price"]))
        return pms["alpha1"]*x + a
    
    @staticmethod
    def pi_plus_minus(pms, dp_dt):
        N = pms["num_noise_optimist"] + pms["num_noise_pessimist"] + pms["num_fundamentalists"]
        nc = pms["num_noise_optimist"] + pms["num_noise_pessimist"]
        return pms["v1"]*nc*(1/N)*math.exp(Functions.U_1(pms, dp_dt, N))
    
    @staticmethod
    def pi_minus_plus(pms, dp_dt):
        N = pms["num_noise_optimist"] + pms["num_noise_pessimist"] + pms["num_fundamentalists"]
        nc = pms["num_noise_optimist"] + pms["num_noise_pessimist"]
        return pms["v1"]*nc*(1/N)*math.exp((-1)*Functions.U_1(pms, dp_dt, N))

    @staticmethod
    def pi_plus_f(pms, dp_dt):
        N = pms["num_noise_optimist"] + pms["num_noise_pessimist"] + pms["num_fundamentalists"]
        return (pms["v2"]/N)*pms["num_noise_optimist"]*math.exp(Functions.U_21(pms, dp_dt))

    @staticmethod
    def pi_f_plus(pms, dp_dt):
        N = pms["num_noise_optimist"] + pms["num_noise_pessimist"] + pms["num_fundamentalists"]
        return (pms["v2"]/N)*pms["num_fundamentalists"]*math.exp((-1)*Functions.U_21(pms, dp_dt))

    @staticmethod
    def pi_minus_f(pms, dp_dt):
        N = pms["num_noise_optimist"] + pms["num_noise_pessimist"] + pms["num_fundamentalists"]
        return (pms["v2"]/N)*pms["num_noise_pessimist"]*math.exp(Functions.U_22(pms, dp_dt))
        
    @staticmethod
    def pi_f_minus(pms, dp_dt):
        N = pms["num_noise_optimist"] + pms["num_noise_pessimist"] + pms["num_fundamentalists"]
        return (pms["v2"]/N)*pms["num_fundamentalists"]*math.exp((-1)*Functions.U_22(pms, dp_dt))


    @staticmethod
    def U_21(pms, dp_dt):
        r = pms["R"]*pms["market_price"]
        denominator = r + dp_dt/(pms["v2"])
        profits = pms["s"]*abs((pms["market_value"]-pms["market_price"])/pms["market_value"])
        return pms["alpha3"]*(((denominator)/pms["market_price"]) -pms["R"] - profits)

    @staticmethod
    def U_22(pms, dp_dt):
        r = pms["R"]*pms["market_price"]
        denominator = r + dp_dt/(pms["v2"])
        profits = pms["s"]*abs((pms["market_value"]-pms["market_price"])/pms["market_value"])
        return pms["alpha3"]*(pms["R"] - ((denominator)/pms["market_price"]) - profits)

    @staticmethod
    def ED(pms):
        ED_c = (pms["num_noise_optimist"] + pms["num_noise_pessimist"])*pms["t_c"]
        ED_f = pms["num_fundamentalists"]*pms["gamma"]*(pms["market_value"]-pms["market_price"])/pms["market_value"]
        return ED_c + ED_f
    
    @staticmethod
    def prob_price_increase(pms, m_u):
        #Atention! There is parameter mu in paper and i don't know wjat does it mean
        a = pms["beta"]*(Functions.ED(pms)+ m_u)
        p_price_up = max(0, a)
        return p_price_up

    @staticmethod
    def prob_price_decrease(pms, m_u):
        #Atention! There is parameter mu in paper and i don't know wjat does it mean
        a = pms["beta"]*(Functions.ED(pms)+m_u)
        p_price_down = (-1)*min(0, a)
        return p_price_down

    @staticmethod
    def prob_value_change(pms):
        mu, sigma = 0, 0.005 # mean and standard deviation
        e = np.random.normal(mu, sigma)
        return pms["market_value"]*math.exp(e) #think it's ok. check



    




