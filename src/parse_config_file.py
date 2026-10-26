from pydantic import BaseModel, Field


class Parse_Config(BaseModel):
    lives: int = Field(gt=0)
    seed: int
    level_max_time: int = Field(gt=0, lt=90, default=90)
    points_per_pacgum: int = Field(gt=0, default=10)
    points_per_super_pacgum: int = Field(gt=0, default=20)
    points_per_ghost: int = Field(gt=0, default=50)
    levels: list[Level]


class Level(BaseModel):
    width: int = Field(gt=2)
    height: int = Field(gt=2)


def parse_config_file(file: str = "config.json") -> Parse_Config:
    try:
        with open(file, 'r') as fd:
            config = Parse_Config.model_validate_json(fd.read())
    except PermissionError:
        print("oopsie")
    return config


if __name__ == "__main__":
    print(parse_config_file())
