# coding=utf-8
from django import template
from ..models import News, Portfolio

register = template.Library()


@register.inclusion_tag('content/block_news_list.html')
def latest_news(count):
    news_list = News.objects.active()[:count]
    return dict(news_list=news_list)


@register.inclusion_tag('content/block_portfolio_list.html')
def latest_portfolio(count):
    portfolio_list = Portfolio.objects.active()[:count]
    return dict(portfolio_list=portfolio_list)
