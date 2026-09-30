import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt

from enum import Enum, auto
import numpy as np

class BaseType(Enum):
    GENERAL = auto()
    SPECIFIC = auto()

    def __str__(self):
        return self.name

conn = psycopg2.connect("dbname=corn_party user=postgres password=password host=localhost")
cur = conn.cursor()

def _generic_query(metric:str,model_name: str, baseType: BaseType):
    query = sql.SQL("""
        SELECT {metric}
        FROM (
            SELECT * FROM translation_mdn WHERE model_name = %s
            UNION ALL
            SELECT * FROM translation_php WHERE model_name = %s
        ) AS resultado;
    """).format(metric=sql.Identifier(metric))
    
    if str(baseType) == str(BaseType.SPECIFIC):
        
        query = sql.SQL("""
            SELECT {metric} FROM translation_open_subtitles WHERE model_name = %s
        """).format(metric=sql.Identifier(metric))
        
        with conn.cursor() as cur:
            cur.execute(query, (model_name,))
            return cur.fetchall()
    else:
        with conn.cursor() as cur:
            cur.execute(query, (model_name, model_name,))
            return cur.fetchall()


def get_bleu_score(model_name: str, baseType: BaseType):
    result = _generic_query("bleu",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

def get_bert_score_score(model_name: str, baseType: BaseType):
    result = _generic_query("bertscore",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

def get_chrf_score_score(model_name: str, baseType: BaseType):
    result = _generic_query("chrf",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

#cur.execute("SELECT * FROM translation_mdn WHERE id = %s", (1,))
#print(cur.fetchall())

models = ['Helsinki-NLP/opus-mt-tc-big-en-pt','facebook/nllb-200-distilled-600M','facebook/m2m100_418M']

def build_bleu_chart_for_general_base():
    x_axis = []
    for model in models:
        x_axis.append(get_bleu_score(model,BaseType.GENERAL))
    
    plt.boxplot(
        x_axis,
        labels=['MarianMT','NLLB','M2M'],
        boxprops=dict(color='blue'),
        whiskerprops=dict(color='red'),
        capprops=dict(color='green'),
        medianprops=dict(color='orange'),
        flierprops=dict(markerfacecolor='red', marker='o')
    )
    
    plt.title('Pontuação BLEU Textos Gerais')
    plt.xlabel('Modelo')
    plt.ylabel('BLEU')
    plt.show()

def build_bleu_chart_for_specific_base():
    x_axis = []
    for model in models:
        x_axis.append(get_bleu_score(model,BaseType.SPECIFIC))
    
    plt.boxplot(
        x_axis,
        labels=['MarianMT','NLLB','M2M'],
        boxprops=dict(color='blue'),
        whiskerprops=dict(color='red'),
        capprops=dict(color='green'),
        medianprops=dict(color='orange'),
        flierprops=dict(markerfacecolor='red', marker='o')
    )
    
    plt.title('Pontuação BLEU Textos Específicos')
    plt.xlabel('Modelo')
    plt.ylabel('BLEU')
    plt.show()

def build_bertscore_chart_for_general_base():
    x_axis = []
    for model in models:
        x_axis.append(get_bert_score_score(model,BaseType.GENERAL))
    
    plt.boxplot(
        x_axis,
        labels=['MarianMT','NLLB','M2M'],
        boxprops=dict(color='blue'),
        whiskerprops=dict(color='red'),
        capprops=dict(color='green'),
        medianprops=dict(color='orange'),
        flierprops=dict(markerfacecolor='red', marker='o')
    )
    
    plt.title('Pontuação BERTscore Textos Gerais')
    plt.xlabel('Modelo')
    plt.ylabel('BERTscore')
    plt.show()

def build_bertscore_chart_for_specific_base():
    x_axis = []
    for model in models:
        x_axis.append(get_bert_score_score(model,BaseType.SPECIFIC))
    
    plt.boxplot(
        x_axis,
        labels=['MarianMT','NLLB','M2M'],
        boxprops=dict(color='blue'),
        whiskerprops=dict(color='red'),
        capprops=dict(color='green'),
        medianprops=dict(color='orange'),
        flierprops=dict(markerfacecolor='red', marker='o')
    )
    
    plt.title('Pontuação BERTscore Textos Específicos')
    plt.xlabel('Modelo')
    plt.ylabel('BERTscore')
    plt.show()

def build_chrf_chart_for_general_base():
    x_axis = []
    for model in models:
        x_axis.append(get_chrf_score_score(model,BaseType.GENERAL))
    
    plt.boxplot(
        x_axis,
        labels=['MarianMT','NLLB','M2M'],
        boxprops=dict(color='blue'),
        whiskerprops=dict(color='red'),
        capprops=dict(color='green'),
        medianprops=dict(color='orange'),
        flierprops=dict(markerfacecolor='red', marker='o')
    )
    
    plt.title('Pontuação chrf Textos Gerais')
    plt.xlabel('Modelo')
    plt.ylabel('chrf')
    plt.show()

def build_chrf_chart_for_specific_base():
    x_axis = []
    for model in models:
        x_axis.append(get_bert_score_score(model,BaseType.SPECIFIC))
    
    plt.boxplot(
        x_axis,
        labels=['MarianMT','NLLB','M2M'],
        boxprops=dict(color='blue'),
        whiskerprops=dict(color='red'),
        capprops=dict(color='green'),
        medianprops=dict(color='orange'),
        flierprops=dict(markerfacecolor='red', marker='o')
    )
    
    plt.title('Pontuação chrf Textos Específicos')
    plt.xlabel('Modelo')
    plt.ylabel('chrf')
    plt.show()

build_chrf_chart_for_specific_base()
cur.close()
conn.close()