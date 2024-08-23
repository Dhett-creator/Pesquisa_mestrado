Para criar um novo projeto e o conectar ao repositório na nuvem:

1 - git init # inicializa o projeto git.
2 - git branch -M <nomeda_branch> # cria uma nova branch local.
3 - git remote add origin <link_do_repositório> # conecta ao branch remoto.
4 - git pull origin <nome_da_branch_desejada> # pucha todo o conteúdo que estiver na branch remota.

Para enviar as mudanças para a nuvem:

1 - git status # visualiza as alterações feitas no projeto local.
2 - git add . # adiciona as mundanças.
3 - git commit -m <"comentário"> # cria o commit/registro de alterações.
4 - git push origin main # envia as alterações para a main.
5 - git push -u origin <nome_da_branch> # cria uma branch se ela não existir. # envia as alterações e cria a branch remota caso ela não exista.
