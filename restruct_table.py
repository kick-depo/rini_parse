import pandas as pd
import re

df = pd.read_csv(r"Hp_Картриджи_2.csv")

pattern_compatible = r'<br/><a href="#add=\d+" class="buy" rel="nofollow, noindex">Купить</a>'
pattern_unnamed_2 = r'<br/><a href="#add=\d+&qty=\d+" class="buy" rel="nofollow, noindex">Купить</a>'
pattern_orig = r'<br/><a href="#add=-\d+" class="buy" rel="nofollow, noindex">Купить</a>'

def remove_compatible(value):
    if isinstance(value, str):
        return re.sub(pattern_compatible, '', value)
    return value

def remove_unnamed_2(value):
    if isinstance(value, str):
        return re.sub(pattern_unnamed_2, '', value)
    return value

def remove_orig(value):
    if isinstance(value, str):
        return re.sub(pattern_orig, '', value)
    return value

df['Cовместимый'] = df['Cовместимый'].apply(remove_compatible)
df['Unnamed: 2'] = df['Unnamed: 2'].apply(remove_unnamed_2)
df['Ориг.'] = df['Ориг.'].apply(remove_orig)

df.to_csv(r'./Hp-Картриджи_cleaned.csv', index=False)

print(df.columns)
