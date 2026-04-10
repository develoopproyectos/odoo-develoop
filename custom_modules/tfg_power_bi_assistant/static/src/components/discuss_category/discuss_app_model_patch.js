/* @odoo-module */

import { DiscussApp } from "@mail/core/common/discuss_app_model";
import { Record } from "@mail/core/common/record";

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(DiscussApp, {
    new(data) {
        const res = super.new(data);
        res.aichat = {
            extraClass: "o-mail-DiscussSidebarCategory-aichat",
            id: "aichat",
            name: _t("AI Chat"),
            isOpen: false,
            canView: false,
            canAdd: false,
            serverStateKey: "is_discuss_sidebar_category_aichat_open",
        };
        return res;
    },
});

patch(DiscussApp.prototype, {
    setup(env) {
        super.setup(env);
        this.aichat = Record.one("DiscussAppCategory");
    },
});
