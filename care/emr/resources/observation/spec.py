from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel, Field

from care.emr.fhir.schema.base import CodeableConcept
from care.emr.models.observation import Observation
from care.emr.resources.base import EMRResource
from care.emr.resources.observation.valueset import (
    CARE_BODY_SITE_VALUESET,
    CARE_OBSERVATION_COLLECTION_METHOD,
)
from care.emr.resources.questionnaire.spec import SubjectType


class ObservationStatus(str, Enum):
    final = "final"
    amended = "amended"


class PerformerType(str, Enum):
    related_person = "related_person"
    user = "user"


class Coding(BaseModel):
    system: str
    code: str
    text: str | None = None


class Performer(BaseModel):
    type: PerformerType
    id: str


class ReferenceRange(BaseModel):
    low: float | None = None
    high: float | None = None
    unit: str | None = None
    text: str | None = None


class ObservationSpec(EMRResource):
    __model__ = Observation

    id: str = Field("", description="Unique ID in the system")

    status: ObservationStatus = Field(
        description="Status of the observation (final or amended)"
    )

    category: Coding | None = Field(
        None, description="List of codeable concepts derived from the questionnaire"
    )

    main_code: Coding | None = Field(
        None, description="Code for the observation (LOINC binding)"
    )

    alternate_coding: CodeableConcept = dict

    subject_type: SubjectType

    encounter: UUID4 | None = None

    effective_datetime: datetime = Field(
        ...,
        description="Datetime when observation was recorded",
    )

    data_entered_by_id: int

    performer: Performer | None = Field(
        None,
        description="Who performed the observation (currently supports RelatedPerson)",
    )  # If none the observation is captured by the data entering person

    value: str | None = Field(
        None,
        description="Value of the observation if not code. For codes, contains display text",
    )

    value_code: Coding | None = Field(
        None, description="Value as code part of a system"
    )

    note: str | None = Field(None, description="Additional notes about the observation")

    body_site: Coding | None = Field(
        None,
        description="Body site where observation was made",
        json_schema_extra={"slug": CARE_BODY_SITE_VALUESET.slug},
    )

    method: Coding | None = Field(
        None,
        description="Method used for the observation",
        json_schema_extra={"slug": CARE_OBSERVATION_COLLECTION_METHOD.slug},
    )

    reference_range: list[ReferenceRange] = Field(
        [], description="Reference ranges for interpretation"
    )

    interpretation: str | None = Field(
        None, description="Interpretation based on the reference range"
    )

    parent: UUID4 | None = Field(None, description="ID reference to parent observation")

    questionnaire_response: UUID4 | None = None

    def perform_extra_deserialization(self, is_update, obj):
        obj.external_id = self.id
        obj.data_entered_by_id = self.data_entered_by_id
        self.meta.pop("data_entered_by_id", None)
        if not is_update:
            obj.id = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["id"] = obj.external_id
        # Avoiding extra queries
        mapping["encounter"] = None
        mapping["patient"] = None
        mapping["questionnaire_response"] = None
