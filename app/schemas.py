from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

SlideType = Literal[
    "title",
    "agenda",
    "section",
    "bullets",
    "comparison",
    "quote",
    "conclusion",
]


class SlidePlan(BaseModel):
    type: SlideType
    title: str
    subtitle: str | None = None

    bullets: list[str] = Field(default_factory=list)

    left_title: str | None = None
    left_bullets: list[str] = Field(default_factory=list)

    right_title: str | None = None
    right_bullets: list[str] = Field(default_factory=list)

    speaker_notes: str

    @field_validator("title", "speaker_notes")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_by_type(self) -> SlidePlan:
        if self.type in {"bullets", "agenda", "conclusion"} and not self.bullets:
            raise ValueError(f"slide type '{self.type}' requires bullets")
        if self.type == "comparison":
            if not self.left_title or not self.left_bullets:
                raise ValueError("comparison slide requires left_title and left_bullets")
            if not self.right_title or not self.right_bullets:
                raise ValueError("comparison slide requires right_title and right_bullets")
        return self


class PresentationPlan(BaseModel):
    title: str
    subtitle: str | None = None
    audience: str
    objective: str
    slides: list[SlidePlan]

    @field_validator("title", "audience", "objective")
    @classmethod
    def root_fields_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field cannot be empty")
        return value

    @field_validator("slides")
    @classmethod
    def at_least_one_slide(cls, slides: list[SlidePlan]) -> list[SlidePlan]:
        if len(slides) < 1:
            raise ValueError("presentation must have at least one slide")
        return slides
