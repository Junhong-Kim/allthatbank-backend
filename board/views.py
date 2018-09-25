import copy
import math

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from board.models import Post, Comment, PostLike, CommentLike
from board.serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
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
        limit = int(request.query_params.get('limit', 10))
        now_page = int(request.query_params.get('page', 1))
        max_page = math.ceil(len(Post.objects.all()) / limit)

        post_qs = paging_data(Post.objects.all()[::-1], limit, now_page)
        post_serializer = PostSerializer(post_qs, many=True)
        posts = post_serializer.data

        for index, post in enumerate(posts):
            user = User.objects.get(pk=post['user'])
            user_serializer = UserSerializer(user)
            comment_count = Comment.objects.filter(post_id=post['id']).count()

            posts[index]['created_at'] = datetime_formatter(post['created_at'], '%Y-%m-%d %H:%M:%S')
            posts[index]['updated_at'] = datetime_formatter(post['updated_at'], '%Y-%m-%d %H:%M:%S')
            posts[index]['user'] = user_serializer.data
            posts[index]['comment_count'] = comment_count
        return Response(response_data(True, posts, now_page, max_page))


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        self.view_post(post)
        post_serializer = PostSerializer(post)
        post_data = post_serializer.data

        user = User.objects.get(pk=post_data['user'])
        user_serializer = UserSerializer(user)
        comment_count = Comment.objects.filter(post_id=post_data['id']).count()

        post_data['created_at'] = datetime_formatter(post_data['created_at'], '%Y-%m-%d %H:%M:%S')
        post_data['updated_at'] = datetime_formatter(post_data['updated_at'], '%Y-%m-%d %H:%M:%S')
        post_data['user'] = user_serializer.data
        post_data['comment_count'] = comment_count
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

    def view_post(self, post):
        views = post.views + 1
        post_serializer = PostSerializer(post, data={'views': views}, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()


class PostLikeListAPIView(APIView):
    def post(self, request, post_id):
        user_id = int(request.query_params['user_id'])
        serializer = PostLikeSerializer(data={
            'post': post_id,
            'user': user_id
        })
        if serializer.is_valid():
            serializer.save()
            self.like_post(post_id)
            return Response(response_data(True, serializer.data))
        else:
            PostLike.objects.get(post_id=post_id, user_id=user_id).delete()
            self.unlike_post(post_id)
            return Response(response_data(True), status=status.HTTP_204_NO_CONTENT)

    def get(self, request, post_id):
        qs = PostLike.objects.filter(post_id=post_id)
        serializer = PostLikeSerializer(qs, many=True)
        return Response(response_data(True, serializer.data))

    def like_post(self, pk):
        post = PostDetailAPIView().get_object(pk)
        like = post.like + 1
        post_serializer = PostSerializer(post, data={'like': like}, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()

    def unlike_post(self, pk):
        post = PostDetailAPIView().get_object(pk)
        like = post.like - 1
        post_serializer = PostSerializer(post, data={'like': like}, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()


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


class CommentLikeListAPIView(APIView):
    def post(self, request, comment_id):
        user_id = int(request.query_params['user_id'])
        serializer = CommentLikeSerializer(data={
            'comment': comment_id,
            'user': user_id
        })
        if serializer.is_valid():
            serializer.save()
            self.like_comment(comment_id)
            return Response(response_data(True, serializer.data))
        else:
            CommentLike.objects.get(comment_id=comment_id, user_id=user_id).delete()
            self.unlike_comment(comment_id)
            return Response(response_data(True), status=status.HTTP_204_NO_CONTENT)

    def get(self, request, comment_id):
        qs = CommentLike.objects.filter(comment_id=comment_id)
        serializer = CommentLikeSerializer(qs, many=True)
        return Response(response_data(True, serializer.data))

    def like_comment(self, pk):
        comment = CommentDetailAPIView().get_object(pk)
        like = comment.like + 1
        comment_serializer = CommentSerializer(comment, data={'like': like}, partial=True)
        if comment_serializer.is_valid():
            comment_serializer.save()

    def unlike_comment(self, pk):
        comment = CommentDetailAPIView().get_object(pk)
        like = comment.like - 1
        comment_serializer = CommentSerializer(comment, data={'like': like}, partial=True)
        if comment_serializer.is_valid():
            comment_serializer.save()


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
