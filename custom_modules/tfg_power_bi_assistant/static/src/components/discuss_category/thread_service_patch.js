/* @odoo-module */

import { ThreadService } from "@mail/core/common/thread_service";
import { compareDatetime } from "@mail/utils/common/misc";

import { patch } from "@web/core/utils/patch";

patch(ThreadService.prototype, {
    /**
     * @override
     * @param {import("models").Thread} thread
     * @param {boolean} pushState
     */
    setDiscussThread(thread, pushState) {
        super.setDiscussThread(thread, pushState);
        if (this.ui.isSmall && thread.type === "aichat") {
            this.store.discuss.activeTab = "aichat";
        }
    },

    canLeave(thread) {
        return thread.type !== "aichat" && super.canLeave(thread);
    },

    canUnpin(thread) {
        if (thread.type === "aichat") {
            return thread.message_unread_counter === 0;
        }
        return super.canUnpin(thread);
    },

    /** @deprecated */
    sortChannels() {
        super.sortChannels();
        // Live chats are sorted by most recent interest date time in the sidebar.
        this.store.discuss.aichat.threads.sort(
            (t1, t2) =>
                compareDatetime(t2.lastInterestDateTime, t1.lastInterestDateTime) || t2.id - t1.id
        );
    },

    /**
     * @returns {boolean} Whether the aichat thread changed.
     */
    goToOldestUnreadaichatThread() {
        const oldestUnreadThread = this.store.discuss.aichat.threads
            .filter((thread) => thread.isUnread)
            .sort(
                (t1, t2) =>
                    compareDatetime(t1.lastInterestDateTime, t2.lastInterestDateTime) ||
                    t1.id - t2.id
            )[0];
        if (!oldestUnreadThread) {
            return false;
        }
        if (this.store.discuss.isActive) {
            this.setDiscussThread(oldestUnreadThread);
            return true;
        }
        const chatWindow = this.store.ChatWindow.insert({ thread: oldestUnreadThread });
        if (chatWindow.hidden) {
            this.chatWindowService.makeVisible(chatWindow);
        } else if (chatWindow.folded) {
            this.chatWindowService.toggleFold(chatWindow);
        }
        this.chatWindowService.focus(chatWindow);
        return true;
    },
});
