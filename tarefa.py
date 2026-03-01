import FreeSimpleGUI as sg

def criar_nova_tarefa():
    sg.theme('DarkBlue4')
    
    layout = [
        [sg.Frame('Pendentes', [[]], key='-PENDENTES-', expand_x=True, expand_y=True)],
        [sg.Frame('Concluídas', [[]], key='-CONCLUIDAS-', expand_x=True, expand_y=True)],
        [sg.Button('Nova tarefa', size=(12, 1)), sg.Button('Limpar Tudo', size=(12, 1)), sg.Button('Sair', size=(8, 1))]
    ]
    
    return sg.Window('Gerenciador de Tarefas', layout, finalize=True, resizable=True, size=(450, 550))

janela = criar_nova_tarefa()
contador = 0

while True:
    event, values = janela.read()
    
    if event in (sg.WIN_CLOSED, 'Sair'):
        break
        
    if event == 'Nova tarefa':
        contador += 1
        # Criamos a nova linha para o frame de pendentes
        nova_linha = [
            [sg.Checkbox('', key=f'-CHECK_{contador}-', enable_events=True), 
             sg.Input('', key=f'-IN_{contador}-', expand_x=True)]
        ]
        janela.extend_layout(janela['-PENDENTES-'], nova_linha)
    
    # Lógica para detectar o clique no checkbox
    if isinstance(event, str) and event.startswith('-CHECK_'):
        if values[event]: # Se o checkbox foi marcado
            # Extrai o número do ID da chave (ex: de '-CHECK_1-' pega '1')
            id_num = event.split('_')[1].replace('-', '')
            
            # Pega o texto que o usuário digitou
            texto_tarefa = values[f'-IN_{id_num}-']
            
            # Se o campo estiver vazio, usamos um texto padrão
            if not texto_tarefa.strip():
                texto_tarefa = "(Tarefa sem nome)"
            
            # 1. Esconde os elementos originais (pendentes)
            janela[f'-IN_{id_num}-'].update(visible=False)
            janela[f'-CHECK_{id_num}-'].update(visible=False)
            
            # 2. Cria uma nova representação visual no quadro de Concluídas
            layout_concluido = [
                [sg.Text(texto_tarefa, key=f'-TEXTO_{id_num}-')]
            ]
            janela.extend_layout(janela['-CONCLUIDAS-'], layout_concluido)

    if event == 'Limpar Tudo':
        janela.close()
        janela = criar_nova_tarefa()
        contador = 0

janela.close()
