/** @odoo-module */

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

import { Component, useState } from "@odoo/owl";
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
        this.rpc = useService("rpc");

        this.state = useState({
            status: "idle", // idle, inviting
            invite: null,
        });        
    }

    onInputChange(ev) {
            const value = ev.target.value;
            this.props.record.update({
                ai_service_api_key: value,
        });
    }


    get validateButtonText() {
        if (this.state.status === "validating") {
            return _t("Validating...");
        }
        return _t("Validate");
    }

    validate() {
        if (!this.props.record.data.ai_service_api_key.length) {
            throw new Error(_t("Empty API Service Key"));
        }
    }


    /**
     * Send validation for valid API Service Key.
     *
     * @private
     */
    async ValidateAIService() {
        try {
            this.validate();
        } catch (e) {
            this.notification.add(e.message, { type: "danger" });
            return;
        }

        this.state.status = "validating";

        try {
            const res = await this.rpc(`/validation/ai_service`, {
                api_key: this.props.record.data.ai_service_api_key,
            });

            if (res.success) {
                this.notification.add(_t("The API Key entered was validated correctly"), { type: "success" });                
            } else {
                this.notification.add(_t("The API Key entered is not correct"), { type: "warning" });                
            }
        } catch (error) {
            this.notification.add(error.message || _t("Validation Error"), { type: "danger" });
        } finally {
            this.state.status = "idle";
        }
    }
}

export const resConfigApiKeyValidation = {
    component: ResConfigApiKeyValidation,
};

registry.category("view_widgets").add("res_config_api_key_validation", resConfigApiKeyValidation);
