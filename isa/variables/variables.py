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

# Versioning
VERSION = '0.0.1'

##STATIC DICTS AND LISTS##
TEMA = 'DefaultNoMoreNagging'

PESOS = {'Iab': 25, 'Ies': 25, 'Irs': 25, 'Icv': 10, 'Irh': 10, 'Ise': 5}

SIGLAS = {'0': ['Dua', 'Dut', 'K', 'NAA', 'NAR', 'sistema', 'VP', 'CP', 't', 'K2/K1'],
          '1': ['Due', 'Ice', 'VT', 'VC', 'CT'],
          '2': ['Duc', 'Iqr', 'VL', 'CA'],
          '3': ['Ivd', 'Ive', 'Ivl'],
          '4': ['Iqb', 'Disp', 'Dem', 'NAA', 'NAR'],
          '5': ['Imh', 'Imr', 'I2s', 'Irm', 'Ine', 'Ie1']}

WIDTH_PERGUNTAS = 80

NOMES_INDICADORES = {'Iab': 'Indicador de abastecimento de água', 'Ica': 'Índice de cobertura de atendimento', 'Iqa': 'Índice de qualidade de água distribuída', 'Isa': 'Saturação dos sistemas produtores', 
                    'Ies': 'Indicador de Esgotos Sanitário', 'Ice': 'Índice de cobertura em coleta e tanques sépticos', 'Ite': 'Índice de esgoto tratado e tanque séptico', 'Ist': 'Saturação do sistema de tratamento', 
                    'Irs': 'Indicador de Resíduos Sólidos', 'Icr': 'Índice de coleta de lixo', 'Iqr': 'Tratamento e disposição final dos resíduos', 'Isr': 'Saturação do tratamento e disposição final', 
                    'Icv': 'Indicador de Controle de Vetores ', 'Ivd': 'Índice de controle de dengue', 'Ive': 'Índice de controle de esquistossomose', 'Ivl': 'Índice de controle de leptospirose', 
                    'Irh': 'Indicador de Recursos Hídricos', 'Iqb': 'Índice de qualidade da água bruta', 'Idm': 'Índice de disponibilidade dos mananciais', 'Ifi': 'Índice de Fontes Isoladas', 
                    'Ise':'Indicador Socioeconômico', 'Isp': 'Indicador de saúde pública', 'Irf': 'Indicador de renda familiar', 'Ied': 'Indicador de educação'}

PERGUNTAS = [
    ["Indicador de Abastecimento\nde Água (Iab)", [{'Índice de cobertura de atendimento (Ica)': ['Domicílios urbanos atendidos (público e particulares) (Dua)',
                                                                                                 'Domicílios urbanos totais (Dut)']},

                                                   {'Índice de qualidade de água distribuída (Iqa)': ['Fator - numero de amostras/numero mínimo de amostras a serem efetuadas pelo SAA (k)',
                                                                                                      'Quantidade de amostras consideradas como sendo de água potável relativa à colimetria, cloro e turbidez (NAA)',
                                                                                                      'Quantidade de amostras realizadas (NAR)']},

                                                   {'Saturação dos sistemas produtores (Isa)': ['Tipo de sistema:\n\tSistemas integrados = 1\n\tSistemas Superficiais = 2\n\tSistemas de Poços = 3',
                                                                                                'Volume de produção para atender [m³/ano] (VP)',
                                                                                                'Capacidade de produção [m³/ano] (CP)',
                                                                                                'Taxa anual de crescimento [%] (t)',
                                                                                                'Coeficente de perdas - perda prevista para 5 anos/perda atual [%] (K2/K1)']}
                                                   ]],

    ["Indicador de Esgotos\nSanitário (Ies)", [{'Índice de cobertura em coleta e tanques sépticos (Ice)': ['Domicílios urbanos atendidos por coleta (Due)']},

                                               {'Índice de esgoto tratado e tanque séptico (Ite)': ['Cobertura em Coleta e tanques [%] (Ice)',
                                                                                                    'Volume tratado de esgotos medido ou estimado nas ETE [m³] (VT)',
                                                                                                    'Volume coletado de esgotos [m³] (VC)']},

                                               {'Saturação do sistema de tratamento (Ist)': ['Capacidade de tratamento [m³/ano] (CT)']}

                                               ]],

    ["Indicador de Resíduos\nSólidos (Irs)", [{'Índice de coleta de lixo (Icr)': ['Domicílios urbanos atendidos por coleta de lixo (Duc)']},

                                              {'Tratamento e disposição final dos resíduos (Iqr)': [
                                                  'Índice de qualidade de Aterros de Resíduos sólidos domiciliares – Cetesb (Iqr)']},

                                              {'Saturação do tratamento e disposição final (Isr)': ['Volume coletado de lixo (VL)',
                                                                                                    'Capacidade restante do aterro (CA)']}
                                              ]],

    ["Indicador de Controle\nde Vetores  (Icv) ", [{'Índice de controle de dengue (Ivd)': ['100 pontos: Municípios sem infestação por Aedes Aegypti nos últimos 12 meses \n50 pontos: Municípios infestados por Aedes Aegypti e sem transmissão de dengue nos últimos 5 anos \n25 pontos: Municípios com transmissão de dengue nos últimos 5 anos \n0 pontos: Municípios com ocorrência de dengue hemorrágico']},

                                                   {'Índice de controle de esquistossomose (Ive)': [
                                                       '100 pontos: Municípios sem casos de esquistossomose nos últimos 5 anos \n50 pontos: Municípios com incidência anual menor que 1 \n25 pontos: Municípios com incidência anual maior ou igual a 1 e menor que 5 \n0 pontos: Municípios com incidência anual maior ou igual a 5 (média dos últimos 5 anos)']},

                                                   {'Índice de controle de leptospirose (Ivl)': [
                                                       '100 pontos: Municípios sem enchentes e sem casos de leptospirose no últimos 5 anos \n50 pontos: Municípios com enchentes e sem nenhum caso de leptospirose nos últimos 5 anos \n25 pontos: Municípios sem enchentes e com casos de leptospspirose nos últimos 5 anos \n0 pontos: Municípios com enchentes e com casos de leptospspirose nos últimos 5 anos']}
                                                   ]],

    ["Indicador de Recursos\nHídricos (Irh)", [{'Índice de qualidade da água bruta (Iqb)': ['100 pontos: Poços sem contaminação e sem necessidade de tratamento (desinfecção não considerado como tratamento) \n50 pontos: Poços sem contaminação e com necessidade de tratamento de qualquer natureza \n0 pontos: Poços com riscos de contaminação']},

                                               {'Índice de disponibilidade dos mananciais (Idm)': ['Disponibilidade, água em condições de tratabilidade para abastecimento (Disp)',
                                                                                                   'Demanda (considerar a demanda futura de 10 anos) (Dem)']},

                                               {'Índice de Fontes Isoladas (Ifi)': ['Quantidade de amostras consideradas como sendo de água potável relativa à colimetria, cloro e turbidez - Caso o município não tenha fontes isoladas, entre -1 (NAA)',
                                                                                    'Quantidade de amostras realizadas (NAR) - Caso o município não tenha fontes isoladas, entre -1']}

                                               ]],

    ["Indicador \nSocioeconômico (Ise)", [{'Indicador de saúde pública (Isp)': ['Taxa de mortalidade infantil ( 0 a 4 anos ) ligada a doença de veiculação hídrica (Imh)',
                                                                                'Taxa de mortalidade da população de 60 anos ou mais (Imr)']},

                                          {'Indicador de renda familiar (Irf)': ['Porcentagem de população com renda inferior a 3 (três) salários mínimos. (I2s)',
                                                                                 'Renda média (Irm)']},

                                          {'Indicador de educação (Ied)': ['Porcentagem da população sem nenhuma escolaridade (Ine)',
                                                                           'Porcentagem da população com escolaridade até o 1º grau (Ie1)']}

                                          ]]

]
