import copy

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from board.models import Post, Comment
from board.serializers import PostSerializer, CommentSerializer
from common.datetime import datetime_formatter
from common.paging import paging_data
from common.response import response_data
from user.models import User
from user.serializers import UserSerializer


class PostListAPIView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(True, serializer.data))
        else:
            return Response(response_data(False, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        qs = paging_data(Post.objects.all(), limit, page)
        post_serializer = PostSerializer(qs, many=True)
        posts = post_serializer.data

        for index, post in enumerate(posts):
            user = User.objects.get(pk=post['user'])
            user_serializer = UserSerializer(user)

            posts[index]['created_at'] = datetime_formatter(post['created_at'], '%Y-%m-%d %H:%M:%S')
            posts[index]['updated_at'] = datetime_formatter(post['updated_at'], '%Y-%m-%d %H:%M:%S')
            posts[index]['user'] = user_serializer.data
        return Response(response_data(True, posts))


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        post_serializer = PostSerializer(post)
        post_data = post_serializer.data

        user = User.objects.get(pk=post_data['user'])
        user_serializer = UserSerializer(user)

        post_data['created_at'] = datetime_formatter(post_data['created_at'], '%Y-%m-%d %H:%M:%S')
        post_data['updated_at'] = datetime_formatter(post_data['updated_at'], '%Y-%m-%d %H:%M:%S')
        post_data['user'] = user_serializer.data
        return Response(response_data(True, post_data))

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(True, serializer.data))
        else:
            return Response(response_data(False, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    def post(self, request, post_id):
        custom_request_data = copy.deepcopy(request.data)
        custom_request_data['post'] = post_id

        serializer = CommentSerializer(data=custom_request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(True, serializer.data))
        else:
            return Response(response_data(False, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        qs = Comment.objects.filter(post_id=post_id)
        comment_serializer = CommentSerializer(qs, many=True)
        comments = comment_serializer.data

        for index, comment in enumerate(comments):
            user = User.objects.get(pk=comment['user'])
            user_serializer = UserSerializer(user)

            comments[index]['created_at'] = datetime_formatter(comment['created_at'], '%Y-%m-%d %H:%M:%S')
            comments[index]['updated_at'] = datetime_formatter(comment['updated_at'], '%Y-%m-%d %H:%M:%S')
            comments[index]['user'] = user_serializer.data
        return Response(response_data(True, comments))


class CommentDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(response_data(True, serializer.data))

    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(True, serializer.data))
        else:
            return Response(response_data(False, serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(response_data(True), status=status.HTTP_204_NO_CONTENT)
