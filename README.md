# Excluir Snapshots e AMIs antigos

Essa função tem o objetivo simples (como o nome já diz) de excluir snapshots e AMIs antigos
Existe uma variável chamada $RETENTION_DAYS responsável por definir quantos dias de backup você deseja manter

#### Requerimentos
+ **Runtime:** Python 3.6
+ **LambdaHandler:** main.handler
+ **Timeout:** 30
+ **Variáveis de ambiente:**
    * RETENTION_DAYS: 4
    * ACCOUNT_ID: id da conta que é owner dos AMIs e Snapshots (no caso a conta em q o lambda será executado)

**Obs:**
Coloque a TAG "protegido" com o valor "sim" (com o valor pokemon também funciona, não existe uma verificação pra isso) para AMIs/Snapshots que não podem ser excluídos de jeito nenhum. Assim o código ignora esses itens mesmo que eles tenham uma idade maior que o período de retenção desejado
