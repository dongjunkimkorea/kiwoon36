import numpy as np
import pandas as pd

data = [[1.4, np.nan],
         [7.1, -4.5],
         [np.nan, np.nan],
         [0.75, -1.3]]

# 컬럼명과 행 인덱스 명 지정
df = pd.DataFrame(data, columns=["one","two"], index=["a", "b", "c", "d"])


print(type(df["one"].sum()))
print(df["one"].sum())