from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer_aaa(serializers.Serializer): # an old serializer class
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'}) # equivalent to widget=widgets.Textarea on Forms
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class SnippetSerializer_bbb(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # or CharField(read_only=True)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']


###########################################################################################################


from django.contrib.auth.models import User

class UserSerializer_bbb(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    # Because 'snippets' is a `reverse` relationship on the User model, it will not be included by default, so we needed to add an explicit field for it.

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


######################################## Hyperlinked Serializers ############################################


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html') # url też ma taki typ pola

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style'] # + url, highlight

# 'url' field by default will refer to '{model_name}-detail', which in this case will be 'snippet-detail' and 'user-detail'.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
