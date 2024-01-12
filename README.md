# PyHeat1D Web

Aplicação web para solução de problemas de transporde de calor 1D. O aplicação foi feita utilizando Djando.

O método utilizado para resolvere o problema foi o método dos volumes fintos elementos finitos. O códido pode ser encontrado no [repo](https://github.com/HenriqueCCdA/)


## Ambiente de desenvolvimento local

Para instalar as dependencias basta:

```bash
poetry install
```

Como ferramentas de desenvolcimento foram utilizadas o `black`, `ruff`, `taskipy`, `coverage` e `pytest`.

Para listar todas as possibilidades do `taskipy` basta:

```bash
task -l
```

Os princiais comandos são `fmt`, `linter`e `tests`. Por exemplos, para formatar o código basta simplesmente usar o camando:

```bash
task fmt
```

Para gerar o relatório de ded cobertura temos o camando

```bash
task test_report
```

Para ver o relatório no navegador

```bash
report_server
```
