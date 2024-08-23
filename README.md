# Procedimentos Git

### :hammer_and_wrench: Para criar um novo projeto e o conectar ao repositório na nuvem:
```bash
 ~ git init # inicializa o projeto git.
 ~ git branch -M <nomeda_branch> # cria uma nova branch local.
 ~ git remote add origin <link_do_repositório> # conecta a branch remota.
 ~ git pull origin <nome_da_branch_desejada> # pucha todo o conteúdo que estiver na branch remota.
```

### :outbox_tray: Para enviar as mudanças para a nuvem:
```bash
 ~ git status # visualiza as alterações feitas no projeto local.
 ~ git add . # adiciona as mundanças.
 ~ git commit -m <"comentário"> # cria o commit/registro de alterações.
 ~ git push origin main # envia as alterações para a main.
 ~ git push -u origin <nome_da_branch> # cria uma branch se ela não existir. # envia as alterações e cria a branch remota caso ela não exista.
```
