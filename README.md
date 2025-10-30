# Projeto-SDLE

Aplicativo de Lista de Compras (local-first) com interface em Tkinter e opção de CLI.

## Funcionalidades

- Login simples por nome (sem senha)
- Criar e remover listas
- Visualizar listas próprias e compartilhadas
- Adicionar, remover e listar itens de uma lista
- Alternar status de item (marcado/não marcado)
- Ajustar quantidade desejada e quantidade adquirida

Persistência local utilizando SQLite.

## Requisitos

- Python 3.10+ (recomendado)
- Tk inter (módulo padrão do Python). Em algumas distribuições Linux pode ser necessário instalar o pacote do sistema: `sudo apt-get install python3-tk`.

Não há dependências externas via pip para a versão Tkinter.

## Configuração com .venv

Crie e ative um ambiente virtual local e inicialize o banco:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # opcional; arquivo pode estar vazio
python -c "from src import db; db.init_db()"
```

## Como executar

Interface Tkinter (GUI):

```bash
python main_tk.py
```

Interface de linha de comando (CLI):

```bash
python main.py
```

## Estrutura do projeto (parcial)

- `main_tk.py`: ponto de entrada da GUI Tkinter
- `main.py`: CLI com as mesmas operações
- `src/db.py`: conexão e inicialização do SQLite
- `src/client.py`: operações de usuário
- `src/list.py`: operações de listas
- `src/item.py`: operações de itens
- `src/Ui/ui_tk.py`: implementação da interface Tkinter
- `data/database.sql`: schema do banco

## Notas

- Se já existir um arquivo `data/db.sqlite` de uma versão anterior e você quiser reinicializar o schema, apague o arquivo ou adapte `db.init_db()` para aceitar `force=True`.
	- Observação: o schema foi alterado para incluir um campo `name` em `shopping_lists`.
		Se você tem um banco existente (data/db.sqlite) criado antes desta alteração, remova-o antes de rodar `db.init_db()` novamente:

		```bash
		rm -f data/db.sqlite
		python -c "from src import db; db.init_db()"
		```
- Em Linux, se ao executar a GUI ocorrer erro de import do Tk (`_tkinter`), instale `python3-tk` via gerenciador de pacotes do sistema.