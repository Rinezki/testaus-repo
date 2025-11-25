import pytest
from unittest.mock import MagicMock
from Order_Placement import OrderPlacement  


def test_confirm_order_success():
    # --- Mockataan Cart ---
    cart = MagicMock()
    cart.items = [MagicMock(name="Burger")]      # mock-item
    cart.calculate_total.return_value = {"total": 15.0}
    cart.view_cart.return_value = ["Burger"]

    # --- Mockataan UserProfile ---
    user_profile = MagicMock()
    user_profile.delivery_address = "Mock Street 123"

    # --- Mockataan RestaurantMenu ---
    restaurant_menu = MagicMock()
    restaurant_menu.is_item_available.return_value = True

    # --- Mockataan PaymentMethod ---
    payment_method = MagicMock()
    payment_method.process_payment.return_value = True

    # --- Luodaan OrderPlacement testattavaksi ---
    order = OrderPlacement(cart, user_profile, restaurant_menu)

    # --- Suoritetaan confirm_order ---
    result = order.confirm_order(payment_method)

    # --- Varmistetaan odotettu toiminta ---
    assert result["success"] is True
    assert result["message"] == "Order confirmed"
    assert "order_id" in result

    # varmistetaan että maksua kutsuttiin oikealla summalla
    payment_method.process_payment.assert_called_once_with(15.0)


def test_confirm_order_item_not_available():
    cart = MagicMock()
    cart.items = [MagicMock(name="Pizza")]

    user_profile = MagicMock()
    restaurant_menu = MagicMock()
    restaurant_menu.is_item_available.return_value = False

    payment_method = MagicMock()

    order = OrderPlacement(cart, user_profile, restaurant_menu)

    result = order.confirm_order(payment_method)

    assert result["success"] is False
    assert result["message"] == "Order validation failed"


def test_confirm_order_payment_fails():
    cart = MagicMock()
    cart.items = [MagicMock(name="Burger")]
    cart.calculate_total.return_value = {"total": 10.0}

    user_profile = MagicMock()
    restaurant_menu = MagicMock()
    restaurant_menu.is_item_available.return_value = True

    payment_method = MagicMock()
    payment_method.process_payment.return_value = False  # maksun epäonnistuminen

    order = OrderPlacement(cart, user_profile, restaurant_menu)

    result = order.confirm_order(payment_method)

    assert result["success"] is False
    assert result["message"] == "Payment failed"