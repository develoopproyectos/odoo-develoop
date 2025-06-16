/* @odoo-module */

import { ChatWindow } from "@mail/core/common/chat_window";

import { patch } from "@web/core/utils/patch";

import { registry } from "@web/core/registry";

registry.category("actions").add("reload_and_open_channel", (env, { params }) => {
    if (!params || !params.channel_id) {
        console.error("Parámetros inválidos en reload_and_open_channel:", params);
        return;
    }

    const channelId = params.channel_id;
    window.location.href = `${window.location.origin}${window.location.pathname}${window.location.search}#action=mail.action_discuss&menu_id=768&cids=1&active_id=discuss.channel_${channelId}`;
    

    setTimeout(() => {
        window.location.reload();
    }, 1);
});

patch(ChatWindow.prototype, {
    async close(options) {
        const thread = this.thread;
        await super.close(options);
        if (thread?.type === "aichat") {
            await thread?.isLoadedDeferred;
            if (thread.messages.length === 0) {
                this.threadService.unpin(thread);
            }
        }
    },
});
