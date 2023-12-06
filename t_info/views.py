from django.shortcuts import render
from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
import logging
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .utils import success_response,failure_response
from django.http import JsonResponse


logger = logging.getLogger("t_info.views")


# Create your views here.

class StandardResultSetPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'p'
    max_page_size = 100


class TeacherModelViewSet(viewsets.ModelViewSet, GenericAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = StandardResultSetPagination
    ordering_fields = ['id','teacher_name', 'teacher_language', 'teacher_city']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['teacher_name', 'teacher_city', 'teacher_language']
    search_fields = ['teacher_name', 'teacher_language', 'teacher_description', 'teacher_contact', 'teacher_email', 'teacher_residence', 'teacher_city']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # Perform additional filtering based on query parameters
            # For example, you can filter based on a request parameter named 'active'
            active_filter = request.query_params.get('active')
            if active_filter:
                queryset = queryset.filter(active=active_filter)

            # Perform ordering based on request parameter 'ordering'
            ordering = request.query_params.get('ordering')
            if ordering in self.ordering_fields:
                queryset = queryset.order_by(ordering)

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info('Data listed successfully')
                return self.get_paginated_response(
                    success_response(message='Data retrieved successfully', data=serializer.data))

            serializer = self.get_serializer(queryset, many=True)
            logger.info('Data listed successfully')
            return Response(success_response(message='Data retrieved successfully', data=serializer.data))
        except Exception as e:
            logger.error(f"An error occurred during listing: {e}")
            return Response(failure_response(message='Failed to retrieve data', data={'error': str(e)}))


    # def list(self, request, *args, **kwargs):
    #     try:
    #         queryset = self.filter_queryset(self.get_queryset())
    #         serializer = self.get_serializer(queryset, many=True)
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             # serializer = self.get_serializer(page, many=True)
    #             logger.info('Data listed successfully')
    #             return Response(success_response(message='Data retrieved successfully', data=serializer.data))
    #     except Exception as e:
    #         logger.error(f"An error occurred during listing: {e}")  # Log error message
    #         return Response(failure_response(message='Failed to retrieve Data', data={'error': str(e)}),
    #                             status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info('Data created successfully')  # Log info message
            return Response(success_response(message='Data created successfully', data={"Success":serializer.data},))
        except Exception as e:
            logger.error(f"An error occurred during creation: {e}")  # Log error message
            return Response(failure_response(message='Failed to create Data', data={'error': str(e)}),
                                status=400)


    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info('Data updated successfully')  # Log info message
            return Response(success_response(message='Data updated successfully',data={serializer.data}))
        except Exception as e:
            logger.error(f"An error occurred during update: {e}")  # Log error message
            return Response(failure_response(message='Failed to update Data', data={'error': str(e)}),
                                status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info('Data deleted successfully')  # Log info message
            return Response(success_response(message='Data deleted successfully'))
        except Exception as e:
            logger.error(f"An error occurred during deletion: {e}")  # Log error message
            return Response(failure_response(message='Failed to delete Data', data={'error': str(e)}),
                                status=400)