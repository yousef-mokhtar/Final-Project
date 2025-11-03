JAZZMIN_SETTINGS = {
    "site_title": "استور، کاستومی",
    "site_header": "استور، کاستومی",
    "site_brand": "استور، کاستومی",
    "site_logo": "logo-type.svg", 
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-rounded",
    "site_icon": None,
    "welcome_sign": "به پنل مدیریت استور، کاستومی خوش آمدید",
    "copyright": "استور، کاستومی - ۱۴۰۴",

    "search_model": [
        "accounts.User",
        "products.Product",
        "orders.Order",
    ],

    "user_avatar": None,

    "topmenu_links": [
        {"name": "خانه", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "مستندات", "url": "https://github.com/farridav/django-jazzmin", "new_window": True},
        {"model": "accounts.User"},
        {"app": "products"},
    ],

    "usermenu_links": [
        {"name": "پروفایل", "url": "admin:accounts_user_change", "parameters": "request.user.pk"},
        {"name": "پشتیبانی", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    "order_with_respect_to": [
        "accounts", "accounts.user", "accounts.address",
        "products", "products.category", "products.product", "products.productimage",
        "seller", "seller.store", "seller.storeitem",
        "cart", "cart.cart", "cart.cartitem",
        "orders", "orders.order", "orders.orderitem", "orders.invoice", "orders.payment",
        "review", "review.review",
    ],

    "custom_links": {
        # مثال:
        # "products": [{
        #     "name": "ایجاد دسته‌بندی", 
        #     "url": "admin:products_category_add", 
        #     "icon": "fas fa-plus",
        #     "permissions": ["products.add_category"]
        # }]
    },

    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.user": "fas fa-user",
        "accounts.address": "fas fa-address-book",
        "auth.Group": "fas fa-users",
        
        "products": "fas fa-box-open",
        "products.category": "fas fa-tags",
        "products.product": "fas fa-box",
        "products.productimage": "fas fa-images",
        
        "seller": "fas fa-store",
        "seller.store": "fas fa-store-alt",
        "seller.storeitem": "fas fa-archive",
        
        "cart": "fas fa-shopping-cart",
        "cart.cart": "fas fa-shopping-basket",
        "cart.cartitem": "fas fa-cart-arrow-down",
        
        "orders": "fas fa-receipt",
        "orders.order": "fas fa-file-invoice",
        "orders.orderitem": "fas fa-file-invoice-dollar",
        "orders.invoice": "fas fa-file-invoice-dollar",
        "orders.payment": "fas fa-money-bill-wave",
        
        "review": "fas fa-comment",
        "review.review": "fas fa-comments",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs"
    },
    "language_chooser": False,
}