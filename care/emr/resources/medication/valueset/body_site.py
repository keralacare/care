from care.emr.fhir.schema.valueset.valueset import ValueSetCompose, ValueSetInclude
from care.emr.registries.care_valueset.care_valueset import CareValueset
from care.emr.resources.valueset.spec import ValueSetStatusOptions

CARE_BODY_SITE_VALUESET = CareValueset(
    "Disease", "system-body-site", ValueSetStatusOptions.active.value
)

CARE_BODY_SITE_VALUESET.register_valueset(
    ValueSetCompose(
        include=[
            ValueSetInclude(
                system="http://snomed.info/sct",
                filter=[{"property": "concept", "op": "is-a", "value": "91723000"}],
            ),
        ]
    )
)

CARE_BODY_SITE_VALUESET.register_as_system()
