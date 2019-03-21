from django.db import models, migrations


def load_codes(apps, schema_editor):
    Code = apps.get_model("calculator", "Codes")
    code_food = Code(id=1, name='Food & Beverage', tax_pct=0.1, is_refundable=True, non_taxable_limit=0)
    code_food.save()
    code_tobacco = Code(id=2, name='Tobacco', tax_pct=0.1, tax_pct_2=0.02, is_refundable=False, non_taxable_limit=0)
    code_tobacco.save()
    code_entertainment = Code(id=3, name='Entertainment', tax_pct=0.01, is_refundable=False, non_taxable_limit=100)
    code_entertainment.save()

class Migration(migrations.Migration):
    dependencies = [
        ('calculator', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(load_codes),
    ]
