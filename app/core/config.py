from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Proje Ayarları
    PROJECT_NAME: str = "Receiptly"
    API_V1_STR: str = "/api/v1"

    # Veritabanı Değişkenleri
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # Güvenlik
    SECRET_KEY: str

    # PostgreSQL Asenkron Bağlantı Dizesini (Connection String) Otomatik Oluşturma
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Pydantic'e .env dosyasını nereden okuyacağını söylüyoruz
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Proje genelinde tek bir ayar nesnesi kullanmak için örneklendik (Instantiate)
settings = Settings()