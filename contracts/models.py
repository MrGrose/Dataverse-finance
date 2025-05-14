from django.db import models
from django.utils.safestring import mark_safe
from accounts.models import Person, Manager
from threads.models import Education_Thread

from typing import Any
from decimal import Decimal


class Contract(models.Model):
    """Модель заключения контракта с авторами или ведущеми/соведущими"""
    contract_number = models.AutoField(
        primary_key=True,
        verbose_name="Номер контракта"
    )
    authors = models.ManyToManyField(
        "Author",
        blank=True,
        related_name="contracts"
    )
    presenters = models.ManyToManyField(
        "Presenter",
        blank=True,
        related_name="contracts"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создание",
        auto_now_add=True
    )
    started_at = models.DateField(verbose_name="Запуск контракта")
    ended_at = models.DateField(verbose_name="Окончание контракта")
    created_by = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        related_name="created_contracts",
        verbose_name="Кто завел контракт"
    )
    responsible_manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        related_name="responsible_contracts",
        verbose_name="Ответственный сотрудник",
        blank=True,
        null=True
    )
    comment_manager = models.TextField(verbose_name="Комментарий менеджера", blank=True)

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ["contract_number"]

    def __str__(self) -> str:
        return f"Контракт №{self.contract_number} {self.get_authors_info()} {self.get_presenters_info()}"

    def get_authors_info(self: Any) -> str:
        return ", ".join([f"{author.author.username} ({author.reward_percent}%)" for author in self.authors.all()])

    def get_presenters_info(self: Any) -> str:
        return ", ".join([f"{presenter.presenter.username} ({presenter.hourly_rate}/час)" for presenter in self.presenters.all()])


class Author(models.Model):
    """Модель автороского контракта"""
    author = models.ForeignKey(
        Person,
        on_delete=models.CASCADE, 
        verbose_name="Преподаватель"
    )
    thead = models.ManyToManyField(
        Education_Thread,
        blank=True,
        related_name="author_theads"
    )
    revenue = models.DecimalField(
        verbose_name="Ожидаемый оборот/прибыль",
        blank=True,
        max_digits=18,
        decimal_places=2
    )
    reward_percent = models.DecimalField(
        verbose_name="Процент",
        max_digits=8,
        decimal_places=1
    )
    reward_type = models.CharField(
        verbose_name="Тип награды",
        choices=[
            ("Оборот", "Оборот"),
            ("Прибыль", "Прибыль")
            ],
        default="Оборот"
    )
    currency = models.CharField(
        verbose_name="Тип валюты",
        choices=[
            ("rub", "RUB"),
            ("usd", "USD")],
        default="rub"
    )

    class Meta:
        verbose_name = "Авторский"
        verbose_name_plural = "_Авторские"

    def __str__(self) -> str:
        return f"{self.author} Выручки:{self.revenue} {self.currency}-Процент:{self.reward_percent}%-Тип награды:{self.reward_type}"


class Presenter(models.Model):
    """Модель по часового контракта ведущего"""
    presenter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Ведущий"
    )
    thead = models.ManyToManyField(
        Education_Thread,
        blank=True,
        related_name="presenter_theads"
    )
    estimate = models.DecimalField(
        verbose_name="Прогнозное кол-во часов",
        max_digits=8,
        decimal_places=1
    )
    hourly_rate = models.DecimalField(
        verbose_name="Ставка за час",
        max_digits=8,
        decimal_places=1
    )
    currency = models.CharField(
        verbose_name="Тип валюты",
        choices=[
            ("rub", "RUB"),
            ("usd", "USD")],
        default="rub"
    )

    class Meta:
        verbose_name = "Ведущий"
        verbose_name_plural = "_Ведущие"

    def __str__(self) -> str:
        return f"{self.presenter}"


class Accrual(models.Model):
    """Модель начисления выплаты по контакту"""
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE
    )
    accrual_flags = models.CharField(
        choices=[
            ("collapsed", "Схлопнутое"),
            ("correction", "Корректировка"),
            ("non_financial", "Нефинансовое")],
        default=None,
        blank=True
    )
    accrual_status = models.CharField(
        choices=[
            ("pending", "Ожидание"),
            ("verified", "Проверено")],
        default="pending",
        blank=True
    )
    payed = models.BooleanField(
        verbose_name="Оплата",
        default=False
    )
    created_by = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        verbose_name="Кто завел начисление",
        blank=True
    )
    updated_by = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_accruals",
        verbose_name="Кто изменил начисление",
        blank=True
    )
    comment_manager = models.TextField(
        verbose_name="Комментарий менеджера",
        null=True,
        blank=True
    )
    hours_worked = models.DecimalField(
        null=True,
        blank=True,
        verbose_name="Фактические часы",
        max_digits=5,
        decimal_places=1,
        help_text="Проставлять факт. часов при выборе контракта Ведущий"
        )
    real_revenue = models.DecimalField(
        null=True,
        blank=True,
        verbose_name="Фактический оборот/выручка",
        max_digits=10,
        decimal_places=2,
        help_text="Проставлять факт. при выборе контракта Авторский"
        )

    calculation_formula = models.JSONField(
        verbose_name="Формула расчета",
        default=dict,
        help_text="Автоматически подставляется при сохранении",
        blank=True
    )

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"

    def __str__(self) -> str:
        return f"Начисление {self.contract}"

    @property
    def formatted_formula(self) -> str:
        """Отображение формулы расчета"""
        if not self.calculation_formula:
            return "Нет данных"
        formula = self.calculation_formula.get("formula", "")
        html_formula = formula.replace("\n", "<br>")
        return mark_safe(html_formula)

    def save(self, *args, **kwargs) -> None:
        self.set_contract_type()
        self.update_calculation_formula()
        super().save(*args, **kwargs)

    def set_contract_type(self) -> None:
        """Определение типа контракта"""
        has_authors = self.contract.authors.exists()
        has_presenters = self.contract.presenters.exists()
        if has_authors and has_presenters:
            self.contract_type = "combined"
        elif has_authors:
            self.contract_type = "author"
        elif has_presenters:
            self.contract_type = "presenter"

    def update_calculation_formula(self) -> None:
        """Сериализация данных и сохранение в calculation_formula"""
        raw_data = self.get_raw_data()
        result = self.calc(raw_data)

        if raw_data and result is not None:
            self.calculation_formula = {
                "formula": self.generate_formula_text(result, raw_data),
                # "raw_data": jsons.dump(raw_data)
            }
        else:
            self.calculation_formula = {"error": "Недостаточно данных для расчета"}

    def get_raw_data(self) -> dict[str, Any]:
        """Получение данных из авторского/ведущего контракта"""
        raw_data = {}
        try:
            if self.contract_type == "author":
                authors = self.contract.authors.all()
                if authors.exists():
                    raw_data = {
                        "authors": [],
                        "total_revenue": self.real_revenue if self.real_revenue else Decimal("0"),
                        "currency": authors[0].currency if authors else "rub"
                    }
                    for author in authors:
                        raw_data["authors"].append({
                            "name": str(author.author),
                            "reward_percent": author.reward_percent,
                        })

            elif self.contract_type == "presenter":
                presenters = self.contract.presenters.all()
                if presenters.exists():
                    raw_data = {
                        "presenters": [],
                        "hours_worked": float(self.hours_worked) if self.hours_worked else None,
                        "currency": presenters[0].currency
                    }
                    for presenter in presenters:
                        raw_data["presenters"].append({
                            "name": str(presenter.presenter),
                            "hourly_rate": float(presenter.hourly_rate),
                        })
            elif self.contract_type == "combined":
                raw_data = {
                    "authors": [],
                    "presenters": [],
                    "currency": "rub"
                }
                authors = self.contract.authors.all()
                if authors.exists():
                    raw_data["authors"] = [{
                        "name": str(author.author),
                        "reward_percent": float(author.reward_percent),
                    } for author in authors]
                    raw_data["total_revenue"] = float(self.real_revenue) if self.real_revenue else 0.0

                presenters = self.contract.presenters.all()
                if presenters.exists():
                    raw_data["presenters"] = [{
                        "name": str(presenter.presenter),
                        "hourly_rate": float(presenter.hourly_rate),
                    } for presenter in presenters]
                    raw_data["hours_worked"] = float(self.hours_worked) if self.hours_worked else 0.0
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
        return raw_data

    def calc(self, raw_data: Any) -> Any | None:
        """Вычисляет сумму начисления из авторского/ведущего контракта"""
        if not raw_data:
            return None
        total = Decimal(0)
        try:
            if "authors" in raw_data and raw_data.get("total_revenue", 0) > 0:
                for author in raw_data["authors"]:
                    percent = Decimal(str(author["reward_percent"]))
                    revenue = Decimal(str(raw_data["total_revenue"]))
                    total += (percent * revenue) / 100

            if "presenters" in raw_data and raw_data.get("hours_worked", 0) > 0:
                hours = Decimal(str(raw_data["hours_worked"]))
                for presenter in raw_data["presenters"]:
                    rate = Decimal(str(presenter["hourly_rate"]))
                    total += hours * rate

            return total.quantize(Decimal('0.01'))
        except (KeyError, TypeError) as e:
            print(f"Ошибка расчета: {e}")
            return None

    def generate_formula_text(self, result: Decimal, raw_data: dict) -> str:
        """Генерация формулы по авторскому/ведущему контракта"""
        formula_lines = []

        if "authors" in raw_data and raw_data.get("total_revenue", 0) > 0:
            formula_lines.append("Авториский: ")
            for author in raw_data["authors"]:
                line = (
                    f"{author['name']}: {author['reward_percent']}% * "
                    f"{raw_data['total_revenue']} {raw_data['currency']} = "
                    f"{(Decimal(author['reward_percent'])) * Decimal(raw_data['total_revenue']) / 100:.2f}"
                )
                formula_lines.append(line)

        if "presenters" in raw_data and raw_data.get("hours_worked", 0) > 0:
            formula_lines.append("\nВедущий: ")
            for presenter in raw_data["presenters"]:
                line = (
                    f"{presenter['name']}: {raw_data['hours_worked']} ч. × "
                    f"{presenter['hourly_rate']} {raw_data['currency']}/ч. = "
                    f"{(Decimal(raw_data['hours_worked'])) * Decimal(presenter['hourly_rate']):.2f}"
                )
                formula_lines.append(line)

        formula_lines.append(f"\nИтого: {result} {raw_data.get('currency', 'RUB')}")
        return "".join(formula_lines)