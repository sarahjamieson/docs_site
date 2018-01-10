from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'docs'
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Chemistry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_id = models.ForeignKey(Category)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'docs'
        db_table = 'Chemistry'
        verbose_name = 'Chemistry'
        verbose_name_plural = 'Chemistries'


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chemistry_id = models.ForeignKey(Chemistry)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'docs'
        db_table = 'Test'
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'


class DocumentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        app_label = 'docs'
        db_table = 'DocumentType'
        verbose_name = 'Document Type'
        verbose_name_plural = 'Document Types'


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'docs'
        db_table = 'Employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class Competency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'docs'
        db_table = 'Competency'
        verbose_name = 'Competency'
        verbose_name_plural = 'Competencies'


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_id = models.ForeignKey(Category)
    type_id = models.ForeignKey(DocumentType)
    test_id = models.ForeignKey(Test, null=True, blank=True)
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'docs'
        db_table = 'Document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class CompetencyDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competency_id = models.ForeignKey(Competency)
    file_path = models.TextField(verbose_name='File Path')
    employee_id = models.ForeignKey(Employee)
    completion_date = models.DateTimeField(default=timezone.now)
    renewal_date = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.completion_date:
            self.renewal_date = self.completion_date + timezone.timedelta(days=365)
        if self.file_path:
            temp_path = self.file_path.replace("\"", "").replace("\\", "/").replace(" ", "%20")
            self.file_path = "file:///{}".format(temp_path)
        super(CompetencyDocument, self).save()

    def __str__(self):
        return self.competency_id.title + "(" + self.employee_id.name + ")"

    class Meta:
        app_label = 'docs'
        db_table = 'CompetencyDocument'
        verbose_name = 'Competency Document'
        verbose_name_plural = 'Competency Documents'



