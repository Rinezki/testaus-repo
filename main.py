"""
Main module of MobileFoodDeliveryAPP. 
Includes Tkinter UI and its functions.
"""
# pylint: disable=too-few-public-methods

#"Too few public methods" disabled because of class "OrderData"
#does not contain any methods.

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

from User_Registration import UserRegistration
from Order_Placement import Cart, OrderPlacement, UserProfile, RestaurantMenu, PaymentMethod
from Restaurant_Browsing import RestaurantDatabase, RestaurantBrowsing
from item_price import Price

# Utility functions for user data storage
USERS_FILE = "users.json"

def load_users():
    """
    Loads user data from JSON-file and returns it in key-value pair.
    If file not exist, returns empty.
    """
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    """
    Saves user data to JSON-file.
    """
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

class Application(tk.Tk):
    """
    Application itself. Shows startup frame first
    and calls different frames when needed.
    """
    def __init__(self):
        """
        Initializes app
        """
        super().__init__()
        self.title("Mobile Food Delivery App")
        self.geometry("600x400")

        # Load user registration data from file
        self.user_data = load_users()

        # Initialize core classes
        self.registration = UserRegistration()
        self.registration.users = self.user_data  # Load existing users into registration system

        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

        # Initially no user logged in
        self.logged_in_email = None

        # Create initial frame
        self.current_frame = None
        self.show_startup_frame()

    def show_startup_frame(self):
        """
        Shows StartupFrame in startup of the app.
        """
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StartupFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        """
        Shows RegisterFrame.
        """
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegisterFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        """
        Shows LoginFrame.
        """
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def login_user(self, email):
        """
        Closes LoginFrame after logging in to show MainAppFrame.
        """
        self.logged_in_email = email
        # After login, show main app frame
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainAppFrame(self, email)
        self.current_frame.pack(fill="both", expand=True)


class StartupFrame(tk.Frame):
    """
    Defines StartupFrame class.
    """
    def __init__(self, master):
        """
        Initializes StartupFrame.
        """
        super().__init__(master)
        tk.Label(
            self, text="Welcome to the Mobile Food Delivery App", font=("Arial", 16)
            ).pack(pady=30)

        tk.Button(self, text="Register", command=self.go_to_register, width=20).pack(pady=10)
        tk.Button(self, text="Login", command=self.go_to_login, width=20).pack(pady=10)

    def go_to_register(self):
        """
        Shows RegisterFrame.
        """
        self.master.show_register_frame()

    def go_to_login(self):
        """
        Shows LoginFrame.
        """
        self.master.show_login_frame()


class RegisterFrame(tk.Frame):
    """
    Defines RegisterFrame class.
    """
    def __init__(self, master):
        """
        Initializes RegisterFrame.
        """
        super().__init__(master)

        tk.Label(self, text="Register New User", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")
        self.conf_pass_entry = self.create_entry("Confirm Password:", show="*")

        tk.Button(self, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        """
        Creates registration entry for user data and returns it.
        """
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def register_user(self):
        """
        Saves user data from inputted entry if data is correct and shows LoginFrame.
        Shows error if occured.
        """
        email = self.email_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.conf_pass_entry.get()

        result = self.master.registration.register(email, password, confirm_password)
        if result["success"]:
            # Save the updated users to file
            save_users(self.master.registration.users)
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.show_login_frame()
        else:
            messagebox.showerror("Error", result["error"])

    def go_back(self):
        """
        Shows StartupFrame.
        """
        self.master.show_startup_frame()


class LoginFrame(tk.Frame):
    """
    Defines LoginFrame class.
    """
    def __init__(self, master):
        """
        Initializes LoginFrame.
        """
        super().__init__(master)

        tk.Label(self, text="User Login", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        """
        Creates login entry for user data registration and returns it.
        """
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def login(self):
        """
        Validates login entry with given credentials and logs in if valid.
        Shows error if occured.
        """
        email = self.email_entry.get()
        password = self.pass_entry.get()
        # Validate login
        # For simplicity, just check if user exists and password matches
        users = self.master.registration.users
        if email in users and users[email]["password"] == password:
            self.master.login_user(email)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def go_back(self):
        """
        Shows StartupFrame.
        """
        self.master.show_startup_frame()


class MainAppFrame(tk.Frame):
    """
    Defines MainAppFrame class.
    """
    def __init__(self, master, user_email):
        """
        Initializes MainAppFrame.
        """
        super().__init__(master)
        tk.Label(self, text=f"Welcome, {user_email}", font=("Arial", 14)).pack(pady=10)

        self.user_email = user_email
        self.database = master.database
        self.browsing = master.browsing

        self.order_data = OrderData()

        # Search Frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Cuisine:").pack(side="left")
        self.cuisine_var = tk.Entry(search_frame)
        self.cuisine_var.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_restaurants).pack(side="left")

        # Results Treeview
        self.results_tree = ttk.Treeview(
            self, columns=("cuisine", "location", "rating"), show="headings"
            )
        self.results_tree.heading("cuisine", text="Cuisine")
        self.results_tree.heading("location", text="Location")
        self.results_tree.heading("rating", text="Rating")
        self.results_tree.pack(pady=10, fill="x")

        # Buttons for actions
        action_frame = tk.Frame(self)
        action_frame.pack(pady=5)
        tk.Button(
            action_frame, text="View All Restaurants", command=self.view_all_restaurants
            ).pack(side="left", padx=5)
        tk.Button(
            action_frame, text="Add Item to Cart", command=self.add_item_to_cart
            ).pack(side="left", padx=5)
        tk.Button(action_frame, text="View Cart", command=self.view_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="Checkout", command=self.checkout).pack(side="left", padx=5)

    def search_restaurants(self):
        """
        Searches restaurants with filters given in search frame.
        """
        self.results_tree.delete(*self.results_tree.get_children())
        cuisine = self.cuisine_var.get().strip()
        results = self.browsing.search_by_filters(cuisine_type=cuisine if cuisine else None)
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def view_all_restaurants(self):
        """
        Shows all restaurants in database.
        """
        self.results_tree.delete(*self.results_tree.get_children())
        results = self.database.get_restaurants()
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def add_item_to_cart(self):
        """
        Shows popup for addig item to cart.
        """
        # For simplicity, let's assume user always adds "Pizza"
        # A more sophisticated approach: Let user select from menu items.
        # We will show a small popup to choose items.
        menu_popup = AddItemPopup(self, self.order_data.restaurant_menu, self.order_data.cart)
        self.wait_window(menu_popup)

    def view_cart(self):
        """
        Shows cart view.
        """
        cart_view = CartViewPopup(self, self.order_data.cart)
        self.wait_window(cart_view)

    def checkout(self):
        """
        Validates order and proceeds if success. Shows checkout after proceeding.
        """
        # Validate order and proceed if valid
        validation = self.order_data.order_placement.validate_order()
        if not validation["success"]:
            messagebox.showerror("Error", validation["message"])
            return

        # Show Checkout Popup
        checkout_popup = CheckoutPopup(self, self.order_data.order_placement)
        self.wait_window(checkout_popup)


class AddItemPopup(tk.Toplevel):
    """
    Defines AddItemPopup class.
    """
    def __init__(self, master, menu, cart):
        """
        Initializes AddItemPopup.
        """
        super().__init__(master)
        self.title("Add Item to Cart")
        self.menu = menu
        self.cart = cart

        tk.Label(self, text="Select an item to add to cart:").pack(pady=10)

        self.item_var = tk.StringVar()
        self.item_var.set(self.menu.available_items[0] if self.menu.available_items else "")
        tk.OptionMenu(self, self.item_var, *self.menu.available_items).pack(pady=5)

        tk.Label(self, text="Quantity:").pack()
        self.qty_entry = tk.Entry(self)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(pady=5)

        tk.Label(self, text="Price: ").pack(pady=5)
        self.price_label = tk.Label(self, text="")
        self.price_label.pack(pady=5)
        self.item_var.trace_add("write", lambda *args: self.update_price())
        self.qty_entry.bind("<KeyRelease>", lambda event: self.update_price())

        tk.Button(self, text="Add to Cart", command=self.add_to_cart).pack(pady=10)

    def add_to_cart(self):
        """
        Adds item with quantity and price information to cart. Shows cart info.
        """
        item = self.item_var.get()
        qty = int(self.qty_entry.get())
        price = float(Price.get_price("menu.json", f"{item}"))
        msg = self.cart.add_item(item, price, qty)
        messagebox.showinfo("Cart", msg)
        self.destroy()

    def calculate_price(self, item, qty):
        """
        Calculates total price
        """
        if Price.get_price("menu.json", f"{item}") is None:
            return "NaN"

        price = float(Price.get_price("menu.json", f"{item}"))
        total = round(price * qty, 2)
        return total

    def update_price(self):
        """
        Updates price label when item or quantity changes
        """
        item = self.item_var.get()
        try:
            qty = int(self.qty_entry.get())
        except ValueError:
            qty = 0

        price = self.calculate_price(item, qty)
        self.price_label.config(text=f"{price} $")



class CartViewPopup(tk.Toplevel):
    """
    Defines CartViewPopup class.
    """
    def __init__(self, master, cart):
        """
        Initialize CartViewPopup
        """
        super().__init__(master)
        self.title("Cart Items")

        items = cart.view_cart()
        if not items:
            tk.Label(self, text="Your cart is empty").pack(pady=20)
        else:
            for i in items:
                tk.Label(self, text=f"{i['name']} x{i['quantity']} = ${i['subtotal']:.2f}").pack()


class CheckoutPopup(tk.Toplevel):
    """
    Defines CheckoutPopup class.
    """
    def __init__(self, master, order_placement):
        """
        Initialize CheckoutPopup
        """
        super().__init__(master)
        self.title("Checkout")
        self.order_placement = order_placement

        order_data = order_placement.proceed_to_checkout()
        tk.Label(self, text="Review your order:", font=("Arial", 12)).pack(pady=10)

        # Show items
        for item in order_data["items"]:
            tk.Label(
                self, text=f"{item['name']} x{item['quantity']} = ${item['subtotal']:.2f}"
                    ).pack()

        total = order_data["total_info"]
        tk.Label(self, text=f"Subtotal: ${total['subtotal']:.2f}").pack()
        tk.Label(self, text=f"Tax: ${total['tax']:.2f}").pack()
        tk.Label(self, text=f"Delivery Fee: ${total['delivery_fee']:.2f}").pack()
        tk.Label(self, text=f"Total: ${total['total']:.2f}").pack()

        tk.Label(self, text=f"Delivery Address: {order_data['delivery_address']}").pack(pady=5)

        # Payment method selection
        tk.Label(self, text="Payment Method:").pack(pady=5)
        self.payment_method = tk.StringVar()
        self.payment_method.set("credit_card")
        tk.Radiobutton(
            self, text="Credit Card",variable=self.payment_method, value="credit_card"
            ).pack()
        tk.Radiobutton(self, text="Paypal", variable=self.payment_method, value="paypal").pack()

        tk.Label(self, text="For credit card enter a 16-digit card number:").pack(pady=5)
        self.card_entry = tk.Entry(self)
        self.card_entry.insert(0, "1234567812345678")
        self.card_entry.pack(pady=5)

        tk.Button(self, text="Confirm Order", command=self.confirm_order).pack(pady=10)

    def confirm_order(self):
        """
        Process order confirmation with the given payment method.
        """
        payment_method_obj = PaymentMethod()  # Mock payment method handling in the old code
        # Actually, we have PaymentProcessing class.
        # Let's just rely on PaymentMethod for simplicity here.
        # If you wanted to use PaymentProcessing, you could do so by integrating it as well.
        # For now, we'll simulate PaymentMethod.process_payment by checking if total > 0.
        # In a full scenario, integrate PaymentProcessing similarly.

        # Confirm the order
        result = self.order_placement.confirm_order(payment_method_obj)
        if result["success"]:
            messagebox.showinfo(
                "Order Confirmed",
                f"Order ID: {result['order_id']}\nEstimatedDelivery: {
                    result['estimated_delivery']}"
                )
            self.destroy()
        else:
            messagebox.showerror("Error", result["message"])

class OrderData:
    """
    Defines Order data with user profile, cart, restaurant menu and order placement.
    """
    def __init__(self):
        """
        Initializes OrderData.
        """
        # Create user's profile and cart
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
