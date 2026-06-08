from pydantic import BaseModel

class RecipeRequest(BaseModel):
    preference: str