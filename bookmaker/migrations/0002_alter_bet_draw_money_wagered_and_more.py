# Generated by Django 5.0.1 on 2024-01-12 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookmaker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bet",
            name="draw_money_wagered",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="bet",
            name="loose_money_wagered",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="bet",
            name="win_money_wagered",
            field=models.IntegerField(default=1),
        ),
    ]