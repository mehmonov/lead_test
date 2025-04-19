from django.contrib.auth.models import Group


def create_attorney_group():
    group_name = "attorney"
    group, created = Group.objects.get_or_create(name=group_name)

    print(f"Group '{group_name}' created with permission.")
    return group
