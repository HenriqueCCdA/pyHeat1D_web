import json
from pathlib import Path

from django.conf import settings


class ResultFileNotFoundError(FileNotFoundError):
    def __init__(self, input_file_path):
        msg = f"Arquivo de resultado não achado no caminho '{input_file_path}'"
        super().__init__(msg)


def _get_simulations_base_folder(pk):
    return Path(settings.MEDIA_ROOT) / f"{pk}"


def create_or_update_simulation_case(new_case, user, indent=2, input_file=None):
    """Cria ou atualiza o arquivo de caso.json. Caso input_file seja diferente de None
    o arquivo será atualizado

    Args:
        new_case (Dict): Dicionario com os dados das análises da interface web.
        user (User): Usuário dono da analise.
        indent (int, optional): Indentação do json. Defaults to 2.
        input_file (Path, optional): O caminho do aquivo se ele já existir case.json. Defaults to None.

    Returns:
        Path: Retorna o caminho do aquivo criado
    """

    case = new_case.copy()

    bcs = {
        "lbc": {"type": 1, "params": {"value": case.pop("lbc_value")}},
        "rbc": {"type": 1, "params": {"value": case.pop("rbc_value")}},
    }

    props = {"k": 1.0, "ro": 1.0, "cp": 1.0}

    case.update(bcs)
    case.update({"prop": props, "write_every_steps": 100})

    if not input_file:
        base_folder = _get_simulations_base_folder(user.pk)
        tag = case.pop("tag")
        simulation_folder = base_folder / tag
        if not simulation_folder.exists():
            simulation_folder.mkdir(parents=True)
        case_file = base_folder / f"{tag}/case.json"
    else:
        case_file = input_file

    # TODO: trata a exceção
    json.dump(case, case_file.open(mode="w"), indent=indent)

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


def read_mesh(base_folder):
    mesh_file_path = base_folder / "mesh.json"
    return json.load(mesh_file_path.open())


def read_results(base_folder):
    result_file_path = base_folder / "results.json"
    return json.load(result_file_path.open())


def results_times(input_file_path):
    """Le o arquivo de resultados obtem os tempos

    Args:
        input_file_path (str| Path): Caminho do arquivo de resultados

    Returns:
        list[float]: Lista com os tempos
    """

    if isinstance(input_file_path, str):
        input_file_path = Path(input_file_path)

    folder_base = input_file_path.parent

    try:
        results = read_results(folder_base)
    except FileNotFoundError as e:
        raise ResultFileNotFoundError(folder_base) from e

    return [round(r["t"], 6) for r in results]
