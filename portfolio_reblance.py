import pandas as pd


class PortfolioRebalancer:
    FILE_PATH = 'portfolioWeights_project.xlsx'

    @classmethod
    def fetch_raw_portfolio(cls):
        df = pd.read_excel(cls.FILE_PATH)
        df = df.rename(columns={'freeFloatMcap': 'mcap'})
        df['weight'] = df['mcap'] / df['mcap'].sum()
        return df
    
    @classmethod
    def apply_10_percent_constraint(cls, df):
        df.loc[df['weight'] > 0.1, 'weight_adj'] = 0.1
        df.loc[df['weight'] <= 0.1, 'weight_adj'] = df['weight']

        extra_weight = df[df['weight'] > 0.1]['weight'].sum() - df[df['weight'] > 0.1]['weight_adj'].sum()
        redistribution_delta = extra_weight / len(df[df['weight'] <= 0.1])
        df['weight_adj'] = df['weight_adj'] + redistribution_delta

        # Names whose weight above 10% after redistribution
        df['']
        
        df = df.drop('weight', axis=1)
        df = df.rename(columns={'weight_adj': 'weight'})
        return df
