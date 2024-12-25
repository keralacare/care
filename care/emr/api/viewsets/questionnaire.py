from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from pydantic import UUID4, BaseModel
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from care.emr.api.viewsets.base import EMRModelViewSet
from care.emr.models import Organization, Questionnaire, QuestionnaireOrganization
from care.emr.resources.organization.spec import OrganizationReadSpec
from care.emr.resources.questionnaire.spec import (
    QuestionnaireReadSpec,
    QuestionnaireSpec,
)
from care.emr.resources.questionnaire.utils import handle_response
from care.emr.resources.questionnaire_response.spec import (
    QuestionnaireResponseReadSpec,
    QuestionnaireSubmitRequest,
)
from care.security.authorization import AuthorizationController


class QuestionnaireFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    subject_type = filters.CharFilter(field_name="subject_type", lookup_expr="iexact")


class QuestionnaireViewSet(EMRModelViewSet):
    database_model = Questionnaire
    pydantic_model = QuestionnaireSpec
    pydantic_read_model = QuestionnaireReadSpec
    lookup_field = "slug"
    filterset_class = QuestionnaireFilter
    filter_backends = [filters.DjangoFilterBackend]

    def permissions_controller(self, request):
        if self.action in ["list", "retrieve", "get_organizations"]:
            return AuthorizationController.call("can_read_questionnaire", request.user)
        if self.action in ["create", "update", "set_organizations"]:
            return AuthorizationController.call("can_write_questionnaire", request.user)

        return request.user.is_authenticated

    def perform_create(self, instance):
        with transaction.atomic():
            super().perform_create(instance)
            for organization in instance._organizations:
                organization = get_object_or_404(Organization, external_id=organization)
                QuestionnaireOrganization.objects.create(
                    questionnaire=instance, organization=organization
                )

    def authorize_create(self, instance):
        for org in instance.organizations:
            # Validate if the user has write permission in the organization
            organization = get_object_or_404(Organization, external_id=org)
            if not AuthorizationController.call(
                "can_write_questionnaire", self.request.user, organization.id
            ):
                raise PermissionDenied("Permission Denied for Organization")


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = AuthorizationController.call("get_filtered_questionnaires" , queryset , self.request.user)
        if "search" in self.request.GET:
            queryset = queryset.filter(title__icontains=self.request.GET.get("search"))
        return queryset.select_related("created_by", "updated_by")

    @action(detail=True, methods=["POST"])
    def submit(self, request, *args, **kwargs):
        request_params = QuestionnaireSubmitRequest(**request.data)
        questionnaire = self.get_object()
        if not AuthorizationController.call(
            "can_submit_questionnaire_obj", request.user, questionnaire
        ):
            raise PermissionDenied("Permission Denied for Questionnaire")

        with transaction.atomic():
            response = handle_response(questionnaire, request_params, request.user)
        return Response(
            QuestionnaireResponseReadSpec.serialize(response).model_dump(mode="json")
        )

    @action(detail=True, methods=["GET"])
    def get_organizations(self, request, *args, **kwargs):
        """
        Get all External Organizations connected to this Questionnaire
        """
        # TODO : Switch to retrieve API of questionnaire
        questionnaire = self.get_object()
        questionnaire_organizations = QuestionnaireOrganization.objects.filter(
            questionnaire=questionnaire
        ).select_related("organization")
        organizations_serialized = [
            OrganizationReadSpec.serialize(obj.organization).to_json()
            for obj in questionnaire_organizations
        ]
        return Response(
            {
                "count": len(organizations_serialized),
                "results": organizations_serialized,
            }
        )

    class QuestionnaireOrganizationUpdateSchema(BaseModel):
        organizations: list[UUID4]

    @action(detail=True, methods=["POST"])
    def set_organizations(self, request, *args, **kwargs):
        """
        Bulk Update all External Organizations connected to this Questionnaire
        """
        questionnaire = self.get_object()
        request_params = self.QuestionnaireOrganizationUpdateSchema(**request.data)
        if not AuthorizationController.call(
            "can_write_questionnaire_obj", request.user, questionnaire
        ):
            raise PermissionDenied("Permission Denied for Questionnaire")
        with transaction.atomic():
            QuestionnaireOrganization.objects.filter(
                questionnaire=questionnaire
            ).delete()
            for org in request_params.organizations:
                # Validate if the user has write permission in the organization
                organization = get_object_or_404(Organization, external_id=org)
                if not AuthorizationController.call(
                    "can_write_questionnaire", request.user, organization.id
                ):
                    raise PermissionDenied("Permission Denied for Organization")
                QuestionnaireOrganization.objects.create(
                    questionnaire=questionnaire, organization=organization
                )
        organizations_serialized = [
            OrganizationReadSpec.serialize(obj.organization).to_json()
            for obj in QuestionnaireOrganization.objects.filter(
                questionnaire=questionnaire
            ).select_related("organization")
        ]
        return Response(
            {
                "count": len(organizations_serialized),
                "results": organizations_serialized,
            }
        )
