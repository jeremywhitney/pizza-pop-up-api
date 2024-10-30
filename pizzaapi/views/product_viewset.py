from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.product import Product
from ..serializers.product_serializer import ProductSerializer
import base64
from django.core.files.base import ContentFile
import uuid


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_available=True)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can create products"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Handle image data if it exists
        image_data = request.data.get("image_path")
        if image_data and ";base64," in image_data:
            # Extract and decode the base64 image
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]

            # Create a file from the base64 data
            data = ContentFile(
                base64.b64decode(imgstr), name=f"product-{uuid.uuid4()}.{ext}"
            )
            # Replace the base64 string with the file object
            request.data["image_path"] = data

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can update products"},
                status=status.HTTP_403_FORBIDDEN,
            )

        image_data = request.data.get("image_path")
        if image_data and ";base64," in image_data:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(
                base64.b64decode(imgstr), name=f"product-{uuid.uuid4()}.{ext}"
            )
            request.data["image_path"] = data

        # Check if we should remove the image
        if request.data.get("remove_image") == "true":
            instance = self.get_object()
            # Delete the actual file
            if instance.image_path:
                instance.image_path.delete(save=False)
            # Set the field to None
            instance.image_path = None
            instance.save()
            return Response(self.get_serializer(instance).data)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can delete products"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
