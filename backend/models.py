from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, computed_field


class UnitCreate(BaseModel):
    phrase: str
    translation: Optional[str] = None
    unit_type: str
    difficulty: int = Field(1, ge=1, le=5)
    language_from: str
    language_to: str
    tags: List[str] = []


class Unit(UnitCreate):
    id: str = Field(default_factory=lambda: str(uuid4()))


class Combination(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    translation: Optional[str] = None
    unit_ids: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExerciseOption(BaseModel):
    label: str
    value: str


class Exercise(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    prompt: str
    answer: str
    options: List[ExerciseOption] = []
    combination_id: Optional[str] = None


class Progress(BaseModel):
    user_id: str
    unit_id: str
    proficiency: int = 0
    attempts: int = 0
    successes: int = 0
    next_review_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: Optional[datetime] = None

    def mark_result(self, success: bool) -> None:
        self.attempts += 1
        if success:
            self.successes += 1

        change = 1 if success else -1
        self.proficiency = max(0, min(5, self.proficiency + change))
        now = datetime.utcnow()
        self.last_seen = now

        mastery = self.mastery_score
        if mastery >= 0.8:
            interval_hours = 72
        elif mastery < 0.6:
            interval_hours = 4
        else:
            interval_hours = 12
        # Encourage extra delay when proficiency is high
        interval_hours += self.proficiency
        self.next_review_at = now + timedelta(hours=interval_hours)

    @computed_field
    @property
    def accuracy(self) -> float:
        if self.attempts == 0:
            return 0.0
        return round((self.successes / self.attempts) * 100, 1)

    @computed_field
    @property
    def mastery_score(self) -> float:
        if self.attempts == 0:
            return 0.0
        return round(self.successes / self.attempts, 2)

    @computed_field
    @property
    def status(self) -> str:
        if self.mastery_score >= 0.8:
            return "mastered"
        if self.mastery_score < 0.6:
            return "weak"
        if self.last_seen and datetime.utcnow() - self.last_seen > timedelta(hours=72):
            return "review"
        return "learning"


class AnalyticsEvent(BaseModel):
    name: str
    user_id: Optional[str] = None
    unit_id: Optional[str] = None
    exercise_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, str] = Field(default_factory=dict)


class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    email: Optional[str] = None
    streak: int = 0
    last_active: Optional[datetime] = None


class RegisterPayload(BaseModel):
    name: str
    email: str
    password: str


class LoginPayload(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user: User


class State(BaseModel):
    users: Dict[str, User] = Field(default_factory=dict)
    units: Dict[str, Unit] = Field(default_factory=dict)
    combinations: Dict[str, Combination] = Field(default_factory=dict)
    exercises: Dict[str, Exercise] = Field(default_factory=dict)
    progress: Dict[str, Progress] = Field(default_factory=dict)
    analytics: List[AnalyticsEvent] = Field(default_factory=list)
    credentials: Dict[str, str] = Field(default_factory=dict)
    sessions: Dict[str, str] = Field(default_factory=dict)
    account_index: Dict[str, str] = Field(default_factory=dict)
