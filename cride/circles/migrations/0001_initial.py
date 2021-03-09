# Generated by Django 2.0.9 on 2021-03-09 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created_at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Last date time on which the object was modified.', verbose_name='modified_at')),
                ('name', models.CharField(max_length=140)),
                ('slug_name', models.SlugField(max_length=40, unique=True)),
                ('about', models.CharField(max_length=255, verbose_name='circle description')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='circles/pictures')),
                ('rides_offered', models.PositiveIntegerField(default=0)),
                ('rides_taken', models.PositiveIntegerField(default=0)),
                ('verified', models.BooleanField(default=False, help_text='Verified circles are also known as official communities.', verbose_name='verified circle')),
                ('is_public', models.BooleanField(default=True, help_text='Public circles are listed in the main page so everyone knows about their existence.')),
                ('is_limited', models.BooleanField(default=False, help_text='Limited circles can grow up to a fices number of members')),
                ('members_limit', models.PositiveIntegerField(default=0, help_text='If a circle is limted this will be the limit on the number of members.')),
            ],
            options={
                'ordering': ('-rides_taken', '-rides_offered'),
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
