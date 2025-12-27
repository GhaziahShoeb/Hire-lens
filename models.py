from pydantic import BaseModel, Field
from typing import List

class JobSkills(BaseModel):
    title: str = Field(description="The job title")
    skills: List[str] = Field(description="A list of technical hard skills only (e.g. Python, AWS, Docker)")
    experience_level: str = Field(description="Junior, Mid, Senior, or Lead")
    reasoning: str = Field(description="A brief explanation of why you chose this experience level")