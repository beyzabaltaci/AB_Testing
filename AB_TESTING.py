import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df1 = pd.read_excel("HAFTA_4/ODEV_HAFTA4/ABTesti/ab_testing.xlsx", sheet_name="Control Group")
df1.head()

df2 = pd.read_excel("HAFTA_4/ODEV_HAFTA4/ABTesti/ab_testing.xlsx", sheet_name="Test Group")
df2.head()

df1.shape
df2.shape
df1.columns
df2.columns
df1.dtypes
df2.dtypes
df1.describe().T
df2.describe().T
df1.value_counts()
df2.value_counts()

df1["Bidding"] = "max"
df2["Bidding"] = "average"

all_groups = pd.concat([df1, df2], ignore_index=True)
all_groups.head(50)
all_groups.describe().T

#H0: M1 == M1 Anlamlı bir fark yoktur.
#H1: M1 != M2 Anlamlı bir fark vardır.

all_groups.loc[all_groups["Bidding"] == "max", "Purchase"].mean()

all_groups.loc[all_groups["Bidding"] == "average", "Purchase"].mean()

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df.loc[all_groups["Bidding"] == "max", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value > 0.05 olduğu için H0 reddedilemez. Normal dağılım sağlanmaktadır.

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

#Kontrol grubuna göre homojenlik:
test_stat, pvalue = levene(all_groups.loc[all_groups["Bidding"] == "max", "Purchase"],
                           all_groups.loc[all_groups["Bidding"] == "average", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p > 0.05 old. için H0 reddedilemez. Homojendir. Parametrik testler kullanılmalıdır. (ANOVA)
#Normal ve homojen dağılım reddedilemediği için parametrik istatistiksel analiz yöntemlerinden olan T testi kullanılacaktır.

test_stat, pvalue = ttest_ind(all_groups.loc[all_groups["Bidding"] == "max", "Purchase"],
                              all_groups.loc[all_groups["Bidding"] == "average", "Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value > 0.05 old. için H0 reddedilemez.