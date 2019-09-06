from nutrition.utils import InfoWithLabel


class EnergyValueWidget(InfoWithLabel):
    """ Widget with energy value of the product. """

    def __init__(self):
        super().__init__("Информация о продукте:", width=300)

