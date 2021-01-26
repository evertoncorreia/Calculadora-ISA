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

#imports
import PySimpleGUI as sg
from collections import OrderedDict
from tempfile import TemporaryDirectory as TmpFolder

import sys
import re

#local imports
import isa.variables as variables
from isa.functions import *

sg.theme(variables.TEMA)      # Add some color to the window

WIDTH_PERGUNTAS = variables.WIDTH_PERGUNTAS

PERGUNTAS = variables.PERGUNTAS

PESOS = variables.PESOS

NOMES_INDICADORES = variables.NOMES_INDICADORES

ICON = resource_path('icon.ico')

#set debug flag
if len(sys.argv) == 2:
    if sys.argv[-1] == '-d':
        DEBUG = True
    else:
        raise SystemExit("only debug flag is available, use -d")
elif len(sys.argv) > 1:
    raise SystemExit("only debug flag is available, use -d")
else:
    DEBUG = False

def make_window(list):
    # make tabs
    sg_Tabs = []
    for index_1 in range(0, len(list)):
        i = list[index_1]
# [sg.Frame('Resultados', result_layout, font='Any 12', title_color='blue'), sg.Frame('Gráfico', frame_layout, font='Any 12', title_color='blue')]
        # make frame
        frame_layout = []
        for index in range(0, len(i[1])):
            quest = i[1][index]
            indicaor = i[1][index]
            indicaor = [*indicaor][0]
            questions = i[1][index][indicaor]
            # adicionar nome do subindicador na ui
            # frame_layout.append(
            #     [sg.Text(indicaor, font=('Arial', 12), size=[WIDTH_PERGUNTAS+10, 0], justification='center')])
            add = []
            for b in range(0, len(questions)):
                question = questions[b]
                add.append([sg.Text(question, size=[WIDTH_PERGUNTAS+10, 0]), sg.Input(
                    '', key=str(index_1)+"_"+str(index)+"_"+str(b), size=[10, 0], enable_events=True)])
            add.append([sg.Text('', font='Any 2')])
            # adicinar novas linhas e caixas de texto em um frame
            ret = [sg.Frame(indicaor, add, font='Any 12', title_color='black')]
            frame_layout.append(ret)


        sg_Tabs.append(sg.Tab(i[0], frame_layout))
    return [sg_Tabs]


def process_results(values):
    # make keys
    # print(values)
    keys = set([x.split("_")[0] for x in values if x.split("_")[0]])
    dict = {}
    for i in keys:
        dict[i] = []

    for i in values:
        key_v = i.split("_")[0]
        if values[i] != '':
            dict[key_v].append(values[i])
        else:
            dict[key_v].append(None)
    
    return OrderedDict(sorted(dict.items()))

# menu_def = [['File', ['Open', 'Save', 'Exit'  ]],      
# 			['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
# 			['Help', 'Sobre...'], ]  

menu_def = [['Arquivo', ['Abrir Projeto', 'Salvar Projeto', 'Sair'  ]],
    ['Ajuda', 'Sobre...']]  

layout = [[sg.Menu(menu_def, )],
    [sg.Image(resource_path('deciv.png')), sg.T('Calculadora de Indicador de Salubridade Ambiental (ISA) - Departamento de Engenharia Civil da UFSCar', font='Any 12', text_color='blue',size=[WIDTH_PERGUNTAS-7, 0], justification='center'), sg.Image(resource_path('ufscar.png'))],
    [sg.TabGroup(make_window(PERGUNTAS))],
    # [sg.T('Calculadora de Indicador de Salubridade Ambiental (ISA) - Departamento de Engenharia Civil da UFSCar', font='Any 12', text_color='blue',size=[WIDTH_PERGUNTAS+15, 0], justification='right')],
    # [sg.Submit(button_text="Calcular"), sg.Cancel(button_text="Cancelar")]
    [sg.Submit(button_text="Calcular"), sg.T('Aluno: Everton Juan Cardoso Correia\nOrientadora: Profa. Dra. Katia Sakihama Ventura', font='Any 12', text_color='blue',size=[WIDTH_PERGUNTAS+9, 0], justification='right')]
]

window = sg.Window('Calculadora de Indicador de Salubridade Ambiental (ISA) - Departamento de Engenharia Civil da UFSCar', layout, icon=ICON)

win2_active = False


while True:
    event, values = window.read()

    if event == None or event == 'Sair':
        raise SystemExit("Closed by user")
        break
    
    # removendo caracteres invalidos do imput
    if bool(re.match("[0-9]_[0-9]_[0-9]$", event)):
        # aceitar apenas 1, 2 ou 3
        if event == '0_2_0':
            val = values[event]
            if val and val[-1] not in ('123'):
                window[event].update(values[event][:-1])
            else:
                if len(val) > 1:
                    window[event].update(values[event][:-1])
        elif event in ['3_0_0','3_1_0','3_2_0','4_0_0']: #100,50,25,0 100,50,0
            val = values[event]
            if val and val[-1] not in ('0123456789'):
                window[event].update(values[event][:-1])
            
            # aceitar 100
            if val.startswith('1'):
                if len(val) > 1:
                    if val[-1] == '0':
                        if len(val) > 3:
                            window[event].update(values[event][:-1])
                    else:
                        window[event].update(values[event][:-1])

            # aceitar 50
            elif val.startswith('5'):
                if len(val) > 1:
                    if val[-1] == '0':
                        if len(val) > 2:
                            window[event].update(values[event][:-1])
                    else:
                        window[event].update(values[event][:-1])

            # aceitar 25
            elif val.startswith('2'):
                if event not in ['4_0_0']:
                    if len(val) > 1:
                        if val[-1] == '5':
                            if len(val) > 2:
                                window[event].update(values[event][:-1])
                        else:
                            window[event].update(values[event][:-1])
                else:
                    window[event].update(values[event][:-1])

            # aceitar 0
            elif val.startswith('0'):
                if len(val) > 1:
                    window[event].update(values[event][:-1])


            else:
                window[event].update(values[event][:-1])

        else:
            if values[event] and values[event][-1] not in ('0123456789,-'):
                window[event].update(values[event][:-1])
            if '-' in values[event]:
                if values[event].index('-') != 0 or values[event].count('-') > 1:
                    window[event].update(values[event][:-1])
            if ',' in values[event]:
                if values[event].index(',') == 0 or values[event].count(',') > 1:
                    window[event].update(values[event][:-1])    



    if event == 'Sobre...':
        sg.popup('sobre sobre', f'Versão {variables.VERSION}', 'Licença de software: GNU General Public License')
    
    if event == 'Salvar Projeto':
        # abrir popup de salvamento
        filename = sg.popup_get_file('Salvar arquivo', no_window=True, save_as=True, default_extension="isa", file_types=(("Arquivos de Calculadora ISA", "*.isa"),))

        # testar se usuario cancelou ao invés de salvar
        if filename != '':
            #generate saving dict
            saving_dict = {}
            for i in values:
                if bool(re.match("[0-9]_[0-9]_[0-9]$", str(i))):
                    saving_dict[i] = values[i]
            
            #salvar dict
            pickle_dump(filename, "save", saving_dict)

    if event == 'Abrir Projeto':
        # abrir popup de salvamento
        filename = sg.popup_get_file('Abrir arquivo', no_window=True, file_types=(("Arquivos de Calculadora ISA", "*.isa"),))
            
        if filename != '':
            #load dict
            err, loaded_dict = pickle_dump(filename, "load")
            if err == True:
                for i in loaded_dict:
                    i_val = loaded_dict[i]
                    window[i].update(i_val)



    if not win2_active and event == 'Calcular':
        #converter values de string para float, substituind , por .
        float_values = {}
        for i in values:
            if bool(re.match("[0-9]_[0-9]_[0-9]$", str(i))):
                if values[i] not in ("", None):
                    if ',' in values[i]:
                        float_values[i] = float(values[i].replace(',','.'))
                    else:
                        float_values[i] = float(values[i].replace(',','.'))
                else:
                    float_values[i] = values[i]
        
        # checar se faltou dados
        if '' in [float_values[x] for x in float_values] and DEBUG is False: # faltou dados, alertar usuário
            sg.popup('Por favor, preencha todos os campos antes de calcular o ISA.')

        else: # sem dados faltantes
            # data do usuario
            user_data = process_results(float_values)

            #user_data falso para debug, dados de araraquara
            if DEBUG:
                user_data = {'0': [217138, 223900, 0.6346, 225.18, 142.92, 1, 35823.1, 47830, 1.197, 1.25], 
                '1': [223521, 100, 18221.95, 18221.95, 19824],
                '2': [217541, 10, 74602.35, 1122437.415],  
                '3': [0, 0, 0], 
                '4': [0, 10.62, 208.9, 225.18, 142.92], 
                '5': [0.0105, 0.0338, 2.64, 0.43, 4.3, 16.2]}

            # processando dados
            indicadores_secundarios, indicadores_sec_terc = Processar_indicadores_secundarios(user_data)
            isa = Processar_ISA(indicadores_secundarios, PESOS)
            situacao = Processar_ss(isa)
            
            #unesting indicadores
            print_sring = ''
            unested_indicadores_sec_terc = OrderedDict()
            unested_indicadores_sec = OrderedDict()
            unested_indicadores_terc = OrderedDict()
            for i in indicadores_sec_terc:
                res = indicadores_sec_terc[i]['result']
                if print_sring == '':
                    print_sring += f'{NOMES_INDICADORES[i]} ({i}) = {round(res)} pontos'
                else:
                    print_sring += f'\n\n{NOMES_INDICADORES[i]} ({i}) = {round(res)} pontos'

                unested_indicadores_sec_terc[i] = indicadores_sec_terc[i]['result']
                unested_indicadores_sec[i] = indicadores_sec_terc[i]['result']
                for j in indicadores_sec_terc[i]['ind_terciarios']:
                    res_terc = indicadores_sec_terc[i]['ind_terciarios'][j]
                    print_sring += f'\n\t{NOMES_INDICADORES[j]} ({j}) = {round(res_terc)} pontos'

                    unested_indicadores_sec_terc[j] = indicadores_sec_terc[i]['ind_terciarios'][j]
                    unested_indicadores_terc[j] = indicadores_sec_terc[i]['ind_terciarios'][j]

            #TODO adicionar opção de salvar relatório, preferencialmente em excel ou word
            window.Disappear() # hide main window
            win2_active = True

            with TmpFolder() as tmp:
                # criar png do gráfico na tmp
                current_plot = 0
                main_plot = Plot(unested_indicadores_sec_terc, f'{tmp}/0.png', 'Todos Indicadores')
                sec_plot = Plot(unested_indicadores_sec, f'{tmp}/1.png', 'Indicadores de Segunda Ordem')
                third_plot = Plot(unested_indicadores_terc, f'{tmp}/2.png', 'Indidcadores de Terceira Ordem')

                def get_bg_color(situacao):
                    if situacao == 'salubre':
                        bg_color = 'green'
                    elif situacao == 'media salubridade':
                        bg_color = 'yellow'
                    elif situacao == 'baixa salubridade':
                        bg_color = 'orange'
                    elif situacao == 'insalubre':
                        bg_color = 'red'
                    else:
                        bg_color = 'white'

                    return bg_color

                frame_layout = [
                    # [sg.Button('<', disabled=True), sg.Image(main_plot, key='-plot-'), sg.Button('>')]
                    [sg.Button('Anterior', disabled=True), sg.Button('Próximo')],
                    [sg.Image(main_plot, key='-plot-')]
                                ]
                result_layout = [[sg.Text(print_sring, font='Any 9')], 
                                [sg.Text(f'Indicador de Salubridade Ambiental = {round(isa)} pontos', font='Any 12')],
                                [sg.Text(f'Situação: {situacao.title()}', font='Any 11', background_color=get_bg_color(situacao), size=[47, 0], justification='center')]
                                ]

                layout2 = [
                    [sg.Image(resource_path('deciv.png')), sg.T('Calculadora de Indicador de Salubridade Ambiental (ISA) - Departamento de Engenharia Civil da UFSCar', font='Any 12', text_color='blue',size=[WIDTH_PERGUNTAS-7, 0], justification='center'), sg.Image(resource_path('ufscar.png'))],
                    [sg.Frame('Resultados', result_layout, font='Any 12', title_color='blue'), sg.Frame('Gráficos', frame_layout, font='Any 12', title_color='blue')],
                    [ sg.Button('Voltar'), sg.T('Aluno: Everton Juan Cardoso Correia\nOrientadora: Profa. Dra. Katia Sakihama Ventura', font='Any 12', text_color='blue',size=[WIDTH_PERGUNTAS+11, 0], justification='right')]
                    ]

                window2 = sg.Window('Resultados', layout2)

                while True:
                    #blocks window
                    event2, value2 = window2.Read()
                    if event2 is None or event2 == 'Voltar':
                        win2_active  = False
                        window2.close()
                        window.Reappear() # unhide main window
                        break

                    if event2 == 'Próximo':
                        if current_plot < 2:
                            current_plot += 1
                        else:
                            current_plot = 0
                        
                        #update plot
                        window2['-plot-'].update(f'{tmp}/{str(current_plot)}.png')
                        
                        #disable button
                        if current_plot == 2:
                            window2['Próximo'].update(disabled=True)

                        #reenable anterior
                        if current_plot != 0:
                            window2['Anterior'].update(disabled=False)

                    if event2 == 'Anterior':
                        if current_plot < 1:
                            current_plot = 2
                        else:
                            current_plot -= 1
                                        
                        #update plot
                        window2['-plot-'].update(f'{tmp}/{str(current_plot)}.png')
                        
                        #disale anterior
                        if current_plot == 0:
                            window2['Anterior'].update(disabled=True)
                        #reenable proximo
                        if current_plot != 2:
                            window2['Próximo'].update(disabled=False)