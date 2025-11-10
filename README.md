# Projeto-SDLE

Aplicativo de Lista de Compras (local-first) com interface em Tkinter e sincronização por versão.

## Funcionalidades

- Login simples por nome (sem senha)
- Criar e remover listas (compartilhadas entre todos os usuários)
- Visualizar listas com número de versão
- Adicionar, remover e listar itens de uma lista
- Alternar status de item (marcado/não marcado)
- Ajustar quantidade desejada e quantidade adquirida
- Sistema de versões: Cada modificação incrementa o contador de versão
- Sincronização manual: Botão "Atualizar" sincroniza com a base de dados partilhada
- Múltiplas instâncias: Suporta várias aplicações acessando a mesma BD simultaneamente

Persistência local utilizando SQLite com version counters (Last-Writer-Wins).

## Requisitos

- Python 3.10+ (recomendado)
- Tkinter (módulo padrão do Python)
  - Linux/WSL: `sudo apt install python3-tk`
  - macOS: Incluído com Python (via python.org ou Homebrew)
  - Windows: Incluído com Python

Não há dependências externas via pip.

## Como Executar

### Linux / macOS / WSL

```bash
chmod +x run.sh
./run.sh
```

### Windows (PowerShell/CMD)

```cmd
python main_tk.py
```

Ou use o script batch:
```cmd
run.bat
```

### WSL (Windows Subsystem for Linux)

Opção 1 - Direto do Windows:
```bash
wsl bash run_instance.sh
```

Opção 2 - Dentro do WSL:
```bash
./run.sh
```

## Configuração Detalhada

### Criar ambiente virtual (opcional)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac/WSL
# OU
.venv\Scripts\activate     # Windows
```

### Inicializar base de dados manualmente

```bash
python -c "from src import db; db.init_db()"
```

### Resetar base de dados

```bash
rm -f data/db.sqlite       # Linux/Mac/WSL
python scripts/init_db.py --force
```

## Testar Múltiplas Instâncias (Sincronização)

Para testar o sistema de versões com sincronização:

### No WSL

Terminal 1:
```bash
cd /mnt/c/Users/USER/OneDrive/Ambiente\ de\ Trabalho/sdle/Projeto-SDLE
python3 main_tk.py
```

Terminal 2 (nova janela):
```bash
cd /mnt/c/Users/USER/OneDrive/Ambiente\ de\ Trabalho/sdle/Projeto-SDLE
python3 main_tk.py
```

### Passos de teste

1. Instância 1: Login como "João", criar lista "Supermercado"
2. Instância 2: Login como "Maria", clicar botão "Atualizar" - lista aparece
3. Instância 1: Adicionar item "Leite" - versão da lista incrementa (v0 para v1)
4. Instância 2: Clicar "Atualizar" - ver versão v1 e item "Leite"

Notas:
- Ambas as instâncias partilham a mesma base de dados SQLite
- Versões incrementam automaticamente em cada modificação
- Botão "Atualizar" sincroniza sem reiniciar a aplicação

## Estrutura do Projeto

```
Projeto-SDLE/
├── main_tk.py              # Ponto de entrada GUI (Tkinter)
├── run.sh                  # Script de execução Linux/Mac/WSL
├── run.bat                 # Script de execução Windows
├── run_instance.sh         # Helper para WSL com caminho completo
├── requirements.txt        # Dependências (vazio - usa stdlib)
├── data/
│   ├── database.sql        # Schema SQLite (com version counters)
│   └── db.sqlite           # Base de dados SQLite (criada automaticamente)
├── scripts/
│   └── init_db.py          # Script para inicializar/resetar BD
└── src/
    ├── db.py               # Conexão e inicialização SQLite
    ├── client.py           # Operações de usuário
    ├── list.py             # Operações de listas (com version increment)
    ├── item.py             # Operações de itens (com version increment)
    └── Ui/
        ├── ui_tk.py        # Interface principal Tkinter
        ├── ui_user.py      # Componente de login/user
        ├── ui_list.py      # Componente de listas (com display de versão)
        └── ui_item.py      # Componente de itens (com coluna versão)
```

## Sistema de Versões (Version Counters)

O projeto implementa um sistema básico de version counters para sincronização:

### Como funciona

- Cada `shopping_list` tem um campo `version` (INTEGER) e `last_modified` (TIMESTAMP)
- Cada `item` também tem um campo `version`
- Toda modificação incrementa a versão:
  - Criar/remover item incrementa `version` da lista
  - Marcar/desmarcar item incrementa `version` da lista E do item
  - Alterar quantidade incrementa `version` da lista E do item

### Interface de Usuário

- Listas: Exibem formato `id=X v2 | Nome da Lista`
- Itens: Coluna "Ver" mostra a versão de cada item
- Botão "Atualizar": Recarrega dados da BD mantendo seleção atual
- Status bar: Mostra mensagens de sincronização

### Limitações atuais (protótipo local)

- Last-Writer-Wins (LWW): Último a escrever na BD ganha, sem merge
- Sincronização manual: Precisa clicar "Atualizar" para ver mudanças
- Single-node: Todas as instâncias acessam a mesma BD SQLite local
- Sem resolução de conflitos: Escritas concorrentes sobrescrevem-se

### Próximos passos (SDLE)

Para evoluir para sistema distribuído:

1. CRDTs: Implementar OR-Set, LWW-Element-Set para itens
2. Vector Clocks: Substituir counters simples por timestamps vetoriais
3. Replicação: Adicionar camada de comunicação (ZeroMQ, gRPC)
4. Dynamo-style: Partitioning, consistent hashing, anti-entropy
5. Conflict Resolution: Merge automático de escritas concorrentes

## Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'tkinter'`

Linux/WSL:
```bash
sudo apt update
sudo apt install python3-tk
```

macOS:
```bash
brew install python-tk@3.11  # ajuste versão
```

### Janela não abre no WSL

Windows 11 (WSLg):
- Certifique-se que WSL 2 está instalado: `wsl --status`
- WSLg vem por padrão, janelas devem aparecer automaticamente

Windows 10 (precisa X server):
1. Instale VcXsrv: https://sourceforge.net/projects/vcxsrv/
2. Execute VcXsrv com "Multiple windows" e "Disable access control"
3. No WSL:
   ```bash
   export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0.0
   ```

### Base de dados corrompida

```bash
rm -f data/db.sqlite
python scripts/init_db.py --force
```

## Referências SDLE

- Local-first software: https://www.inkandswitch.com/local-first/
- CRDTs: https://crdt.tech/papers.html
- Amazon Dynamo: https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- ZeroMQ: https://zeromq.org/

---

Projeto desenvolvido para Large Scale Distributed Systems (SDLE)
- Se a janela não aparecer, verifique se não está minimizada ou em outro desktop virtual.