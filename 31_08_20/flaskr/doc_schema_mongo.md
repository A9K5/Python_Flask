# Mongoengine

## 2.3

### 2.3.1. Defining a document’s schema

```
from mongoengine import *
import datetime

class Page(Document):
    title = StringField(max_length=200, required=True)
    date_modifield = DateTimeField(default=datetime.datetime.utcnow)
```

### 2.3.2. Dynamic document schemas

```
from mongoengine import *

class Page(DynamicDocument):
    title = StringField(max_length=200, required=True)


page = Page('title':"Using MongoEngine")
page.tags = ['mongo','mongoengine']
page.save()
Page.objects(tags='manoengine').count()
```

#### Field Arguments 

- df_field
- required
- default

```
 class ExampleFirst(Document):
     # Default an empty list
    values = ListField(IntField(), default=list)

 class ExampleSecond(Document):
     # Default a set of values
     values = ListField(IntField(), default=lambda: [1,2,3])

 class ExampleDangerous(Document):
     # This can make an .append call to  add values to the default (and all the following objects),
     # instead to just an object
     values = ListField(IntField(), default=[1,2,3])
```


- choices

```
SIZE = (('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'))


 class Shirt(Document):
     size = StringField(max_length=3, choices=SIZE)
```

or

```
SIZE = ('S', 'M', 'L', 'XL', 'XXL')

class Shirt(Document):
    size = StringField(max_length=3, choices=SIZE)
```

- validation

```
def _not_empty(val):
    if not val:
        raise ValidationError('value can not be empty')

class Person(Document):
    name = StringField(validation=_not_empty)
```

#### List Fields

```
class Page(Document):
    tags = ListField(StringField(max_length=50))
```

#### Embedded Documents

```
class Comment(EmbeddedDocument):
    content = StringField()

class Page(Document):
    comments = ListField(EmbeddedDocumentField(Comment))

comment1 = Comment(content='Good work!')
comment2 = Comment(content='Nice article!')
page = Page(comments=[comment1, comment2])
```

#### Dictionary fields

```
class SurveyResponse(Document):
    date = DateTimeField()
    user = ReferenceField(User)
    answers = DictField()

survey_response = SurveyResponse(date=datetime.utcnow(), user=request.user)
response_form = ResponseForm(request.POST)
survey_response.answers = response_form.cleaned_data()
survey_response.save()
```

#### Refernce Fields

```
class User(Document):
    name = StringField()

class Page(Document):
    content = StringField()
    author = ReferenceField(User)

john = User(name="John Smith")
john.save()

post = Page(content="Test Page")
post.author = john
post.save()
```

or 

```
class Employee(Document):
    name = StringField()
    boss = ReferenceField('self')
    profile_page = ReferenceField('ProfilePage')

class ProfilePage(Document):
    content = StringField()
```
##### one to many list fields

```
class User(Document):
    name = StringField()

class Page(Document):
    content = StringField()
    authors = ListField(ReferenceField(User))

bob = User(name="Bob Jones").save()
john = User(name="John Smith").save()

Page(content="Test Page", authors=[bob, john]).save()
Page(content="Another Page", authors=[john]).save()

# Find all pages Bob authored
Page.objects(authors__in=[bob])

# Find all pages that both Bob and John have authored
Page.objects(authors__all=[bob, john])

# Remove Bob from the authors for a page.
Page.objects(id='...').update_one(pull__authors=bob)

# Add John to the authors for a page.
Page.objects(id='...').update_one(push__authors=john)
```

##### dealing with deletion of referred document

```
class ProfilePage(Document):
    ...
    employee = ReferenceField('Employee', reverse_delete_rule=mongoengine.CASCADE)
```

##### Generic Reference Field

```
class Link(Document):
    url = StringField()

class Post(Document):
    title = StringField()

class Bookmark(Document):
    bookmark_object = GenericReferenceField()

link = Link(url='http://hmarr.com/mongoengine/')
link.save()

post = Post(title='Using MongoEngine')
post.save()

Bookmark(bookmark_object=link).save()
Bookmark(bookmark_object=post).save()
```

##### Uniqueness Constraint

```
    username = StringField(unique=True)
    first_name = StringField()
    last_name = StringField(unique_with='first_name')
    # unique_with, which may be either a single field name, or a list or tuple of field names:
```

##### Skipping document verification on save

```
class Recipient(Document):
    name = StringField()
    email = EmailField()

recipient = Recipient(name='admin', email='root@localhost')
recipient.save()               # will raise a ValidationError while
recipient.save(validate=False) # won't
```

#### Document collection
Renaming the collection name.
```
class Page(Document):
    title = StringField(max_length=200, required=True)
    meta = {'collection': 'cmsPage'}
```

##### Capped Collection 
collections capped in size

```
class Log(Document):
    ip_address = StringField()
    meta = {'max_documents': 1000, 'max_size': 2000000}

```

#### Indexes 

To be done later....

#### Ordering

```
from datetime import datetime

class BlogPost(Document):
    title = StringField()
    published_date = DateTimeField()

    meta = {
        'ordering': ['-published_date']
    }

blog_post_1 = BlogPost(title="Blog Post #1")
blog_post_1.published_date = datetime(2010, 1, 5, 0, 0 ,0)

blog_post_2 = BlogPost(title="Blog Post #2")
blog_post_2.published_date = datetime(2010, 1, 6, 0, 0 ,0)

blog_post_3 = BlogPost(title="Blog Post #3")
blog_post_3.published_date = datetime(2010, 1, 7, 0, 0 ,0)

blog_post_1.save()
blog_post_2.save()
blog_post_3.save()

# get the "first" BlogPost using default ordering
# from BlogPost.meta.ordering
latest_post = BlogPost.objects.first()
assert latest_post.title == "Blog Post #3"

# override default ordering, order BlogPosts by "published_date"
first_post = BlogPost.objects.order_by("+published_date").first()
assert first_post.title == "Blog Post #1"
```

#### 2.3.7 Shard Keys

#### 2.3.8 Document inheritance

#### 2.3.9 Abstract Classes

---

### 2.5 Querying the database

Document classes have an objects attribute, which is used for accessing the objects in the database associated with the class. The objects attribute is actually a QuerySetManager, which creates and returns a new QuerySet object on access. The QuerySet object may be iterated over to fetch documents from the database:

```
# Prints out the names of all the users in the database
for user in User.objects:
    print user.name

```

<b>1. Filtering Queries</b>

```
# This will return a QuerySet that will only iterate over users whose
# 'country' field is set to 'uk'
uk_users = User.objects(country='uk')
```

<centre>or</centre>
Fields on embedded documents may also be referred to using field lookup syntax by using a double-underscore in place of the dot in object attribute access syntax:
```
# This will return a QuerySet that will only iterate over pages that have
# been written by a user whose 'country' field is set to 'uk'
uk_pages = Page.objects(author__country='uk')
```

<b>2. Query operators</b>

```
# Only find users whose age is 18 or less
young_users = Users.objects(age__lte=18)
```

Available operators are as follows:

- ne – not equal to
- lt – less than
- lte – less than or equal to
- gt – greater than
- gte – greater than or equal to
- not – negate a standard check, may be used before other operators (e.g. Q(age__not__mod=(5, 0)))
- in – value is in list (a list of values should be provided)
- nin – value is not in list (a list of values should be provided)
- mod – value % x == y, where x and y are two provided values
- all – every item in list of values provided is in array
- size – the size of the array is
- exists – value for field exists

1. String Queries
- exact – string field exactly matches value
- iexact – string field exactly matches value (case insensitive)
- contains – string field contains value
- icontains – string field contains value (case insensitive)
- startswith – string field starts with value
- istartswith – string field starts with value (case insensitive)
- endswith – string field ends with value
- iendswith – string field ends with value (case insensitive)
- match – performs an $elemMatch so you can match an entire document within an array

2. Geo queries
Left for later.

3. Querying lists

```
class Page(Document):
    tags = ListField(StringField())

# This will match all pages that have the word 'coding' as an item in the
# 'tags' list
Page.objects(tags='coding')
```

<centre>or</centre>

```
Page.objects(tags__0='db')
```
If you only want to fetch part of a list eg: you want to paginate a list, then the slice operator is required:

```
# comments - skip 5, limit 10
Page.objects.fields(slice__comments=[5, 10])
```

For updating documents, if you don’t know the position in a list, you can use the $ positional operator
```
Post.objects(comments__by="joe").update(**{'inc__comments__$__votes': 1})
```
<centre>or</centre>
```
Post.objects(comments__by="joe").update(inc__comments__S__votes=1)
```

4. Raw queries

```
Page.objects(__raw__={'tags': 'coding'})
```

<b>3. Sorting and ordering results</b>

```
# Order by ascending date
blogs = BlogPost.objects().order_by('date')    # equivalent to .order_by('+date')

# Order by ascending date first, then descending title
blogs = BlogPost.objects().order_by('+date', '-title')
```

<b> 4. Limiting and Skipping results</b>

```
# Only the first 5 people
users = User.objects[:5]

# All except for the first 5 people
users = User.objects[5:]

# 5 users, starting from the 11th user found
users = User.objects[10:15]
```

<b> 5. Default Document queries </b>
By default, the objects objects attribute on a document returns a QuerySet that doesn’t filter the collection – it returns all objects. This may be changed by defining a method on a document that modifies a queryset. The method should accept two arguments – doc_cls and queryset. The first argument is the Document class that the method is defined on (in this sense, the method is more like a classmethod() than a regular method), and the second argument is the initial queryset. The method needs to be decorated with queryset_manager() in order for it to be recognised.

```
class BlogPost(Document):
    title = StringField()
    date = DateTimeField()

    @queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('-date')
```

Over here you can also write your custom queries.

```
class BlogPost(Document):
    title = StringField()
    published = BooleanField()

    @queryset_manager
    def live_posts(doc_cls, queryset):
        return queryset.filter(published=True)

BlogPost(title='test1', published=False).save()
BlogPost(title='test2', published=True).save()
assert len(BlogPost.objects) == 2
assert len(BlogPost.live_posts()) == 1
```

<b> 6. Custom query set.</b>

```
class AwesomerQuerySet(QuerySet):

    def get_awesome(self):
        return self.filter(awesome=True)

class Page(Document):
    meta = {'queryset_class': AwesomerQuerySet}

# To call:
Page.objects.get_awesome()
```

<b>7. Aggregation </b>

```
num_users = User.objects.count()
yearly_expense = Employee.objects.sum('salary')
mean_age = User.objects.average('age')


class Article(Document):
    tag = ListField(StringField())

# After adding some tagged articles...
tag_freqs = Article.objects.item_frequencies('tag', normalize=True)

from operator import itemgetter
top_tags = sorted(tag_freqs.items(), key=itemgetter(1), reverse=True)[:10]
```

<b> 8. Query efficiency and performance </b>

####  Retrieving a subset of fields
```
>>> class Film(Document):
...     title = StringField()
...     year = IntField()
...     rating = IntField(default=3)
...
>>> Film(title='The Shawshank Redemption', year=1994, rating=5).save()
>>> f = Film.objects.only('title').first()
>>> f.title
'The Shawshank Redemption'
>>> f.year   # None
>>> f.rating # default value
3
```

#### Getting related Data

#### Turning off dereferencing

```
post = Post.objects.no_dereference().first()
assert(isinstance(post.author, DBRef))
```

<b> 9. Advanced Queries</b>

```
from mongoengine.queryset.visitor import Q

# Get published posts
Post.objects(Q(published=True) | Q(publish_date__lte=datetime.now()))

# Get top posts
Post.objects((Q(featured=True) & Q(hits__gte=1000)) | Q(hits__gte=5000))
```

<b> 10. Atomic updates</b>

