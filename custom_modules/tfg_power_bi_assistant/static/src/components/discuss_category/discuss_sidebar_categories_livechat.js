/* @odoo-module */

import { discussSidebarCategoriesRegistry } from "@mail/discuss/core/web/discuss_sidebar_categories";

discussSidebarCategoriesRegistry.add(
    "aichats",
    {
        predicate: (store) =>
            store.discuss.aichat.threads.some(
                (thread) => thread.displayToSelf || thread.isLocallyPinned
            ),
        value: (store) => store.discuss.aichat,
    },
    { sequence: 20 }
);
