# Generated by Django 5.1.5 on 2025-03-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpleblog', '0016_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Image',
            field=models.ImageField(blank=True, default='/Userprofile/user.png', upload_to='images/'),
        ),
    ]
