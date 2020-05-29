from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CustomCreateModelMixin(GenericViewSet, mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CustomListModelMixin(GenericViewSet, mixins.ListModelMixin):

    allowed_filters = []

    def get_queryset(self):
        filters = {
            key: self.request.query_params.get(key)
            for key
            in self.allowed_filters
            if self.request.query_params.get(key)
        }
        return super().get_queryset().filter(**filters)


class CustomCreateRetrieveListViewSet(CustomCreateModelMixin,
                                      CustomListModelMixin,
                                      mixins.RetrieveModelMixin):
    pass


class CustomModelViewSet(CustomCreateModelMixin,
                         CustomListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    pass
