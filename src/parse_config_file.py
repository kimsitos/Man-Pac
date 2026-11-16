from pydantic import BaseModel, Field, ValidationError
import sys


class Level(BaseModel):
    width: int = Field(gt=2)
    height: int = Field(gt=2)


class Config(BaseModel):
    lives: int = Field(gt=0)
    seed: int = Field(default=0)
    level_max_time: int = Field(gt=0, default=90)
    points_per_pacgum: int = Field(gt=0, default=10)
    points_per_super_pacgum: int = Field(gt=0, default=20)
    points_per_ghost: int = Field(gt=0, default=50)
    levels: list[Level]


def parse_config_file(file: str = "config.json") -> Config | None:
    config = None
    try:
        with open(file, 'r') as fd:
            config = Config.model_validate_json(fd.read())
    except PermissionError as e:
        print("\033[91mPermission Error:\033[0m", e)
    except FileNotFoundError as e:
        print("\033[91mFile not found Error:\033[0m", e)
    except ValidationError as e:
        print(f"\033[91mValidation Error:\033[0m {file} file", e)

    if not config:
        sys.exit(1)
    return config
