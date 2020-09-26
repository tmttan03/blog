# Generated by Django 3.0.4 on 2020-03-20 12:24

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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField()),
                ('cover', models.ImageField(default='/default/cover.jpg', upload_to='cover')),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Archived', 'Archived'), ('Published', 'Published')], default='Draft', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]