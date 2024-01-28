import json
from pathlib import Path

from django.conf import settings


def _get_simulations_base_folder():
    return Path(settings.MEDIA_ROOT)


def create_or_update_simulation_case(new_case, indent=2, input_file=None):
    """Cria ou atualiza o arquivo de caso.json. Caso input_file seja diferente de None
    o arquivo será atualizado

    Args:
        new_case (Dict): Dicionario com os dados das análises da interface web
        indent (int, optional): Indentação do json. Defaults to 2.
        input_file (Path, optional): O caminho do aquivo se ele já existir case.json. Defaults to None.

    Returns:
        Path: Retorna o caminho do aquivo criado
    """

    new_case = new_case.copy()

    bcs = {
        "lbc": {"type": 1, "params": {"value": new_case.pop("lbc_value")}},
        "rbc": {"type": 1, "params": {"value": new_case.pop("rbc_value")}},
    }

    props = {"k": 1.0, "ro": 1.0, "cp": 1.0}

    new_case.update(bcs)
    new_case.update({"prop": props, "write_every_steps": 100})

    if not input_file:
        base_folder = _get_simulations_base_folder()
        tag = new_case.pop("tag")
        simulation_folder = base_folder / tag
        if not simulation_folder.exists():
            simulation_folder.mkdir(parents=True)
        case_file = base_folder / f"{tag}/case.json"
    else:
        case_file = input_file

    # TODO: trata a exceção
    json.dump(new_case, case_file.open(mode="w"), indent=indent)

    return case_file


def delete_simulation_folder(input_file):
    """Delete a pasta da simulação

    Args:
        input_file (Path): Arquivo de caso da simulação
    """

    if input_file.exists():
        input_file.unlink()

    base_dir = input_file.parent

    mesh_file = base_dir / "mesh.json"
    if mesh_file.exists():
        mesh_file.unlink()

    results_file = base_dir / "results.json"
    if results_file.exists():
        results_file.unlink()

    base_dir.rmdir()



def cleaned_isteps(query_list, max_istep):
    """Gera um lista de passo de tempo de um lista

    Args:
        query_list (list[str]): Lista de passos de tempos
        max_istep (int): Valor máximo permitido para o passo de tempo.

    Returns:
        list[str]: Retorna uma lista de passos de tempo
    """

    isteps = []

    for query_item in query_list:

        n = int(query_item)

        if n < 0:
            raise ValueError("O passo de tempo não pode ser negativo.")
        elif n >= max_istep:
            raise ValueError(f"O passo de tempo não pode ser maior ou igual a {max_istep}.")

        isteps.append(n)

    return isteps
