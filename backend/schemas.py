from pydantic import BaseModel


class RecipeGenerationRequest(BaseModel):
    products: list[str]
    preference: str
    custom_request: str = ""