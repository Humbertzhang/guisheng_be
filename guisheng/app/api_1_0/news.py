# coding: utf-8
from flask import render_template,jsonify,Response,g,request
import json
from ..models import Role,User,News
from . import api


@api.route('/news/<int:id>/', methods=['GET'])
def get_news(id):
    news = News.query.get_or_404(id)
    return Response(json.dumps({
        "title":news.title,
        "author":User.query.get_or_404(news.author_id).name,
        "time":news.time.strftime('%m/%d/%Y'),
        "body":news.body,
        }),mimetype='application/json')

@api.route('/news/', methods=['GET','POST'])
def command_news():
    n_id = request.get_json().get('article_id',type=int)
    news_tag = PostTag.query.filter_by(news_id=n_id).first()
    tag_id = news_tag.tag_id
    tag_news = News.query.filter_by(tag_id=tag_id).order_by(News.views.desc()).all()
    command_news = []
    for n in all_news:
        if n.tag[0]==news_tag:
            command_news.append(n)
    return Response(json.dumps([{
            "title":news.title,
            "description":news.description,
            "author":User.query.get_or_404(news.author_id).name,
            "tag":news.tag[0],
            "views":news.views
        }for news in command_news]
    ),mimetype='application/json')


