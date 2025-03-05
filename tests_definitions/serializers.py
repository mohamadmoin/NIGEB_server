from django.conf import settings
from rest_framework import serializers

from accounts import models
from .models import TestInfo, FavoriteTestGroup

class TestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestInfo
        fields = '__all__'


# class FavoriteTestGroupSerializer(serializers.ModelSerializer):
#     # you can nest the LabTestSerializer if you wish, or just store IDs
#     test_ids = serializers.PrimaryKeyRelatedField(
#         source='tests', 
#         many=True, 
#         queryset=TestInfo.objects.all(),
#         required=False
#     )

#     class Meta:
#         model = FavoriteTestGroup
#         fields = ['id', 'group_name', 'description', 'test_ids']

#     def create(self, validated_data):
#         tests = validated_data.pop('tests', [])
#         group = FavoriteTestGroup.objects.create(**validated_data)
#         group.tests.set(tests)
#         return group
# class FavoriteTestGroupSerializer(serializers.ModelSerializer):
#     tests = serializers.PrimaryKeyRelatedField(
#         many=True, 
#         queryset=TestInfo.objects.all(),
#         required=False
#     )

#     class Meta:
#         model = FavoriteTestGroup
#         fields = ['id', 'group_name', 'description', 'tests']

#     def create(self, validated_data):
#         # now "tests" is correct
#         tests = validated_data.pop('tests', [])
#         group = FavoriteTestGroup.objects.create(**validated_data)
#         group.tests.set(tests)
#         return group

#     def update(self, instance, validated_data):
#         tests = validated_data.pop('tests', None)
#         instance.group_name = validated_data.get('group_name', instance.group_name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         if tests is not None:
#             instance.tests.set(tests)
#         return instance

# class FavoriteTestGroup(models.Model):
#     """
#     Allows each user to create multiple "favorite test groups."
#     E.g., "My Routine Panel," "Pediatrics Panel," etc.
#     """
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='favorite_test_groups'
#     )
#     group_name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)

#     # Many-to-many relationship to the TestInfo model
#     tests = models.ManyToManyField(TestInfo, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'group_name')
#         ordering = ['group_name']

#     def __str__(self):
#         return f"{self.group_name} ({self.user.username})"


class FavoriteTestGroupSerializer(serializers.ModelSerializer):
    # When reading, you'll see a list of fully expanded TestInfo objects
    tests = TestInfoSerializer(many=True, read_only=True)

    # When writing (create/update), you send test IDs here
    test_ids = serializers.PrimaryKeyRelatedField(
        source='tests', 
        many=True, 
        queryset=TestInfo.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = FavoriteTestGroup
        # We expose both 'tests' (read-only) and 'test_ids' (write-only)
        fields = ['id', 'group_name', 'description', 'tests', 'test_ids']

    def create(self, validated_data):
        # 'tests' here is populated by 'test_ids' because source='tests'
        tests = validated_data.pop('tests', [])
        group = FavoriteTestGroup.objects.create(**validated_data)
        group.tests.set(tests)
        return group

    def update(self, instance, validated_data):
        tests = validated_data.pop('tests', None)
        instance.group_name = validated_data.get('group_name', instance.group_name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        if tests is not None:
            instance.tests.set(tests)
        return instance