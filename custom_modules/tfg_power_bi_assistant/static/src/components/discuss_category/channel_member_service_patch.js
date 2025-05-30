/* @odoo-module */

import { ChannelMemberService } from "@mail/core/common/channel_member_service";
import { patch } from "@web/core/utils/patch";

patch(ChannelMemberService.prototype, {
    getName(member) {
        if (member.thread.type !== "aichat") {
            return super.getName(member);
        }
        if (member.persona.name) {
            return member.persona.name;
        }
        if (member.persona.is_public) {
            return member.thread.anonymous_name;
        }
        return super.getName(member);
    },
});
