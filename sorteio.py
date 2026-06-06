import pandas as pd

arquivo = "vagas.xlsx"

df = pd.read_excel(arquivo, sheet_name="Links")

amostra = df.sample(n=33)

with pd.ExcelWriter(
    arquivo,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:
    amostra.to_excel(
        writer,
        sheet_name="Sorteadas",
        index=False
    )