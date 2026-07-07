/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { DomainSelector } from "@web/core/domain_selector/domain_selector";
// import { Domain, InvalidDomainError } from "@web/core/domain";
// import { EvaluationError } from "@web/core/py_js/py_builtin";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

export class G2PBeneficiariesComponent extends Component {
    static template = "g2p_beneficiaries_info_tpl";
    static components = {
        DomainSelector
    };
    static props = {
        context: { type: Object, optional: true },
        resModel: { type: String, optional: true },
        record: { type: Object, optional: true },
        readonly: { type: Boolean, optional: true },
    };

    setup() {
        const recordData = this.props.record?.data || {};
        this.state = useState({
            title: _t("Beneficiaries"),
            records: [],
            page: 1,
            pageSize: 3,
            totalCount: 0,
            totalPages: 1,
            target_registry: recordData.target_registry || null,
            searched: false,
            domain: "[]",
            showAllColumns: false,
        });
        this.orm = useService("orm");
        console.log(this);
    }

    onDomainChange(newDomain) {
        this.state.domain = newDomain;
        this.render();
    }

    getEvaluatedDomain() {
        return this.state.domain;
    }

    searchRegistrants() {
        this.state.searched = true;  // show title and pagination when search is clicked
        this.state.page = 1;
        this.state.pageSize = 20;
        this._fetchRecords();
    }

    async _fetchRecords() {
        const result = await this.orm.call(
            'g2p.bgtask.summary.wizard',
            'get_beneficiaries',
            [this.props.record.resId, this.state.page, this.state.pageSize, this.getEvaluatedDomain()],
            {},
        );

        if (result?.response_body) {
            const body = result.response_body;
            this.state.records = body.response_payload?.beneficiaries || [];
            this.state.totalCount = body.pagination_response?.number_of_items || 0;
            this.state.totalPages = body.pagination_response?.number_of_pages || 1;
        } else if (result?.message) {
            this.state.records = result.message.beneficiaries || [];
            this.state.totalCount = result.message.total_beneficiary_count || 0;
            this.state.totalPages = Math.ceil(this.state.totalCount / this.state.pageSize) || 1;
        } else if (result) {
            this.state.records = result.records || [];
            this.state.totalCount = result.total_count || 0;
            this.state.totalPages = Math.ceil(this.state.totalCount / this.state.pageSize) || 1;
        }
    }

    async nextPage() {
        if (this.state.page < this.state.totalPages) {
            this.state.page++;
            await this._fetchRecords();
        }
    }

    async prevPage() {
        if (this.state.page > 1) {
            this.state.page--;
            await this._fetchRecords();
        }
    }

    toggleColumns() {
        this.state.showAllColumns = !this.state.showAllColumns;
    }
}

export const g2pBeneficiariesWidget = {
    component: G2PBeneficiariesComponent,
    extractProps({ attrs }, dynamicInfo) {
        console.log(attrs, dynamicInfo)
        return {
            resModel: attrs.model,
            context: dynamicInfo.context,
        };
    },
};
registry.category("view_widgets").add("g2p_beneficiaries_widget", g2pBeneficiariesWidget);
