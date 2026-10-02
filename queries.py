import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt

from enum import Enum, auto
import numpy as np
from tabulate import tabulate

class BaseType(Enum):
    GENERAL = auto()
    SPECIFIC = auto()

    def __str__(self):
        return self.name

class Efficiency:
    model_name: str
    base_type: BaseType
    cpu_average_usage: float
    cpu_max_usage: float
    additional_memory: float
    peak_memory: float
    initial_memory: float
    inference_time: float

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

def get_average_cpu_usage(model_name: str, baseType: BaseType):
    result = _generic_query("cpu_average_usage",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

def get_max_cpu_usage(model_name: str, baseType: BaseType):
    result = _generic_query("cpu_max_usage",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

def get_additional_memory(model_name: str, baseType: BaseType):
    result = _generic_query("additional_memory",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

def get_peak_memory(model_name: str, baseType: BaseType):
    result = _generic_query("peak_memory",model_name,baseType)

    arrayPlot = []

    for line in result:
        arrayPlot.append(float(line[0]))

    return np.array(arrayPlot)

def get_initial_memory(model_name: str, baseType: BaseType):
    result = _generic_query("initial_memory",model_name,baseType)

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

def get_inference_time(model_name: str, baseType: BaseType):
    result = _generic_query("inference_time",model_name,baseType)

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

def get_efficiency_data():
    lines: list[Efficiency] = []
        
    for model in models:
        efficiencyGeneral: Efficiency = Efficiency()
        efficiencyGeneral.model_name = model
        efficiencyGeneral.base_type = BaseType.GENERAL
    
        cpu_usage_general = get_average_cpu_usage(model,BaseType.GENERAL)
        max_cpu_usage_general = get_max_cpu_usage(model,BaseType.GENERAL)
        additional_memory_general = get_additional_memory(model,BaseType.GENERAL)
        peak_memory_general = get_peak_memory(model,BaseType.GENERAL)
        initial_memory_general = get_initial_memory(model,BaseType.GENERAL)
        inference_time_general = get_inference_time(model,BaseType.GENERAL)
    
        efficiencyGeneral.cpu_average_usage = cpu_usage_general.mean()
        efficiencyGeneral.cpu_max_usage = max_cpu_usage_general.mean()
        efficiencyGeneral.additional_memory = additional_memory_general.mean()
        efficiencyGeneral.peak_memory = peak_memory_general.mean()
        efficiencyGeneral.initial_memory = initial_memory_general.mean()
        efficiencyGeneral.inference_time = inference_time_general.mean()
    
    
        efficiencySpecific: Efficiency = Efficiency()
        efficiencySpecific.model_name = model
        efficiencySpecific.base_type = BaseType.SPECIFIC
        
        average_cpu_usage_specific = get_average_cpu_usage(model,BaseType.SPECIFIC)
        max_cpu_usage_specific = get_max_cpu_usage(model,BaseType.SPECIFIC)
        additional_memory_specific = get_additional_memory(model,BaseType.SPECIFIC)
        peak_memory_specific = get_peak_memory(model,BaseType.SPECIFIC)
        initial_memory_specific = get_initial_memory(model,BaseType.SPECIFIC)
        inference_time_specific = get_inference_time(model,BaseType.SPECIFIC)
    
        efficiencySpecific.cpu_average_usage = average_cpu_usage_specific.mean()
        efficiencySpecific.cpu_max_usage =     max_cpu_usage_specific.mean()
        efficiencySpecific.additional_memory = additional_memory_specific.mean()
        efficiencySpecific.peak_memory =       peak_memory_specific.mean()
        efficiencySpecific.initial_memory = initial_memory_specific.mean()
        efficiencySpecific.inference_time = inference_time_specific.mean()
    
        lines.append(efficiencyGeneral)
        lines.append(efficiencySpecific)

    return lines

def build_efficiency_table():
    line = get_efficiency_data()

    headers = [
    "Modelo", "Tipo", "CPU Média", "CPU Máx", 
    "Mem Add", "Mem Pico", "Tempo Inf."
    ]

    table_data = [
    [
        item.model_name,
        str(item.base_type),
        f"{item.cpu_average_usage:.1f}%",
        f"{item.cpu_max_usage:.1f}%",
        f"{item.additional_memory:.2f} MB",
        f"{item.peak_memory:.2f} GB",
        f"{item.inference_time:.3f}s",
    ]
    for item in line
]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def build_cpu_average_usage_chart():
    models = ['Helsinki-NLP/opus-mt-tc-big-en-pt','facebook/nllb-200-distilled-600M','facebook/m2m100_418M']

    specific_base = []
    general_base = []

    for model in models:
        inference_time = get_average_cpu_usage(model,BaseType.SPECIFIC)
        inference_time.mean()
        specific_base.append(inference_time.mean())

        inference_time = get_average_cpu_usage(model,BaseType.GENERAL)
        inference_time.mean()
        general_base.append(inference_time.mean())
        
    models = ['MarianMT','NLLB','M2M']
    

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    

    ax.bar(
        x - width/2,
        specific_base,
        width,
        label='Base específica',
        color='#10b981',
    )
    ax.bar(
        x + width/2,
        general_base,
        width,
        label='Base geral',
        color='#3b9eff',
    )

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    ax.set_ylabel('Uso médio de CPU (%)')
    ax.set_title('Uso médio de CPU por modelo e tipo de texto')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

def build_peak_memory_usage_chart():
    models = ['Helsinki-NLP/opus-mt-tc-big-en-pt','facebook/nllb-200-distilled-600M','facebook/m2m100_418M']

    specific_base = []
    general_base = []

    for model in models:
        inference_time = get_peak_memory(model,BaseType.SPECIFIC)
        inference_time.mean()
        specific_base.append(inference_time.mean())

        inference_time = get_peak_memory(model,BaseType.GENERAL)
        inference_time.mean()
        general_base.append(inference_time.mean())
        
    models = ['MarianMT','NLLB','M2M']
    

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    

    ax.bar(
        x - width/2,
        specific_base,
        width,
        label='Base específica',
        color='#3b9eff',
    )
    ax.bar(
        x + width/2,
        general_base,
        width,
        label='Base geral',
        color='#10b981',
    )

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    ax.set_ylabel('Pico de memória (GB)')
    ax.set_title('Pico de memória por modelo e tipo de texto')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

def build_inference_time_chart():
    specific_base = []
    general_base = []

    models = ['Helsinki-NLP/opus-mt-tc-big-en-pt','facebook/nllb-200-distilled-600M','facebook/m2m100_418M']
    
    for model in models:
        inference_time = get_inference_time(model,BaseType.SPECIFIC)
        inference_time.mean()
        specific_base.append(inference_time.mean())

        inference_time = get_inference_time(model,BaseType.GENERAL)
        inference_time.mean()
        general_base.append(inference_time.mean())
    
    models = ['MarianMT','NLLB','M2M']
    

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    

    ax.bar(
        x - width/2,
        specific_base,
        width,
        label='Base específica',
        color='#3b9eff',
    )
    ax.bar(
        x + width/2,
        general_base,
        width,
        label='Base geral',
        color='#10b981',
    )

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    ax.set_ylabel('Tempo médio (segundos)')
    ax.set_title('Tempo médio de inferência por modelo')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

build_peak_memory_usage_chart()
cur.close()
conn.close()