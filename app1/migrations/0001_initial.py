# Generated by Django 4.2.7 on 2024-06-07 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('category', models.CharField(choices=[('income', 'Income'), ('housing', 'Housing'), ('utilities', 'Utilities'), ('food', 'Food'), ('transportation', 'Transportation'), ('healthcare', 'Healthcare'), ('entertainment', 'Entertainment'), ('other', 'Other')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
