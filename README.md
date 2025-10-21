# Projeto-SDLE

## Descrição

Este projeto permite que usuários criem listas de compras através da interface do usuário. Cada lista é identificada por um ID único (por exemplo, uma URL), que pode ser compartilhado para colaboração. Qualquer usuário com acesso ao ID pode adicionar ou remover itens da lista.

Cada item da lista possui:
- Nome
- Quantidade desejada
- Quantidade atual adquirida (ambas podem ser ajustadas)
- Flag de status indicando se o item foi adquirido

O sistema suporta edição concorrente das listas por múltiplos usuários, visando alta disponibilidade. Inicialmente, utiliza o método Last-Writer-Wins com relógios locais para resolução de conflitos, com possibilidade de evolução para CRDTs (Conflict-free Replicated Data Types) para maior robustez em ambientes distribuídos.

- linguagem: python
- database: SQLite
- interface: Tkinter
- api: Zeromq
- sistema de controle de versão: Git
- sistema operacional: multiplataforma