from odoo import models, fields

from .registry import G2PRegistry


class G2PFarmerRegistry(models.Model):
    _name = "g2p.register.farmer"
    _description = "Farmer Registry"
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

    # G2PPerson fields
    foundational_id = fields.Char(string="Foundational ID", index=True)
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    given_name = fields.Char(string="Given Name")
    prefix = fields.Char(string="Prefix")
    suffix = fields.Char(string="Suffix")
    gender = fields.Selection(
        selection=[
            ("MALE", "Male"),
            ("FEMALE", "Female"),
            ("OTHERS", "Others"),
            ("UNKNOWN", "Unknown"),
        ],
        string="Gender",
    )
    birth_date = fields.Date(string="Birth Date")
    phone_numbers = fields.Json(string="Phone Numbers")
    emails = fields.Json(string="Emails")
    marital_status = fields.Selection(
        selection=[
            ("SINGLE", "Single"),
            ("MARRIED", "Married"),
            ("DIVORCED", "Divorced"),
            ("WIDOWED", "Widowed"),
            ("SEPARATED", "Separated"),
            ("UNKNOWN", "Unknown"),
        ],
        string="Marital Status",
    )
    occupation = fields.Char(string="Occupation")
    income_level = fields.Char(string="Income Level")
    language_code = fields.Char(string="Language Code")
    registration_date = fields.Date(string="Registration Date")

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

    # G2PFarmer fields
    estimated_age = fields.Integer(string="Estimated Age")
    has_personal_phone = fields.Boolean(string="Has Personal Phone")
    disabled = fields.Boolean(string="Disabled")
    disability_type = fields.Selection(
        selection=[
            ("VISION", "Vision"),
            ("HEARING", "Hearing"),
            ("MOBILITY", "Mobility"),
            ("COGNITION", "Cognition"),
            ("SELF_CARE", "Self Care"),
            ("COMMUNICATION", "Communication"),
        ],
        string="Disability Type",
    )
    disability_severity = fields.Selection(
        selection=[
            ("NO_DIFFICULTY", "No Difficulty"),
            ("SOME_DIFFICULTY", "Some Difficulty"),
            ("A_LOT_OF_DIFFICULTY", "A Lot of Difficulty"),
            ("CANNOT_DO_AT_ALL", "Cannot Do At All"),
        ],
        string="Disability Severity",
    )
    source_of_income = fields.Selection(
        selection=[
            ("CROP_PRODUCTION", "Crop Production"),
            ("LIVESTOCK_PRODUCTION", "Livestock Production"),
            ("GOVERNMENT_NGO_SUPPORT", "Government / NGO Support"),
            ("OTHERS", "Others"),
        ],
        string="Source of Income",
    )
    source_of_income_other = fields.Char(string="Source of Income (Other)")
    language_spoken = fields.Char(string="Language Spoken")
    education_level = fields.Selection(
        selection=[
            ("ILLITERATE", "Illiterate"),
            ("CAN_READ_AND_WRITE", "Can Read and Write"),
            ("BASIC", "Basic"),
            ("INTERMEDIARY", "Intermediary"),
            ("HIGHER_EDUCATION", "Higher Education"),
        ],
        string="Education Level",
    )
    national_id_masked = fields.Char(string="National ID (Masked)")
