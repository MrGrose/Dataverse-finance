from django.contrib import admin
from contracts.models import Contract, Author, Presenter, Accrual


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "display_contract_number", "get_articul",  "created_at", "get_authors_info",
        "get_presenters_info", "started_at", "ended_at",
        "created_by", "comment_manager", "responsible_manager",
        )
    autocomplete_fields = ("authors", "presenters",)
    filter_horizontal = ("authors", "presenters",)
    search_fields = ('contract_number',)

    def display_contract_number(self, obj):
        return f"Контракт №{obj.contract_number}"
    display_contract_number.short_description = "Номер контракта"

    def get_authors_info(self, obj):
        return obj.get_authors_info()
    get_authors_info.short_description = "Автор (процент)"

    def get_presenters_info(self, obj):
        return obj.get_presenters_info()
    get_presenters_info.short_description = "Ведущий (ставка)"

    def get_articul(self, obj):
        return obj.get_articul()
    get_articul.short_description = "Арктикул"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "author", "get_thead", "reward_type",
        "revenue", "reward_percent", "currency",
    )
    search_fields = ('author__name',)
    autocomplete_fields = ["author", "thead",]

    def get_thead(self, obj):
        return ", ".join([str(art.articul) for art in obj.thead.all()])
    get_thead.short_description = "Артикул"


@admin.register(Presenter)
class PresenterAdmin(admin.ModelAdmin):
    list_display = (
        "presenter", "get_thead", "estimate",
        "hourly_rate", "currency",
    )
    search_fields = ('presenter__name',)
    autocomplete_fields = ["presenter", "thead",]

    def get_thead(self, obj):
        return ", ".join([str(art.articul) for art in obj.thead.all()])
    get_thead.short_description = "Артикул"


@admin.register(Accrual)
class AccrualAdmin(admin.ModelAdmin):
    list_display = (
        "display_accrual_number",
        "created_at",
        "created_by",
        "formatted_formula_display",
        "updated_by",
        "payed",
        "accrual_flags",
        "accrual_status",
        "comment_manager",
    )
    autocomplete_fields = ("contract",)
    readonly_fields = (
        "calculation_formula",
        "formatted_formula_display",
    )
    search_fields = ('contract__contract_number',)

    def display_accrual_number(self, obj):
        return f"Начисление #{obj.id}"
    display_accrual_number.short_description = "Начисление"

    def formatted_formula_display(self, obj):
        return obj.formatted_formula
    formatted_formula_display.short_description = "Расчет"