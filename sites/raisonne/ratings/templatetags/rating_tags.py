from django import template

register = template.Library()


def show_rating(context, object):
    rating = object.rating
    return {
            'rating_key': object.slug,
            'total_votes': rating.votes,
            'total_ratings': rating.total,
            'rating': rating.stars,
            'percent': rating.percent,
            'max_stars': rating.max_stars
            }
register.inclusion_tag("ratings/ratings.html", takes_context=True)(show_rating)
