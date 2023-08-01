from django.db.models import TextChoices


class UserRoleChoices(TextChoices):
    ADMIN = "admin", "Администратор"
    SUPER_ADMIN = "super_admin", "Супер администратор"
    DIRECTOR = "director", "Директор"
    MANAGER = "manager", "Менеджер"
    SUPER_MANAGER = "super_manager", "Супер менеджер"
    OPERATOR = "operator", "Оператор"
    SUPER_OPERATOR = "super_operator", "Супер оператор"
    ACCOUNTING = "accounting", "Бухгалтерия"

    DRIVER = "driver", "Водитель"

    CLIENT = "client", "Клиент"


class DriverStatusChoices(TextChoices):
    START = "start", "Старт"
    COMFORT = "comfort", "Комфорт"
    BUSINESS = "business", "Бизнес"
    VIP = "vip", "VIP"
    DELIVERY = "delivery", "Доставка"


class AuthStatusChoices(TextChoices):
    NEW = "new", "Новый"
    VERIFY = "verify", "На проверке"
    HALF_DONE = "half_done", "Частично заполнен"
    DONE = "done", "Заполнен"


class ColorChoices(TextChoices):
    WHITE = "white", "Белый"
    BLACK = "black", "Черный"
    RED = "red", "Красный"
    BLUE = "blue", "Синий"
    GREEN = "green", "Зеленый"
    YELLOW = "yellow", "Желтый"
    GREY = "grey", "Серый"
    BROWN = "brown", "Коричневый"
    ORANGE = "orange", "Оранжевый"
    GOLD = "gold", "Золотой"
    SILVER = "silver", "Серебряный"
    BRONZE = "bronze", "Бронзовый"
    BEIGE = "beige", "Бежевый"
    BURGUNDY = "burgundy", "Бордовый"
    CHOCOLATE = "chocolate", "Шоколадный"


class PaymentTypeChoices(TextChoices):
    CASH = "cash", "Наличные"
    CARD = "card", "Карта"
    NON_CASH = "non_cash", "Безналичный расчет"
    BONUS = "bonus", "Бонусы"


class TripStatusChoices(TextChoices):
    WAITING = "waiting", "Ожидание"
    ACCEPTED = "accepted", "Принят"
    CANCELED_BY_CLIENT = "canceled_by_client", "Отменен клиентом"
    CANCELED_BY_DRIVER = "canceled_by_driver", "Отменен водителем"
    IN_PROGRESS = "in_progress", "В процессе"
    COMPLETED = "completed", "Завершен"
