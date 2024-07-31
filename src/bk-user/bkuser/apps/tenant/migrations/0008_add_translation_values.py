# Generated by Django 3.2.25 on 2024-07-31 08:20

from django.db import migrations


def forwards_func(apps, schema_editor):
    """添加用户自定义字段翻译"""

    UserBuiltinField = apps.get_model("tenant", "UserBuiltinField")

    original_translation_mapping = {
        '用户名': 'Username',
        '姓名': 'Full Name',
        '邮箱': 'Email',
        '手机号': 'Phone Number',
        '手机国际区号': 'Phone Country Code',
    }

    fields = UserBuiltinField.objects.all()

    for field in fields:
        # 中文翻译直接原样赋值
        field.display_name_zh_cn = field.display_name
        field.display_name_en_us = original_translation_mapping[field.display_name]

    UserBuiltinField.objects.bulk_update(fields, ['display_name_zh_cn', 'display_name_en_us'])


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0007_add_translation_fields'),
    ]

    operations = [migrations.RunPython(forwards_func)]
