from .models import (
    BeneficiaryListSummaryFarmer,
    BeneficiaryListSummaryHousehold,
)


def get_models():
    return [
        BeneficiaryListSummaryFarmer,
        BeneficiaryListSummaryHousehold,
    ]
