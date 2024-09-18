import pandas as pd
import matplotlib.pyplot as plt


# Suponiendo que 'df' es tu DataFrame con múltiples columnas
def plot_barras(df, ax):
    df.plot(kind='bar', ax=ax)

def plot_lineas(df, ax):
    df.plot(kind='line', ax=ax)
    ax.set_yscale('log') 

def plot_circular(df, ax):
    df_sum = df.sum(axis=0)  # Sumamos las columnas para hacer un solo gráfico de torta
    df_sum.plot(kind='pie', ax=ax)

def plot_dispersión(df, ax):
    if df.shape[1] > 2:
        for i in range(1, df.shape[1]):
            ax.scatter(df.iloc[:, 0], df.iloc[:, i], label=df.columns[i])
        ax.legend()
    else:
        df.plot(kind='scatter', x=df.columns[0], y=df.columns[1], ax=ax)

def plot_histograma(df, ax):
    df.plot(kind='hist', ax=ax, alpha=0.5)  # Usamos alpha para superponer los histogramas

def plot_area(df, ax):
    df.plot(kind='area', ax=ax)