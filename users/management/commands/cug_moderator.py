from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='product_moderator')
        if created:
            content_type = ContentType.objects.get_for_model(Product)
            perm_set_published = Permission.objects.get(
                codename='set_published',
                content_type=content_type,
            )
            perm_change_category = Permission.objects.get(
                codename='change_category',
                content_type=content_type,
            )
            group.permissions.add(perm_set_published)
            group.permissions.add(perm_change_category)
            group.permissions.add(Permission.objects.get(codename='change_product', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='add_product', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='view_product', content_type=content_type))
            group.save()
            print('Группа создана')
        else:
            print('Группа уже существует')
        # Group.objects.all().delete()
