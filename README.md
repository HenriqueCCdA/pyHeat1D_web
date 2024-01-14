# PyHeat1D Web

Aplicação web para solução de problemas de transporde de calor 1D. O aplicação foi feita utilizando Djando.

O método utilizado para resolvere o problema foi o método dos volumes fintos elementos finitos. O códido pode ser encontrado no [repo](https://github.com/HenriqueCCdA/pyHeat1D)


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
task report_server
```

## Postgres

Para usar o `postgres` basta definir a variável de ambiente:

```
DATABASE_URL=postgres://pyheat1d_web_user:123456@localhost:5432/pyheat1d_web_db
```

Subindo o contenier do `postgres`

```bash
docker compose up database
```

Caso queira usar o sqlite basta apenas não definir `DATABASE_URL`


## Redis

Docker compose para subir o postgres e o redis

```bash
docker compose up redis
```

## Celery

Como broker foi utilizando o `redis`. Para subir o redis:

```bash
docker compose up redis
```

Subindo o worker do celery localmente:

```bash
watchfiles --filter python 'celery -A pyheat1d_web.celery worker --concurrency=2  -l INFO'
```

Subindo o worker do flower localmente:

```bash
celery --broker=redis://localhost:6379/0 flower --port=5555
```
