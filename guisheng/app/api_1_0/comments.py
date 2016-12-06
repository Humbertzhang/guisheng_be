# coding: utf-8
import ast
from flask import render_template,jsonify,Response,g,request
import json
from ..models import Role,User,News,Picture,Article,Interaction,Everydaypic,\
        Collect,Like,Light,Comment
from . import api


@api.route('/comments/',methods=['GET','POST'])
def get_comments():
    kind = request.args.get('kind')
    a_id = request.args.get('article_id')
    post = {1: News, 2: Picture, 3: Article, 4: Interaction}.get(kind).query.get_or_404(a_id)
    _ids = {1: "news_id", 2: "picture_id", 3: "article_id", 4: "interaction_id" }.get(kind)
    c_id = ast.literal_eval(_ids)
    comments = Comment.query.filter_by(c_id=a_id).order_by(Comment.time.asc()).all()
    responses = Comment.query.filter_by(c_id=a_id).order_by(Comment.time.asc()).all()
    return Response(json.dumps([{
            "article_id":a_id,
            "img_url":(User.query.get_or_404(comment.author_id)).img_url,
            "message":comment.body,
            "comments":[{
                "article_id":a_id,
                "img_url":(User.query.get_or_404(response.author_id)).img_url,
                "message":response.body,
               "likes":response.like.count(),
                }for response in responses],
            "likes":comment.like.count(),
        } for comment in comments]
    ),mimetype='application/json')

@api.route('/comments/',methods=['GET','POST'])
def create_comments():
    if request.method == 'POST':
        comment = Comment()
        kind = request.get_json().get("kind")
        if kind == 1:
            comment.news_id = request.get_json().get("article_id")
        if kind == 2:
            comment.picture_id = request.get_json.get("article_id")
        if kind == 3:
            comment.article_id = request.get_json.get("article_id")
        if kind == 4:
            comment.interaction_id = request.get_json.get("article_id")
        comment.comment_id = request.get_json().get("comment_id")
        comment.body = request.get_json().get("message")
        comment.author_id = request.get_json().get("user_id")
        db.session.add(comment)
        db.session.commit()
        return Response(json.dumps({
            "status":"200",
            }),mimetype='application/json')

@api.route('/comments/<int:id>/like/')
def get_comment_likes(id):
    comment = Comment.query.get_or_404(id)
    likes = comment.like.count()
    return Response(json.dumps({
        "likes":likes,
        }),mimetype='application/json')


