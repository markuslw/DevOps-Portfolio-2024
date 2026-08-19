from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import generics
from .models import Post
from .serializer import PostSerializer

class AdvancedPostSearchView(generics.ListAPIView):
    """
    Provides a list API view that supports searching posts by their title and content.
    Utilizes Django's PostgreSQL full-text search capabilities to allow for advanced
    search queries, ranking results based on relevance to the search term provided
    by the user.

    Attributes:
        serializer_class (PostSerializer): Specifies the serializer class for the queryset.
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        """
        Overrides the default queryset to perform a full-text search on the Post model.
        The search considers both the title and content of the posts, with titles having
        a higher weight in the search ranking.

        Returns:
            QuerySet: A queryset of Post objects ranked by relevance to the search query.
                      Returns an empty queryset if no search query is provided.
        """
        query = self.request.query_params.get('query')
        if query:
            # Define the search vectors with weights, prioritizing title over content.
            search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
            search_query = SearchQuery(query)

            # Annotate the Post objects with a 'rank' attribute based on their search relevance
            # and filter the results to include only those with a rank above a certain threshold.
            return Post.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')  # Rank threshold and ordering

        # If no search query is provided, return an empty queryset to signify no results.
        return Post.objects.none()
