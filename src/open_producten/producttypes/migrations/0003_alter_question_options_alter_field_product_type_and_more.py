# Generated by Django 4.2.13 on 2024-07-10 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("producttypes", "0002_category_alter_producttype_conditions_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="question",
            options={"verbose_name": "Question", "verbose_name_plural": "Questions"},
        ),
        migrations.AlterField(
            model_name="field",
            name="product_type",
            field=models.ForeignKey(
                help_text="The product type that this field is part of",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fields",
                to="producttypes.producttype",
                verbose_name="Product Type",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer",
            field=models.TextField(verbose_name="Answer"),
        ),
        migrations.AlterField(
            model_name="question",
            name="question",
            field=models.CharField(max_length=250, verbose_name="Question"),
        ),
    ]
