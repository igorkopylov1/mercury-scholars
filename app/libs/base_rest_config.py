import os


class BaseRestConfig:
    _required = set()

    @classmethod
    def validate(cls):
        for var in cls._required:
            if var not in os.environ:
                raise ValueError(f"Missing required environment variable: {var}")

    @classmethod
    def get(cls, key, default=None):
        return os.environ.get(key, default)
    
    @staticmethod
    def load_env_file(file_path: str):
        try:
            with open(file_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
        except FileNotFoundError:  # TODO: logging instead of print
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"Ошибка при загрузке файла .env: {e}")
