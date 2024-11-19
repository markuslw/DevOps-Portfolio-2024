from platApp.models import Reaction

def calculate_sentiment(reaction_post):
    total_reactions_count = Reaction.objects.filter(post=reaction_post).count()
    if total_reactions_count != 0:
        total_likes = Reaction.objects.filter(post=reaction_post, type="like").count()
        total_dislikes = Reaction.objects.filter(post=reaction_post, type="dislike").count()
    
        sentiment = None
        # like / dislike ratio
        positive_ratio = total_likes / total_reactions_count
        if positive_ratio >= 0.75:
            sentiment = "very positive"
        elif positive_ratio > 0.55:
            sentiment = "mostly positive"
        elif 0.45 <= positive_ratio <= 0.55:
            sentiment = "mixed reactions"
        elif positive_ratio < 0.45 and positive_ratio >= 0.25:
            sentiment = "mostly negative"
        else:
            sentiment = "very negative"
        return sentiment
    else:
        return "no reactions"
