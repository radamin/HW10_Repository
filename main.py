class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


class ProductDAO:
    """ProductDAO содержит методы для добавления, удаления и получения продуктов из базы данных (в данном случае список products)."""

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_all_products(self):
        return self.products


class ProductRepository:
    """ProductRepository использует ProductDAO для доступа к данным о продуктах.
    Он также содержит логику, связанную с продуктами, например, проверку на корректность данных."""

    def __init__(self, dao):
        self.dao = dao

    def add_product(self, product):
        # Проверка на корректность данных продукта
        if product.price <= 0:
            raise ValueError("Цена продукта должна быть положительным числом")
        self.dao.add_product(product)

    def remove_product(self, product):
        self.dao.remove_product(product)

    def get_all_products(self):
        return self.dao.get_all_products()


class ProductService:
    """ProductService использует ProductRepository для выполнения операций с продуктами,
    а также добавляет свою бизнес-логику, например, проверку цены продукта."""

    def __init__(self, repository):
        self.repository = repository

    def add_product(self, product):
        # Проверка цены продукта
        if product.price > 100:
            print("Цена продукта превышает 100")
        self.repository.add_product(product)


class UnitOfWork:
    """UnitOfWork позволяет группировать операции с продуктами в рамках транзакции.
    Мы регистрируем новые продукты и удаленные продукты в UnitOfWork и сохраняем или отменяем изменения."""

    def __init__(self):
        self.new_products = []
        self.removed_products = []

    def register_new(self, product):
        self.new_products.append(product)

    def register_removed(self, product):
        self.removed_products.append(product)

    def commit(self):
        for product in self.new_products:
            print("Сохранение нового продукта:", product.name)
            # Здесь должны быть операции сохранения продукта
        for product in self.removed_products:
            print("Удаление продукта:", product.name)
            # Здесь должны быть операции удаления продукта

        self.new_products = []
        self.removed_products = []


def main():
    dao = ProductDAO()
    repository = ProductRepository(dao)
    service = ProductService(repository)
    uow = UnitOfWork()

    # Создание нескольких продуктов
    product1 = Product(1, "Apple", 10)
    product2 = Product(2, "Orange", 20)
    product3 = Product(3, "Banana", 30)

    # Регистрация продуктов в Unit of Work
    uow.register_new(product1)
    uow.register_new(product2)

    # Добавление продуктов с помощью сервиса
    service.add_product(product1)
    service.add_product(product2)

    # Отмена транзакции
    uow.commit()  # изменения сохраняются
    uow.register_removed(product2)
    uow.register_removed(product3)

    uow.commit()  # изменения не сохраняются

    # Завершение транзакции и вывод списка всех продуктов
    products = repository.get_all_products()
    for product in products:
        print("ID:", product.id, "Name:", product.name, "Price:", product.price)


if __name__ == "__main__":
    main()
