# QUICK START - Como Executar o Projeto

## Comandos Rápidos

### Windows (PowerShell/CMD)
```cmd
python main_tk.py
```

### Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

### WSL (Windows Subsystem for Linux)
```bash
# Opção 1: Dentro do WSL
cd "/mnt/c/Users/USER/OneDrive/Ambiente de Trabalho/sdle/Projeto-SDLE"
./run.sh

# Opção 2: Do PowerShell
wsl bash run_instance.sh
```

---

## Pré-requisitos

- Python 3.10+
- Tkinter instalado:
  - Linux/WSL: `sudo apt install python3-tk`
  - macOS/Windows: Vem com Python

---

## Testar com 2 Instâncias (Sincronização)

### Passo a passo

Terminal 1:
```bash
cd Projeto-SDLE
python3 main_tk.py
```

Terminal 2 (nova janela):
```bash
cd Projeto-SDLE
python3 main_tk.py
```

### Teste de sincronização

1. Janela 1: Login como "João", criar lista "Supermercado"
2. Janela 2: Login como "Maria", clicar botão "Atualizar" 
   - Lista "Supermercado" aparece
3. Janela 1: Adicionar item "Leite" 
   - Versão muda de v0 para v1
4. Janela 2: Clicar "Atualizar" novamente
   - Versão agora é v1
   - Item "Leite" aparece

---

## Resetar Base de Dados

```bash
rm -f data/db.sqlite
python scripts/init_db.py --force
```

---

## Problemas Comuns

### Erro: `ModuleNotFoundError: No module named 'tkinter'`
```bash
# Linux/WSL
sudo apt update && sudo apt install python3-tk

# macOS
brew install python-tk@3.11
```

### Janela não abre no WSL (Windows 10)
1. Instale VcXsrv
2. Execute VcXsrv
3. No WSL: `export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0.0`

---

Veja README.md completo para mais detalhes
