import FreeSimpleGUI as sg
import sqlite3

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, status INTEGER)''')
    conn.commit()
    return conn

# --- INTERFACE ---
def criar_janela():
    sg.theme('DarkBlue4')
    
    col_pendentes = [
        [sg.Column([[]], key='-COL-PENDENTES-', scrollable=True, vertical_scroll_only=True, expand_x=True, size=(400, 200))]
    ]
    
    col_concluidas = [
        [sg.Column([[]], key='-COL-CONCLUIDAS-', scrollable=True, vertical_scroll_only=True, expand_x=True, size=(400, 200))]
    ]

    layout = [
        [sg.Frame('Tarefas Ativas', col_pendentes, expand_x=True)],
        [sg.pin(sg.Frame('Concluídas', col_concluidas, key='-FRAME-CONCLUIDAS-', visible=False, expand_x=True))],
        [sg.Button('Nova tarefa'), sg.Button('Salvar Alterações', button_color=('white', 'green')), 
         sg.Button('Ver Concluidas'), sg.Button('Sair')]
    ]
    
    return sg.Window('Gerenciador de Tarefas', layout, finalize=True, resizable=True, size=(450, 650))

# --- FUNÇÕES DE APOIO ---
def add_pendente(janela_ref, id_db, texto=""):
    # O campo sg.Input já permite a edição direta
    linha = [[sg.Checkbox('', key=f'-CH_{id_db}-', enable_events=True), 
              sg.Input(texto, key=f'-IN_{id_db}-', expand_x=True)]]
    janela_ref.extend_layout(janela_ref['-COL-PENDENTES-'], linha)
    janela_ref['-COL-PENDENTES-'].contents_changed()

def add_concluida(janela_ref, texto):
    linha = [[sg.Text(texto)]]
    janela_ref.extend_layout(janela_ref['-COL-CONCLUIDAS-'], linha)
    janela_ref['-COL-CONCLUIDAS-'].contents_changed()

def carregar_dados(janela_ref):
    ids_ativos_local = []
    cursor = conn.cursor()
    cursor.execute("SELECT id, texto, status FROM tarefas")
    for tid, txt, status in cursor.fetchall():
        if status == 0:
            add_pendente(janela_ref, tid, txt)
            ids_ativos_local.append(tid)
        else:
            add_concluida(janela_ref, txt)
    return ids_ativos_local

# --- LÓGICA PRINCIPAL ---
conn = init_db()
janela = criar_janela()
mostrar_concluidas = False
ids_ativos = carregar_dados(janela)

while True:
    event, values = janela.read()
    
    if event in (sg.WIN_CLOSED, 'Sair'): 
        break

    if event == 'Nova tarefa':
        c = conn.cursor()
        c.execute("INSERT INTO tarefas (texto, status) VALUES ('', 0)")
        conn.commit()
        novo_id = c.lastrowid
        add_pendente(janela, novo_id)
        ids_ativos.append(novo_id)

    # LÓGICA DE EDIÇÃO: Salva o que foi digitado nos campos Input
    if event == 'Salvar Alterações':
        for tid in ids_ativos:
            key_in = f'-IN_{tid}-'
            if key_in in values:
                txt_editado = values[key_in]
                conn.cursor().execute("UPDATE tarefas SET texto = ? WHERE id = ?", (txt_editado, tid))
        conn.commit()
        sg.popup("Alterações salvas com sucesso!")

    if event == 'Ver Concluidas':
        mostrar_concluidas = not mostrar_concluidas
        janela['-FRAME-CONCLUIDAS-'].update(visible=mostrar_concluidas)

    if isinstance(event, str) and event.startswith('-CH_'):
        tid = int(event.replace('-CH_', '').replace('-', ''))
        # Captura o texto editado no momento do clique no checkbox
        texto_final = values[f'-IN_{tid}-'] or "(Tarefa sem nome)"
        
        conn.cursor().execute("UPDATE tarefas SET texto = ?, status = 1 WHERE id = ?", (texto_final, tid))
        conn.commit()
        
        janela[f'-IN_{tid}-'].update(visible=False)
        janela[f'-CH_{tid}-'].update(visible=False)
        add_concluida(janela, texto_final)
        
        if tid in ids_ativos:
            ids_ativos.remove(tid)

janela.close()
conn.close()
