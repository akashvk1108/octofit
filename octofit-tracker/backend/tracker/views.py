from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import ActivitySerializer
from .mongo import activities_collection, serialize_activity


def object_id_or_none(value):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


class ActivityViewSet(viewsets.ViewSet):
    def list(self, request):
        activities = [serialize_activity(doc) for doc in activities_collection.find().sort('date', -1)]
        return Response(activities)

    def retrieve(self, request, pk=None):
        object_id = object_id_or_none(pk)
        if object_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        doc = activities_collection.find_one({'_id': object_id})
        if not doc:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialize_activity(doc))

    def create(self, request):
        serializer = ActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = activities_collection.insert_one({
            'user': data['user'],
            'title': data['title'],
            'description': data.get('description', ''),
            'duration_minutes': data['duration_minutes'],
            'date': str(data['date']),
        })
        created = activities_collection.find_one({'_id': result.inserted_id})
        return Response(serialize_activity(created), status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        object_id = object_id_or_none(pk)
        if object_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        updated = activities_collection.update_one(
            {'_id': object_id},
            {'$set': {
                'user': data['user'],
                'title': data['title'],
                'description': data.get('description', ''),
                'duration_minutes': data['duration_minutes'],
                'date': str(data['date']),
            }}
        )

        if updated.matched_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        updated_doc = activities_collection.find_one({'_id': object_id})
        return Response(serialize_activity(updated_doc))

    def destroy(self, request, pk=None):
        object_id = object_id_or_none(pk)
        if object_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        result = activities_collection.delete_one({'_id': object_id})
        if result.deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
