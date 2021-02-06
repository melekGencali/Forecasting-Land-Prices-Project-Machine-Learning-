
import pandas as pd
df_train = pd.read_csv('scrapyProje/hurriyetVeri.csv')
df_train["Team"] = df_train["Team"].str.upper()


df_train