import pandas as pd
import re

df = pd.read_csv(r"c:\Users\kaper\Desktop\35-Картриджи-Sharp-2024-06-30.csv")

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

def replace_color(value):
    replacements = {
        '<span style="background: black"> </span>': '<span class="rini_color-square-black"></span>',
        '<span style="background: #FFD700"> </span>': '<span class="rini_color-square-yellow"></span>',
        '<span style="background: #00BFFF"> </span>': '<span class="rini_color-square-cyan"></span>',
        '<span style="background: darkmagenta"> </span>': '<span class="rini_color-square-magenta"></span>',
        '<em style="background: blue"> </em><em style="background: red"> </em><em style="background: yellow"> </em>': '<span class="rini_color-square"></span>'
    }
    return replacements.get(value, value)

df['Cовместимый'] = df['Cовместимый'].apply(remove_compatible)
df['Cовместимый 10 шт.'] = df['Cовместимый 10 шт.'].apply(remove_unnamed_2)
df['Ориг.'] = df['Ориг.'].apply(remove_orig)
df['Цвет'] = df['Цвет'].apply(replace_color)

df.to_csv(r'./sharp-cartridges_cleaned_full.csv', index=False)

print(df.columns)
