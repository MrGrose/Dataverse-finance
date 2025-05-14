from django.db import models


class Person(models.Model):
    username = models.CharField(max_length=30, verbose_name="Пользователь", null=True, blank=True)
    contact_email = models.EmailField(verbose_name="контактный email", null=True, blank=True)
    contact_phone = models.CharField(verbose_name="контактный тел.", null=True, blank=True)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self) -> str:
        return f"{self.username}"


class Manager(models.Model):
    manager = models.CharField(max_length=30, verbose_name="Менеджер", null=True, blank=True)

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self) -> str:
        return f"Менеджер {self.manager}"
