import numpy as np
import pandas as pd

data = [[1],
         [2],
         [3],
         [4],[5],[6],[7],[8],[9],[10]]

# 컬럼명과 행 인덱스 명 지정
df = pd.DataFrame(data, columns=["one"])


print(df)
print("----------------------------------")
print(df["one"].cumsum(window=2))