from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    llm_api_key: str
    llm_api_url: str
    llm_option: str
    kavak_url: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_whatsapp_number: str

settings = AppSettings()
