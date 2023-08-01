class Mobile:
    class Client:
        """ SWAGGER TAGS FOR CLIENT MOBILE APP """
        PREFIX = 'mobile_client'

        PAYMENT = f'{PREFIX}_payment'
        CARD = f'{PREFIX}_card'
        QR_SCAN = f'{PREFIX}_qr_scan'
        PROFILE = f'{PREFIX}_profile'
        REGISTRATION = f'{PREFIX}_registration'
        AUTHORIZATION = f'{PREFIX}_authorization'

    class Driver:
        """Swagger tags for driver mobile app"""
        PREFIX = 'mobile_driver'

        ORDERS = f'{PREFIX}_orders'
        PROFILE = f'{PREFIX}_profile'
        REGISTRATION = f'{PREFIX}_registration'
        AUTHORIZATION = f'{PREFIX}_authorization'

    class Car:
        """Swagger tags for car mobile app"""
        PREFIX = 'mobile_car'

    class Staff:
        """Swagger tags for staff mobile app"""
        PREFIX = 'mobile_staff'
