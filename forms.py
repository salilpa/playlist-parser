from flask_wtf import Form
from wtforms import ValidationError, SubmitField, IntegerField, SelectField, TextField, BooleanField
from wtforms.validators import Required


class InsertForm(Form):
    name = TextField('name', description='unique name for station', validators=[Required(message='name is required')])
    display_name = TextField('display name', description='display name',
                             validators=[Required(message='display name is required')])
    url = TextField('url', description='url of station', validators=[Required(message='url is required')])
    parser = TextField('parser', description='parser', validators=[Required(message='parser is required')],
                       default='html5lib')
    user_agent = TextField('user agent', description='user agent',
                           validators=[Required(message='user agent is required')],
                           default="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0")
    list_tag = TextField('list tag', description='list tag', validators=[Required(message='required')],
                         default="article")
    list_attr_key = TextField('list attr key', description='list attr key', validators=[Required(message='required')],
                         default="class")
    list_attr_val = TextField('list attr val', description='list attr val', default="song_review")
    keyword_tag_1 = TextField('keyword tag 1', description='keyword tag 1', validators=[Required(message='required')],
                         default="span")
    keyword_attr_key_1 = TextField('keyword attr key 1', description='keyword attr key 1', validators=[Required(message='required')],
                         default="class")
    keyword_attr_val_1 = TextField('keyword attr val 1', description='keyword attr val 1', default="or12")
    keyword_tag_2 = TextField('keyword tag 2', description='keyword tag 2', default="span")
    keyword_attr_key_2 = TextField('keyword attr key 2', description='keyword attr key 2', default="class")
    keyword_attr_val_2 = TextField('keyword attr val 2', description='keyword attr val 2', default="moviename")
    country = TextField('country', description='country', validators=[Required(message='required')])
    language = TextField('language', description='language', validators=[Required(message='required')])
    insert_val = BooleanField('insert')
    test_button = SubmitField('test')