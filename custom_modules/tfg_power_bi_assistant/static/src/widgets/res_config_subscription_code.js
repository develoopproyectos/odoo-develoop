/** @odoo-module */

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

import { Component, useState, onWillStart } from "@odoo/owl";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

class ResConfigSubscriptionCode extends Component {
    static template = "res_config_subscription_code";
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
                ai_service_sub_code: value,
        });
    }

    get validateButtonText() {
        if (this.state.status === "validating") {
            return _t("Validating...");
        }
        return _t("Validate");
    }

    validate() {
        if (!this.props.record.data.ai_service_sub_code.length) {
            throw new Error(_t("Empty Subscription Code"));
        }
    }
    
    /**
     * Send validation for the subscription code.
     *
     * @private
     */
    async ValidateSubCode() {
        try {
            this.validate();
        } catch (e) {
            this.notification.add(e.message, { type: "danger" });
            return;
        }

        this.state.status = "validating";

        try {
            const res = await this.rpc(`/validation/subscription_code`, {
                api_key: this.props.record.data.ai_service_sub_code,
            });

            if (res.success) {
                this.notification.add(_t("The Subscription Code entered was validated correctly"), { type: "success" });
            } else {
                this.notification.add(_t("The Subscription Code entered is not correct"), { type: "warning" });
            }
        } catch (error) {
            this.notification.add(error.message || _t("Validation Error"), { type: "danger" });
        } finally {
            this.state.status = "idle";
        }
    }
}

export const resConfigSubscriptionCode = {
    component: ResConfigSubscriptionCode,
};

registry.category("view_widgets").add("res_config_subscription_code", resConfigSubscriptionCode);
