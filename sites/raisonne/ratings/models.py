# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from picassoft.utils.validators import validate_bounds

def calc_rating(score, votes):
    return 1.0 * score / votes if votes>0 else 0.0


class RatedModel(models.Model):
    rating_votes = models.PositiveIntegerField(_("Total rating votes"), default=0)
    rating_score = models.FloatField(_("Total rating score"), default=0.0) # Each vote increases score by (0.0, 1.0], so score <= votes.
    rating_value = models.FloatField(_("Actual rating value"), default=1.0) # Falls in (0.0; 1.0]. Recalculated automatically on save.

    max_stars = 5

    class Meta:
        abstract = True

    @property
    def percent(self):
        return int(self.rating_value * 100)

    @property
    def stars(self):
        return round(self.rating_value * self.max_stars, 1)

    def save(self, *args, **kwargs):
        self.rating_value = calc_rating(self.rating_score, self.rating_votes)
        super(RatedModel, self).save(*args, **kwargs)

    def vote(self, vote=None):
        if vote is None:
            # Default vote is maximum vote
            self.rating_score += 1.0
        else:
            validate_bounds(u"Vote", vote, 0, self.max_stars)
            # Normalize stored value during saving to DB, due to this fact later we would be able
            # to change max_stars without necessity to recalculate votes.
            self.rating_score += 1.0 * vote / self.max_stars
        self.rating_votes += 1
        self.save()
        return self
