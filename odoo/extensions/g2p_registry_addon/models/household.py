from odoo import models, fields

from .registry import G2PRegistry


class G2PRegisterHousehold(models.Model):
    _name = "g2p.register.households"
    _description = "Register Household"
    _inherit = "g2p.registry"

    # G2PRegister fields
    functional_record_id = fields.Char(string="Functional Record ID", index=True)
    link_internal_record_id = fields.Char(string="Link Internal Record ID", index=True)
    link_foundational_id = fields.Char(string="Link Foundational ID", index=True)
    record_name = fields.Char(string="Record Name")
    record_image_storage_id = fields.Text(string="Record Image Storage ID")
    created_by = fields.Char(string="Created By")
    created_at = fields.Datetime(string="Created At")
    last_approved_at = fields.Datetime(string="Last Approved At")
    last_approved_by = fields.Char(string="Last Approved By")
    search_text = fields.Text(string="Search Text")
    record_status = fields.Selection(
        selection=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("archived", "Archived"),
        ],
        string="Record Status",
        default="active",
    )
    record_status_reason = fields.Char(string="Record Status Reason")

    # G2PGeo fields
    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    altitude = fields.Char(string="Altitude")
    plus_code = fields.Char(string="Plus Code", index=True)
    address_line_1 = fields.Char(string="Address Line 1")
    address_line_2 = fields.Char(string="Address Line 2")
    postal_code = fields.Char(string="Postal Code", index=True)
    country_code = fields.Char(string="Country Code", index=True)
    geo_lowest_level_value_id = fields.Char(string="Geo Lowest Level Value ID", index=True)
    geo_code_hierarchy_json = fields.Json(string="Geo Code Hierarchy")

    # Household head
    household_head_internal_record_id = fields.Char(
        string="Household Head Internal Record ID", index=True
    )
    household_head_name = fields.Char(string="Household Head Name")
    headship_type = fields.Selection(
        selection=[
            ("MALE_HEADED", "Male Headed"),
            ("FEMALE_HEADED", "Female Headed"),
            ("CHILD_HEADED", "Child Headed"),
            ("ELDERLY_HEADED", "Elderly Headed"),
            ("DISABLED_HEADED", "Disabled Headed"),
        ],
        string="Headship Type",
    )

    # Household composition
    size_total = fields.Integer(string="Total Size")
    size_adults = fields.Integer(string="Adults")
    size_children_u5 = fields.Integer(string="Children Under 5")
    size_school_age = fields.Integer(string="School Age")
    size_elderly = fields.Integer(string="Elderly")
    number_of_female_members = fields.Integer(string="Number of Female Members")
    number_of_male_members = fields.Integer(string="Number of Male Members")
    elderly_member_present = fields.Boolean(string="Elderly Member Present")

    # Dwelling
    dwelling_type = fields.Selection(
        selection=[
            ("PERMANENT", "Permanent"),
            ("SEMI_PERMANENT", "Semi-Permanent"),
            ("TEMPORARY", "Temporary"),
        ],
        string="Dwelling Type",
    )
    roof_material = fields.Selection(
        selection=[
            ("THATCH", "Thatch"),
            ("CORRUGATED_IRON", "Corrugated Iron"),
            ("CONCRETE", "Concrete"),
            ("TILE", "Tile"),
            ("PLASTIC_SHEET", "Plastic Sheet"),
            ("OTHER", "Other"),
        ],
        string="Roof Material",
    )
    wall_material = fields.Selection(
        selection=[
            ("MUD", "Mud"),
            ("WOOD", "Wood"),
            ("BAMBOO", "Bamboo"),
            ("STONE", "Stone"),
            ("BRICK", "Brick"),
            ("CONCRETE", "Concrete"),
            ("OTHER", "Other"),
        ],
        string="Wall Material",
    )
    floor_material = fields.Selection(
        selection=[
            ("EARTH", "Earth"),
            ("WOOD", "Wood"),
            ("CEMENT", "Cement"),
            ("TILE", "Tile"),
            ("OTHER", "Other"),
        ],
        string="Floor Material",
    )
    tenure_status = fields.Selection(
        selection=[
            ("OWNED", "Owned"),
            ("RENTED", "Rented"),
            ("HOSTED", "Hosted"),
            ("TEMPORARY", "Temporary"),
        ],
        string="Tenure Status",
    )
    rooms_count = fields.Integer(string="Rooms Count")
    overcrowding_indicator = fields.Float(string="Overcrowding Indicator")

    # Utilities
    water_source_type = fields.Selection(
        selection=[
            ("PIPED", "Piped"),
            ("PUBLIC_TAP", "Public Tap"),
            ("WELL", "Well"),
            ("SPRING", "Spring"),
            ("SURFACE_WATER", "Surface Water"),
            ("RAINWATER", "Rainwater"),
            ("TANKER_TRUCK", "Tanker Truck"),
            ("OTHER", "Other"),
        ],
        string="Water Source Type",
    )
    water_distance_minutes = fields.Integer(string="Water Distance (Minutes)")
    sanitation_type = fields.Selection(
        selection=[
            ("FLUSH_TOILET", "Flush Toilet"),
            ("PIT_LATRINE", "Pit Latrine"),
            ("COMPOSTING_TOILET", "Composting Toilet"),
            ("SHARED", "Shared"),
            ("OPEN", "Open"),
            ("OTHER", "Other"),
        ],
        string="Sanitation Type",
    )
    lighting_source = fields.Selection(
        selection=[
            ("GRID", "Grid"),
            ("SOLAR", "Solar"),
            ("GENERATOR", "Generator"),
            ("KEROSENE", "Kerosene"),
            ("CANDLE", "Candle"),
            ("NONE", "None"),
        ],
        string="Lighting Source",
    )
    cooking_fuel_type = fields.Selection(
        selection=[
            ("ELECTRICITY", "Electricity"),
            ("GAS", "Gas"),
            ("KEROSENE", "Kerosene"),
            ("CHARCOAL", "Charcoal"),
            ("FIREWOOD", "Firewood"),
            ("BIOMASS", "Biomass"),
            ("OTHER", "Other"),
        ],
        string="Cooking Fuel Type",
    )
    mobile_phone_type = fields.Selection(
        selection=[
            ("NONE", "None"),
            ("BASIC", "Basic"),
            ("SMARTPHONE", "Smartphone"),
        ],
        string="Mobile Phone Type",
    )

    husband_dead = fields.Boolean(string="Is Husband Dead")
    husband_death_date = fields.Datetime(string="Husband Death Date")
