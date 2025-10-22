import os
from sentient_agent_framework.implementation.default_server import DefaultServer
from agent.agent import Agent
from fastapi.middleware.cors import CORSMiddleware

class CorsDefaultServer(DefaultServer):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        
        origins = self.parse_list_env("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
        methods = self.parse_list_env("CORS_METHODS", "GET,POST,OPTIONS")
        headers = self.parse_list_env("CORS_HEADERS", "Content-Type")
        credentials_env = os.getenv("CORS_CREDENTIALS", "True")
        credentials = credentials_env.lower() == 'true'

        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=credentials,
            allow_methods=methods,
            allow_headers=headers,
        )

    @staticmethod
    def parse_list_env(env_var_name, default_value):
        value_str = os.getenv(env_var_name, default_value)
        return [item.strip() for item in value_str.split(',') if item.strip()]

if __name__ == "__main__":
    server = CorsDefaultServer(Agent())
    server.run(host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")))
