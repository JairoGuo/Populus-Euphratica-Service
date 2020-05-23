
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from sonsuz_website.ImageHosting.api.serializers import ImageSerializer
from sonsuz_website.ImageHosting.models import Image


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def create(self, request, *args, **kwargs):

        # if request.data  == {}:
        #     return Response(data={"data": "null"})
        self.serializer_class = ImageSerializer
        rlt_data =[]
        for i in request.data:

            data = {
                "image": request.data[i],
            }
            serializer = ImageSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            rlt_data.append([eval(i), 'http://localhost:8000' + serializer.data['image']])

        return Response({'imgs': rlt_data})
        # return Response(serial.data)
        # return Response({'code': '200', 'message': 'OK'})



