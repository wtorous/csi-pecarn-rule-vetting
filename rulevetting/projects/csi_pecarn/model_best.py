import numpy as np
import pandas as pd


class SpecialTree:
    def __init__(self):

        self.v_lists = [

        # >12
        ['FocalNeuroFindings', 'HighriskDiving', 'GCSbelowThreshold','PainNeck',
        'SubInj_Head', 'axialloadtop', 'TenderNeck', #'HEENT'
        'HighriskMVC'], 

        # 5-12
        ['FocalNeuroFindings', 'GCSbelowThreshold', 'Torticollis', #'HighriskDiving','HighriskHitByCar'
        'PainNeck', 'Predisposed', 'Clotheslining', 'SubInj_TorsoTrunk', 
        'AxialLoadAnyDoc','HighriskFall','HEENT'], 

        # 2-5
        ['AlteredMentalStatus', 'FocalNeuroFindings', 'Torticollis', 'Predisposed',
        'HighriskMVC', 'PosMidNeckTenderness'],

        # <2
        ['AlteredMentalStatus', 'PosMidNeckTenderness', 'Predisposed', 'AxialLoadAnyDoc',
        'EMSArrival']
        ]

    def predict(self, data):

        for one_list in self.v_lists:
            for v in one_list:
                if v not in data.columns:
                    print('cannot find ' + v)
                    return

        pred = []
        n = data.shape[0]

        for i in range(n):
            df = data.iloc[i]

            if df['VeryYoung'] == 1:
                v_list = self.v_lists[3]
            elif (df['NonVerbal'] == 1) & (df['VeryYoung'] == 0):
                v_list = self.v_lists[2]
            elif (df['YoungAdult'] == 0) & (df['NonVerbal'] == 0):
                v_list = self.v_lists[1]
            else:
                v_list = self.v_lists[0]

            indicator = df[v_list].sum().astype('int')

            if indicator > 0:
                pred.append(1)
            else:
                pred.append(0)

        return pred
    
    def predict_proba(self, data):

        pred_binary = self.predict(data)
        
        # refactored from
        # https://stackoverflow.com/questions/29831489/convert-array-of-indices-to-1-hot-encoded-numpy-array
        prob_result = np.zeros((pred_binary.size, 2))
        prob_result[np.arange(pred_binary.size),pred_binary] = 1
        
        return prob_result

    def print_model(self, data):

        pred = self.predict(data)

        n1 = sum(pred)
        n0 = len(pred) - n1

        s = 'Classification summary: '+str(n1) +' patients labeled 1 and ' +str(n0) + ' patients labeled 0.'

        return s
 

