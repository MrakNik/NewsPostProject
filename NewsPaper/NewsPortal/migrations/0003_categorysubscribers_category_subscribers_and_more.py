# Generated by Django 4.1 on 2022-09-08 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('NewsPortal', '0002_alter_post_time_in'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySubscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(through='NewsPortal.CategorySubscribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categorysubscribers',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.category'),
        ),
        migrations.AddField(
            model_name='categorysubscribers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='categorysubscribers',
            unique_together={('category', 'user')},
        ),
    ]