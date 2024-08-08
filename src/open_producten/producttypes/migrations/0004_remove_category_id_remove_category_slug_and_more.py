# Generated by Django 4.2.13 on 2024-08-08 09:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        (
            "producttypes",
            "0003_alter_question_options_alter_field_product_type_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="id",
        ),
        migrations.RemoveField(
            model_name="category",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="condition",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="condition",
            name="id",
        ),
        migrations.RemoveField(
            model_name="condition",
            name="published",
        ),
        migrations.RemoveField(
            model_name="condition",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="field",
            name="id",
        ),
        migrations.RemoveField(
            model_name="file",
            name="id",
        ),
        migrations.RemoveField(
            model_name="link",
            name="id",
        ),
        migrations.RemoveField(
            model_name="price",
            name="id",
        ),
        migrations.RemoveField(
            model_name="priceoption",
            name="id",
        ),
        migrations.RemoveField(
            model_name="producttype",
            name="id",
        ),
        migrations.RemoveField(
            model_name="producttype",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="question",
            name="id",
        ),
        migrations.RemoveField(
            model_name="tag",
            name="id",
        ),
        migrations.RemoveField(
            model_name="tag",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="tagtype",
            name="id",
        ),
        migrations.RemoveField(
            model_name="upn",
            name="id",
        ),
        migrations.AddField(
            model_name="category",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="condition",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="link",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="price",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="priceoption",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="producttype",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="tagtype",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="upn",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
