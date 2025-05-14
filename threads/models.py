from django.db import models
from django.utils import timezone


class Education_Thread(models.Model):
    """Модель Образовательных потоков"""
    name = models.CharField(verbose_name="Название потока", max_length=200, blank=True)
    started_at = models.DateField(verbose_name="Начало потока")
    ended_at = models.DateField(verbose_name="Окончание потока")
    type_course = models.CharField(
        verbose_name="Тип курса",
        max_length=20,
        choices=[
            ("regular", "regular"),
            ("bootcamp", "bootcamp"),
            ("workshop", "workshop"),
            ("indi", "indi"),
        ], blank=True
    )
    articul = models.CharField(verbose_name="Артикул потока", max_length=20, blank=True)

    class Meta:
        verbose_name = "Образовательный поток"
        verbose_name_plural = "Образовательные потоки"

    def __str__(self) -> str:
        return f"{self.name} - {self.articul}"

    def generate_articul(self) -> str:
        """Генерация артикула из названия и типа курса"""
        name_part = "".join([c for c in self.name if c.isalpha()])[:3].upper()
        type_map = {
            "regular": "RG",
            "bootcamp": "BC",
            "workshop": "WS",
            "indi": "IN",
        }
        type_part = type_map.get(self.type_course, "XX")
        return f"{name_part}-{self.started_at}-{type_part}"

    def save(self, *args, **kwargs) -> None:
        # При изменение названия потока, даты, курса, перезаписывается артикул
        if self.name and self.type_course:
            self.articul = self.generate_articul()
        super().save(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        """Отображение статуса потока"""
        today = timezone.localdate()
        return self.started_at <= today <= self.ended_at