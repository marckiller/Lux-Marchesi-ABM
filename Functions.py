import math

class Functions:
    """Package for functions and mathematical expresions that are used in simulation. Natation as in Lux-Marchesi paper. 
    All mtehods are operating based on parameters dictionary"""
    @staticmethod
    def prob_optimist_to_pesimist(alpha, n_plus, n_minus, alpha_2, v_1, price_trend, n_fundamentalist):
        """probability of switching from optimist to pesimist. It uses another function: U_1"""
        return v_1*(n_plus+n_minus)*(1/(n_plus+n_minus+n_fundamentalist))*math.exp(Functions.U_1(alpha, n_plus, n_minus, alpha_2, v_1, price_trend))

    @staticmethod
    def prob_pesimist_to_optimist(alpha, n_plus, n_minus, alpha_2, v_1, price_trend, n_fundamentalist):
        """probability of switching from pesimist to optimist. It uses another function: U_1"""
        return v_1*(n_plus+n_minus)*(1/(n_plus+n_minus+n_fundamentalist))*math.exp((-1)*Functions.U_1(alpha, n_plus, n_minus, alpha_2, v_1, price_trend))

    @staticmethod
    def prob_optimist_to_fundamentalist(alpha_3, v_2, r, R, p, p_f, price_trend, sn ):
        """probability of switching from optimist noise trader to fundamentlalist"""
        pass

    @staticmethod
    def prob_fundamentalist_to_optimist():
        """probability of switching from fundamentlalist to optimist noise trader"""
        pass

    @staticmethod
    def prob_optimist_to_fundamentalist():
        """probability of switching from pessimist noise trader to fundamentlalist"""
        pass

    @staticmethod
    def prob_fundamentalist_to_optimist():
        """probability of switching from fundamentlalist to pessimist noise trader"""
        pass

    @staticmethod
    def U_1(alpha, n_plus, n_minus, alpha_2, v_1, price_trend):
        #price trend is dp/dt * 1/p
        x = (n_plus-n_minus)/(n_plus + n_minus)
        u_1 = aplha_1*x + aplha_2*price_trend/v_1
        return u_1

    @staticmethod
    def U_2_1(alpha_3, v_2, r, R, p, p_f, price_trend, s):
        #price trend is dp/dt * 1/p
        term1 = (r/p) + price_trend/(v_2**2)
        term2 = s*abs((p_f-p)/p)
        return alpha_3*(term1-R-term2)

    @staticmethod
    def U_1_2(alpha_3, v_2, r, R, p, p_f, price_trend, s):
        #price trend is dp/dt * 1/p
        term1 = (r/p) +price_trend/(v_2**2)
        term2 = s*abs((p_f-p)/p)
        return alpha_3*(R - term1 - term2)

    



