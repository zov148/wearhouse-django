from django.db import migrations

def seed_admin_demo(apps, schema_editor):
    Brand = apps.get_model('shop', 'Brand')
    Profile = apps.get_model('shop', 'BrandProfile')
    for name, country, website, description in [
        ('URBAN', 'Россия', 'https://example.org/', 'Учебный бренд городской одежды.'),
        ('NORTHLINE', 'Финляндия', 'https://example.net/', 'Учебный бренд одежды для прохладной погоды и прогулок.'),
    ]:
        brand, _ = Brand.objects.get_or_create(name=name, defaults={'country': country})
        Profile.objects.get_or_create(brand=brand, defaults={'website': website, 'description': description})

class Migration(migrations.Migration):
    dependencies = [('shop', '0003_alter_brand_options_alter_brandprofile_options_and_more')]
    operations = [migrations.RunPython(seed_admin_demo, migrations.RunPython.noop)]
