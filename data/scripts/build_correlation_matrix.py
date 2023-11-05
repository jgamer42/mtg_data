import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Supongamos que tienes un DataFrame llamado 'df' con tus datos
# Si tienes un archivo CSV o Excel, puedes leerlo así:
# df = pd.read_csv('ruta_del_archivo.csv')
# df = pd.read_excel('ruta_del_archivo.xlsx')

# Calcular la matriz de correlación

df = pd.read_csv(f"/home/jaime/mtg_minner/data/clean/Unlimited_Edition.csv")
df = df[['cmc', 'reprint','edhrec_rank', 'penny_rank', "usd","rarity","reserved"]]
df["usd"] = df["usd"].str.replace(",",".")
df["rarity"] = df["rarity"].str.replace("uncommon","2")
df["rarity"] = df["rarity"].str.replace("common","1")
df["rarity"] = df["rarity"].str.replace("rare","3")
df["rarity"] = df["rarity"].str.replace("mythic","4")

matriz_correlacion = df.corr()

# Crear un mapa de calor (heatmap)
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriz de Correlación')
plt.show()