{
    "name": "PBMS Theme",
    "category": "G2P",
    "version": "3.1.1",
    "sequence": 1,
    "author": "G2P",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": ["base", "web", "auth_signup", "website"],
    "data": [
        "templates/g2p_login_page.xml",
        "templates/g2p_reset_password.xml",
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "pbms_theme_extension/static/src/js/g2p_window_title.js",
            "pbms_theme_extension/static/src/css/style.css",
        ],
        "web.assets_frontend": [
            "pbms_theme_extension/static/src/scss/new_login_page.scss",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
