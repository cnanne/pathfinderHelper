# Generated by Django 2.2.12 on 2020-06-22 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20200622_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pc',
            name='race',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.SelectedRace'),
        ),
        migrations.AlterField(
            model_name='wieldableitem',
            name='area',
            field=models.CharField(choices=[('2H', 'Two Handed'), ('1H', 'One Handed')], max_length=2),
        ),
    ]