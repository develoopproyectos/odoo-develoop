/** @odoo-module */

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

import { Component, useState, onWillStart } from "@odoo/owl";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

class ResConfigApiKeyValidation extends Component {
    static template = "res_config_api_key_validation";
    static props = {
        ...standardWidgetProps,
    };

    setup() {
        this.orm = useService("orm");
        this.invite = useService("user_invite");
        this.action = useService("action");
        this.notification = useService("notification");
        this.user = useService("user");

        this.state = useState({
            status: "idle", // idle, inviting
            validation_key: "",
            invite: null,
        });        
    }


    get validateButtonText() {
        if (this.state.status === "validating") {
            return _t("Validating...");
        }
        return _t("Validate");
    }


    /**
     * Send invitation for valid and unique email addresses
     *
     * @private
     */
    async sendInvite() {
        try {
            //this.validate();
        } catch (e) {
            this.notification.add(e.message, { type: "danger" });
            return;
        }

        this.state.status = "validating";

        try {
            //TODO           
        } finally {
            this.state.validation_key = "";
            this.state.status = "idle";
        }
    }
}

export const resConfigApiKeyValidation = {
    component: ResConfigApiKeyValidation,
};

registry.category("view_widgets").add("res_config_api_key_validation", resConfigApiKeyValidation);
