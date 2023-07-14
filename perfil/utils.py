from extrato.models import mValores
from datetime import datetime

def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo)
    return total


def calcula_equilibrio_financerio():
    gastos_enssenciais = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_enssenciais = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_enssenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_enssenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais


    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total
        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    
    except:

        return 0, 0


def saldo_despesas():
    entrada_mes = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='E')
    saida_mes = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='S')


    total_entrada_mes = calcula_total(entrada_mes, 'valor')
    total_saida_mes = calcula_total(saida_mes, 'valor')

    total_livre = total_entrada_mes - total_saida_mes

    return total_entrada_mes, total_saida_mes, total_livre