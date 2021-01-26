#!/usr/bin/python3
# coding=utf-8
# Created by Everton Correia
""" This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. """

# imports
from numpy import arange
from math import log
import os, sys
import pickle

# local imports
import isa.variables as variables
import matplotlib.pyplot as plt
plt.rcdefaults()

PESOS = variables.PESOS

SIGLAS = variables.SIGLAS

# resultados de araraquara, usado para debug
# result = {'0': [217138, 223900, 0.6346, 225.18, 142.92, 1, 35823.1, 47830, 1.197, 1.25],
# '1': [223521, 100, 18221.95, 18221.95, 19824],
# '2': [217541, 10, 74602.35, 1122437.415],
# '3': [0, 0, 0],
# '4': [0, 10.62, 208.9, 225.18, 142.92],
# '5': [0.0105, 0.0338, 2.64, 0.43, 4.3, 16.2]}


def Processar_indicadores_secundarios(dict_crude: dict):
    # processar indicadores secundarios

    dict = {}
    for i in dict_crude:
        # make new list
        dict_r = {}
        for ind in range(len(dict_crude[i])):
            value = dict_crude[i][ind]
            key = SIGLAS[i][ind]
            dict_r[key] = value
        dict[i] = dict_r

    # subfunctions
    def Interpol(min, max, x):
        if x >= min and x <= max:
            m = 100/(max - min)
            y = m*(x - min)
        elif x < min:
            y = 0
        elif x > max:
            y = 100

        return y

    # variaveis usadas por mais de um indicador de segunda ordem
    Dut = dict['0']['Dut']
    t = dict['0']['t']

    result = {}
    full_result = {}  # {iab:{result:10, ind_terciarios:{ica:10, iqa:20,..}]}
    for i in dict:
        v = dict[i]
        if i == '0':  # Indicador de Abastecimentode Água (Iab)
            # calcular Ica
            Ica = (v['Dua']/Dut)*100

            # calcular Iqa
            if v['K'] <= 1:
                Iqa_calc = (v['K']*(v['NAA']/v['NAR']))*100
            else:
                Iqa_calc = (1*(v['NAA']/v['NAR']))*100

            if Iqa_calc >= 100:
                Iqa = 100
            elif Iqa_calc >= 95 and Iqa_calc < 100:
                Iqa = 80
            elif Iqa_calc >= 85 and Iqa_calc < 95:
                Iqa = 60
            elif Iqa_calc >= 70 and Iqa_calc < 85:
                Iqa = 40
            elif Iqa_calc >= 50 and Iqa_calc < 70:
                Iqa = 20
            elif Iqa_calc < 50:
                Iqa = 0

            # calcular Isa
            n = log(v['CP']/(v['VP']*v['K2/K1']))/log(1+t/100)

            if v['sistema'] == 1:  # sistemas integrados
                Isa = Interpol(0, 5, n)
            elif v['sistema'] == 2:  # sistemas superficiais
                Isa = Interpol(0, 3, n)
            elif v['sistema'] == 3:  # sistemas superficiais
                Isa = Interpol(0, 2, n)

            # calculando Indicador de Abastecimentode Água (Iab)
            Iab = (Ica+Iqa+Isa)/3

            # add to result
            result["Iab"] = Iab

            # add to full_result
            full_result['Iab'] = {'result': Iab, 'ind_terciarios': {
                'Ica': Ica, 'Iqa': Iqa, 'Isa': Isa}}

            # # debug
            # print("\n Ica:",Ica,"\n Iqa:", Iqa, "\n Isa:", Isa)
            # print("Indicador de Abastecimentode Água (Iab):", Iab)

        elif i == '1':  # Indicador de EsgotosSanitário (Ies)
            # calcular Ice
            Ice_calc = (v['Due']/Dut)*100

            if Dut <= 5000:
                Ice = Interpol(50, 85, Ice_calc)
            if Dut > 5000 and Dut <= 20000:
                Ice = Interpol(55, 85, Ice_calc)
            if Dut > 20000 and Dut <= 50000:
                Ice = Interpol(60, 85, Ice_calc)
            if Dut > 50000 and Dut <= 100000:
                Ice = Interpol(65, 85, Ice_calc)
            if Dut > 100000 and Dut <= 500000:
                Ice = Interpol(70, 90, Ice_calc)
            if Dut > 500000:
                Ice = Interpol(75, 95, Ice_calc)

            # calcular Ite
            Ite_calc = (v['Ice']/100)*(v['VT']/v['VC'])*100

            if Dut <= 5000:
                Ite = Interpol(15, 56, Ite_calc)
            if Dut > 5000 and Dut <= 20000:
                Ite = Interpol(16.5, 63.75, Ite_calc)
            if Dut > 20000 and Dut <= 50000:
                Ite = Interpol(18, 68, Ite_calc)
            if Dut > 50000 and Dut <= 100000:
                Ite = Interpol(26, 72.25, Ite_calc)
            if Dut > 100000 and Dut <= 500000:
                Ite = Interpol(35, 81, Ite_calc)
            if Dut > 500000:
                Ite = Interpol(45, 81, Ite_calc)

            # calcular Ise
            n = log(v['CT']/v['VC'])/log(1+t/100)

            if Dut <= 50000:
                Ist = Interpol(0, 2, n)
            elif Dut > 50000 and Dut <= 200000:
                Ist = Interpol(0, 3, n)
            elif Dut > 200000:
                Ist = Interpol(0, 5, n)

            # calculando Indicador de EsgotosSanitário (Ies)
            Ies = (Ice+Ite+Ist)/3

            # add to result
            result["Ies"] = Ies

            # add to full_result
            full_result['Ies'] = {'result': Ies, 'ind_terciarios': {
                'Ice': Ice, 'Ite': Ite, 'Ist': Ist}}

            # # debug
            # print("\n Ice:",Ice,"\n Ite:", Ite, "\n Ist:", Ist)
            # print("Indicador de EsgotosSanitário (Ies):", Ies)

        elif i == '2':  # Indicador de Resíduos Sólidos (Irs)
            # calculando Icr
            Icr_calc = (v['Duc']/Dut)*100

            if Dut <= 20000:
                Icr = Interpol(80, 90, Icr_calc)
            elif Dut > 20000 and Dut <= 100000:
                Icr = Interpol(90, 95, Icr_calc)
            elif Dut > 100000:
                Icr = Interpol(95, 99, Icr_calc)

            # calcular Iqr
            if v['Iqr'] >= 0 and v['Iqr'] <= 6:
                # condições inadequadas
                Iqr = 0
            elif v['Iqr'] > 6 and v['Iqr'] <= 8:
                # condições controladas
                Iqr = Interpol(6, 8, v['Iqr'])
            elif v['Iqr'] > 8 and v['Iqr'] <= 10:
                # cond. adequadas
                Iqr = 100

            # calculando Isr
            n = log(v['CA']*(t)/v['VL'] + 1)/log(1+t)

            if Dut <= 50000:
                Isr = Interpol(0, 2, n)
            elif Dut > 50000 and Dut <= 200000:
                Isr = Interpol(0, 3, n)
            elif Dut > 200000:
                Isr = Interpol(0, 5, n)

            # calculando Indicador de Resíduos Sólidos (Irs)
            Irs = (Icr+Iqr+Isr)/3

            # add to result
            result["Irs"] = Irs

            # add to full_result
            full_result['Irs'] = {'result': Irs, 'ind_terciarios': {
                'Icr': Icr, 'Iqr': Iqr, 'Isr': Isr}}

            # # debug
            # print("\n Icr:",Icr,"\n Iqr:", Iqr, "\n Isr:", Isr)
            # print("Indicador de Resíduos Sólidos (Irs):", Irs)

        elif i == '3':  # Indicador de Controle de Vetores  (Icv)
            # calcular Ivd
            Ivd = v['Ivd']

            # calcular Ive
            Ive = v['Ive']

            # calcular Ivl
            Ivl = v['Ivl']

            # calculando Indicador de Controle de Vetores  (Icv)
            Icv = ((Ivd+Ive)/2 + Ivl)/2

            # add to result
            result["Icv"] = Icv

            # add to full_result
            full_result['Icv'] = {'result': Icv, 'ind_terciarios': {
                'Ivd': Ivd, 'Ive': Ive, 'Ivl': Ivl}}

            # # debug
            # print("\n Ivd:",Ivd,"\n Ive:", Ive, "\n Ivl:", Ivl)
            # print("Indicador de Controle de Vetores  (Icv):", Icv)

        elif i == '4':  # Indicador de Recursos Hídricos (Irh)
            # calcular Iqb
            Iqb = v['Iqb']

            # calcular Idm
            Idm_calc = v['Disp']/v['Dem']

            if Idm_calc > 2:
                Idm = 100
            elif Idm_calc <= 2 and Idm_calc > 1.5:
                Idm = 50
            elif Idm_calc <= 1.5:
                Idm = 0

            # calcular Ifi
            if v['NAA'] == -1 and v['NAR'] == -1:  # não tem fontes isoladas, usar média
                Ifi = False
            else:
                Ifi_calc = (v['NAA']/v['NAR'])*100

                if Ifi_calc >= 100:
                    Ifi = 100
                elif Ifi_calc < 100 and Ifi_calc >= 95:
                    Ifi = 80
                elif Ifi_calc < 95 and Ifi_calc >= 85:
                    Ifi = 60
                elif Ifi_calc < 85 and Ifi_calc >= 70:
                    Ifi = 40
                elif Ifi_calc < 70 and Ifi_calc >= 50:
                    Ifi = 20
                elif Ifi_calc < 50:
                    Ifi = 0

            # calculando Indicador de Recursos Hídricos (Irh)
            if Ifi is False:
                Irh = (Iqb+Idm)/2
            else:
                Irh = (Iqb+Idm+Ifi)/3

            # add to result
            result["Irh"] = Irh

            # add to full_result
            full_result['Irh'] = {'result': Irh, 'ind_terciarios': {
                'Iqb': Iqb, 'Idm': Idm, 'Ifi': Ifi}}

            # # debug
            # print("\n Iqb:",Iqb,"\n Idm:", Idm, "\n Ifi:", Ifi)
            # print("Indicador de Recursos Hídricos (Irh):", Irh)

        elif i == '5':  # Indicador Socioeconômico (Ise)
            # calculando Isp
            Isp = 0.7*v['Imh'] + 0.3*v['Imr']
            # TODO adicionar calculo dos quartis

            # calculando Irf
            Irf = 0.7*v['I2s'] + 0.3*v['Irm']
            # TODO adicionar calculo dos quartis

            # calculando Ied
            Ied = 0.6*v['Ine'] + 0.4*v['Ie1']
            # TODO adicionar calculo dos quartis

            # calculando Indicador Socioeconômico (Ise)
            Ise = (Isp+Irf+Ied)/3

            # add to result
            result["Ise"] = Ise

            # add to full_result
            full_result['Ise'] = {'result': Ise, 'ind_terciarios': {
                'Isp': Isp, 'Irf': Irf, 'Ied': Ied}}

            # # debug
            # print("\n Isp:",Isp,"\n Irf:", Irf, "\n Ied:", Ied)
            # print("Indicador Socioeconômico (Ise):", Ise)

    return [result, full_result]


def Processar_ISA(dict: dict, pesos):
    """Calcula o ISA a partir de um dicionario contendo os indicadores secundarios"""
    # TODO testar pesos e indicadores sec.
    result = 0
    for i in dict:
        # print('peso:', pesos[i], dict[i])
        result += pesos[i]*dict[i]

    result = result/100

    return result


def Processar_ss(ISA):
    """Retorna a situação de salubridade de um floar ou int resultante do calculo de um ISA"""
    if ISA >= 0 and ISA <= 25.5:
        sit = "insalubre"
    elif ISA > 25.5 and ISA <= 50.5:
        sit = "baixa salubridade"
    elif ISA > 50.5 and ISA <= 75.5:
        sit = "media salubridade"
    elif ISA > 75.5 and ISA <= 100:
        sit = "salubre"
    else:
        raise("use valores entre 0 e 100")

    return sit


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def Plot(indicadores, save_location, tittle):
    objects = list(reversed(indicadores.keys()))
    y_pos = arange(len(objects))
    performance_unp = list(reversed(indicadores.values()))

    # substituir 0 por 1 para que os mesmos aparecam no grafico
    performance = []
    for i in performance_unp:
        if i < 1:
            performance.append(1.0)
        else:
            performance.append(i)

    # color_change = ['Iab','Ies', 'Irs', 'Icv', 'Irh', 'Ise']

    # # mudar height
    # height = []
    # for i in objects:
    #     if i in color_change:
    #         height.append(1)
    #     else:
    #         height.append(0.5)
    # print(height)

    fig, ax = plt.subplots(figsize=(3.4, 4.68))
    bars = ax.barh(y_pos, performance, align='center')

    # mudar cores para bater com pontuação
    for i in range(len(performance)):
        if Processar_ss(performance[i]) == 'salubre':
            bars[i].set_color('g')
        elif Processar_ss(performance[i]) == 'media salubridade':
            bars[i].set_color('y')
        elif Processar_ss(performance[i]) == 'baixa salubridade':
            bars[i].set_color('#e67300')
        elif Processar_ss(performance[i]) == 'insalubre':
            bars[i].set_color('r')


    plt.yticks(y_pos, objects)
    plt.xlabel('Pontos')
    plt.title(tittle)

    # plt.show()

    plt.savefig(save_location, transparent=True)
    return save_location


def pickle_dump(location, operation, data=''):
    if operation == "save":
        with open(location, 'wb') as fp:
            try:
                pickle.dump(data, fp)
                return True
            except:
                return False
    elif operation == 'load':
        with open(location, 'rb') as fp:
            try:
                data = pickle.load(fp)
                return [True, data]
            except:
                return [False, None]


# secundarios = Processar_indicadores_secundarios(result)
# print(secundarios)

# isa = Processar_ISA(secundarios, PESOS)
# print('isa: ', isa)

# situacao = Processar_ss(isa)
# print(situacao)
