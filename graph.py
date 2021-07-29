from seaborn import distplot, boxplot
import matplotlib.pyplot as plt
from pandas import concat as pdconcat, DataFrame as pdDataFrame
from numpy import log10 as np_log10
from io import BytesIO

from side_functions import get_meaning_count, custom_round

def StatAnalysis_2_arr_make_boxplot(arr1, arr2, 
    color='#92cb9e', sizes=(9, 5), dpi=100, labels=('X1', 'X2'), percentage = 0.1):
    fig, ax = plt.subplots(figsize=sizes)
    
    ax = boxplot(
        x='label', 
        y='arr', 
        linewidth=2,
        color=color,
        zorder=5,
        data=pdconcat(
            [
                pdDataFrame(
                    data={'arr' : arr1, 'label': [labels[0]] * len(arr1)}
                ),
                pdDataFrame(
                    data={'arr' : arr2, 'label': [labels[1]] * len(arr2)}
                ),
            ]
        )
    )

    ax.xaxis.grid('Vertical', zorder=0)
    ax.set_title('Диаграмма размаха выборок', fontsize='xx-large')        
    ax.set_xlabel('Выборки', fontsize='xx-large')
    ax.set_ylabel('Значения', fontsize='xx-large')
    
    gmin = min(arr1[0], arr2[0])
    gmax = max(arr1[-1], arr2[-1])
    
    ax.axis(
            ymin=gmin - (gmax-gmin) * percentage,
            ymax=gmax + (gmax-gmin) * percentage,
    )


    plt.tight_layout()
    
    
    buf = BytesIO()
    plt.savefig(buf, dpi=dpi)
    plt.close('all')
    
    return buf

def StatAnalysis_1_arr_make_hist(arr, color='#92cb9e', sizes=(9, 5), dpi=100, percentage=0.01):
    meaning_count_of_array = max([get_meaning_count(el) for el in arr])
    

    delta = max(arr) - min(arr)

    bins_count = delta / (1 + 3.3 * np_log10(len(arr)))
    if bins_count < 5:
        bins_count = 5

    fig, ax = plt.subplots(figsize=sizes)

    ax = distplot(arr,
                  bins=int(round(bins_count, 0)),
                  ax=ax,
                  rug=True,
                  hist_kws={'linewidth': 2,                        
                            'color': color,
                            'zorder': 10,
                            'alpha': 1,
                            'edgecolor': 'grey'  # "k"#
                            },
                  kde_kws={
                      'linewidth': 3,
                      'alpha': 1,
                      "color": '#114b5f',
                      'zorder': 15
                  },
    )


    ax.set_xticks(arr, )    
    arr_meaning = [custom_round(el, meaning_count_of_array) for el in arr]
    ax.set_xticklabels(arr, rotation=90, fontsize='medium')


    ax.yaxis.grid('Vertical', zorder=0)
    ax.set_ylabel('Частота значений (%)', fontsize='xx-large')
    ax.set_xlabel('Значения', fontsize='xx-large')
    ax.set_title('Комбинированный график гистограммы \nи кривой распределения заначений', fontsize='xx-large')

    ax.axis(
        xmin=min(arr) - delta * percentage,
        xmax=max(arr) + delta * percentage)
    #         _ = ax.set_ylabel('')
    plt.tight_layout()

    buf = BytesIO()

    plt.tight_layout()
    plt.savefig(buf, dpi=dpi)
    plt.close('all')

    return buf

    histplot


def StatAnalysis_1_arr_make_boxplot(arr, color='#88d498', sizes=(9, 5), dpi=100, percentage=0.01):
    fig, ax = plt.subplots(figsize=sizes)

    delta = max(arr) - min(arr)
    ax = boxplot(
        x=arr,
        orient='h',
        linewidth=2,
        color=color,
    )

    ax.xaxis.grid('Vertical', zorder=0)
    ax.set_title('Диаграмма размаха выборки', fontsize='xx-large')        
    ax.set_xlabel('Значения', fontsize='xx-large')
    ax.axis(
            xmin=min(arr) - delta * percentage,
            xmax=max(arr) + delta * percentage)


    plt.tight_layout()
    
    
    buf = BytesIO()
    plt.savefig(buf, dpi=dpi)
    plt.close('all')

    return buf

def StatAnalysis_1_true_plot(arr, true_value, color='#88d498', sizes=(9, 5), dpi=100):
    fig, ax = plt.subplots(figsize=sizes)
    
    # plt.ylim(max(max(arr), true_value)+0.03)

    plt.scatter(
        range(1, len(arr)+1),
        arr,
        linewidth=8,
        alpha=0.9,
        color=color,
        zorder=6,
        label='X эксп'
    )

    ax.xaxis.grid('Vertical', zorder=0)
    ax.set_title('Точечная диаграмма', fontsize='xx-large')        
    ax.set_xlabel('Значения', fontsize='xx-large')
    
    # ots = 0.05
    
    ax.axhline(
        xmin=0, 
        xmax=5 ,
        y=true_value, 
        color='#114b5f',
        linewidth=2,
        linestyle='--',
        zorder=1, 
        label='X действ')


    plt.legend()
    plt.tight_layout()
    
    
    buf = BytesIO()
    plt.savefig(buf, dpi=dpi)
    plt.close('all')

    return buf