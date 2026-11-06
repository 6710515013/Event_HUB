
from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("events", "Category")

    categories = [
        "การศึกษา/อบรม",
        "เทคโนโลยี/IT/Programmer",
        "กีฬา/การแข่งขัน",
        "ศิลปะ/วัฒนธรรม",
        "ดนตรี/ความบันเทิง",
        "จิตอาสา/บำเพ็ญประโยชน์",
        "พบปะ/สร้างเครือข่าย",
        "ธุรกิจ/อาชีพ/หางาน",
        "ศาสนา/พัฒนาจิตใจ",
        "สิ่งแวดล้อม/อนุรักษ์ธรรมชาติ",
        "ท่องเที่ยว",
        "สุขภาพ/พัฒนาตนเอง",
        "เทศกาล",
    ]

    for category_name in categories:
        Category.objects.get_or_create(name=category_name)


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_categories,
            migrations.RunPython.noop
        ),
    ]
