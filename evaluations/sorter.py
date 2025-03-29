import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) 

df = pd.read_csv(base_dir + '/answersCA.csv')

df = df.sort_values(by="Required Database", ascending=True)
df.to_csv(base_dir + "/sortedAnswersCA.csv", index=False)

#df_column = df[['Amount of Tokens']]
#df_column.to_csv(base_dir + '/TokensCA.csv', index=False)