import csv
import io

from customers import serializers, gems_utils
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

User = get_user_model()


class CustomerViewSet(mixins.ListModelMixin, viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.DealsUploadSerializer

    def list(self, request: dict, *args, **kwargs) -> Response:
        queryset = (
            User.objects.annotate(
                spent_money=Sum("customer__total"), count=Count("customer")
            )
            .order_by("-spent_money")
            .exclude(count=0)[:5]
        )
        gems = gems_utils.Gems(queryset)
        serializer = serializers.GemsSerializer(gems.result())
        del queryset
        return Response(serializer.data)

    def post(self, request: dict) -> Response:
        file_serializer = self.serializer_class(data=request.data)
        file_serializer.is_valid(raise_exception=True)
        uploaded_file = file_serializer.validated_data["deals"]

        decoded_file = uploaded_file.read().decode()
        io_string = io.StringIO(decoded_file)

        items = [item for item in csv.DictReader(io_string)]
        for item in items:
            self.create_user(item)

        customer_items = serializers.CustomerSerializer(data=items, many=True)
        if customer_items.is_valid():
            customer_items.save()
            result = Response(
                "OK - файл был обработан без ошибок", status=status.HTTP_200_OK
            )
        else:
            result = Response(
                f"Error, Desc: {customer_items.errors[0]}  - в процессе обработки файла произошла ошибка.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return result

    @staticmethod
    def create_user(item: dict) -> None:
        customer = item.get("customer")
        User.objects.get_or_create(username=customer)
