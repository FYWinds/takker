import os
import glob


def get_all_models(model_path: str) -> list[str]:
    """
    :说明: `_get_all_model`
    > 获取该目录下所有的py文件，转换为tortoise认可的model格式

    :参数:
        * `model_path: str`: 目录

    :返回:
        - `list[str]`: model列表
    """
    # _models: list[str] = []

    # def _get_all_models(
    #     model_path: str, _temp_path: t.Optional[str] = None
    # ) -> list[str]:
    #     for _file in os.listdir(model_path):
    #         if _file.endswith(".py"):
    #             _models.append(f"models.{_temp_path or ''}{_file[:-3]}")
    #         elif os.path.isdir(f"{model_path}/{_file}") and _file != "__pycache__":
    #             _models.extend(
    #                 _get_all_models(
    #                     f"{model_path}/{_file}", f"{_temp_path or ''}{_file}."
    #                 )
    #             )

    #     return _models

    # return _get_all_models(model_path, None)

    # 使用glob模块的版本，但是效率是上面的一半左右
    return list(
        map(
            lambda x: f"models.{x.replace(os.sep, '.')[:-3]}",
            glob.glob(r"**/*.py", root_dir=model_path, recursive=True),
        )
    )
