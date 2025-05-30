/* @odoo-module */

import { reactive } from "@odoo/owl";

import { registry } from "@web/core/registry";

export class AIChatCoreWeb {
    constructor(env, services) {
        Object.assign(this, {
            busService: services.bus_service,
        });
        /** @type {import("@mail/core/common/messaging_service").Messaging} */
        this.messagingService = services["mail.messaging"];
        /** @type {import("@mail/core/common/store_service").Store} */
        this.store = services["mail.store"];
    }

    setup() {
        this.messagingService.isReady.then((data) => {
            if (data.current_user_settings?.is_discuss_sidebar_category_aichat_open) {
                this.store.discuss.aichat.isOpen = true;
            }
            /* this.busService.subscribe("res.users.settings", (payload) => {
                if (payload) {
                    this.store.discuss.livechat.isOpen =
                        payload.is_discuss_sidebar_category_livechat_open ??
                        this.store.discuss.livechat.isOpen;
                }
            }); */
        });
    }
}

export const aichatCoreWeb = {
    dependencies: ["bus_service", "mail.messaging", "mail.store"],
    start(env, services) {
        const aichatCoreWeb = reactive(new AIChatCoreWeb(env, services));
        aichatCoreWeb.setup();
        return aichatCoreWeb;
    },
};

registry.category("services").add("tfg_power_bi_assistant.core.web", aichatCoreWeb);
