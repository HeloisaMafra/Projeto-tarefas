    if isinstance(event, str) and event.startswith('-CHECK_'):
        if values[event]:
            # Extrai o ID removendo o prefixo '-CHECK_' e o traço final '-'
            # Exemplo: '-CHECK_1-' vira '1'
            id_num = event.replace('-CHECK_', '').replace('-', '')
            
            # 1. Atualiza no Back-end (SQLite)
            atualizar_status(id_num)
            
            # 2. Atualiza o Front-end
            chave_texto = f'-TXT_{id_num}-'
            
            # Verificamos se a chave existe na janela para evitar o KeyError
            if chave_texto in janela.key_dict:
                texto_orig = janela[chave_texto].get()
                
                # Esconde os elementos originais (Pendentes)
                janela[f'-CHECK_{id_num}-'].update(visible=False)
                janela[chave_texto].update(visible=False)
                
                # CORREÇÃO: Adiciona ao quadro de Concluídas fechando corretamente os colchetes
                janela.extend_layout(janela['-CONCLUIDAS-'],])
