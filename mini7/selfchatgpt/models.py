from django.db import models


class QueryLog(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False)
    datetime = models.DateTimeField(null=False)
    query = models.TextField(null=False)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"QueryLog {self.id} by {self.username}"


class Topic(models.Model):
    qa_id = models.ForeignKey(QueryLog, on_delete=models.CASCADE, db_column='qa_id')
    user_name = models.CharField(max_length=255, null=True)
    topic_id = models.CharField(max_length=100, null=False)
    title = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.topic_id


class ChromaDB(models.Model):
    category = models.CharField(max_length=256)
    QA = models.CharField(max_length=256)
    # due_date = models.DateTimeField()
    # is_complete = models.BooleanField(default=False)
