from pydantic import BaseModel, Field, ValidationError
import sys
from typing import cast


class Level(BaseModel):
    width: int = Field(gt=2, default=15)
    height: int = Field(gt=2, default=15)


class Config(BaseModel):
    lives: int = Field(gt=0)
    seed: int = Field(default=0)
    level_max_time: int = Field(gt=0, default=90)
    points_per_pacgum: int = Field(gt=0, default=10)
    points_per_super_pacgum: int = Field(gt=0, default=20)
    points_per_ghost: int = Field(gt=0, default=50)
    levels: list[Level] = Field(min_length=10, default=[
        Level() for _ in range(10)
        ])


def parse_config_file(file: str = "config.json") -> Config:
    config: Config | None = None
    try:
        with open(file, 'r') as fd:
            final_str = ""
            for line in fd:
                temp_line = line.strip()
                if not temp_line or temp_line.startswith("#"):
                    continue
                final_str += line

            config = cast(Config, Config.model_validate_json(final_str))
    except PermissionError as e:
        print("\033[91mPermission Error:\033[0m", e)
    except FileNotFoundError as e:
        print("\033[91mFile not found Error:\033[0m", e)
    except ValidationError as e:
        print(f"\033[91mValidation Error:\033[0m {file} file", e)

    if not config:
        sys.exit(1)
    return config
