/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { GanttRenderer } from "@web_gantt/gantt_renderer";

patch(GanttRenderer.prototype, {
    async onPlanningCellClicked(row, column) {
        if (
            this.model.metaData.resModel === "planning.slot" &&
            row.isGroup &&
            !column.isFoldable
        ) {
            const action = await this.orm.call(
                "planning.slot",
                "action_open_slot_log_from_gantt",
                [row.resId, column.start.toISODate()],
            );

            if (action) {
                this.actionService.doAction(action);
            }

            return;
        }

        if (row.isGroup && !column.isFoldable) {
            return this.model.toggleRow(row.id);
        }

        return this.onCellClicked(row.id, column, row.grid.row);
    },

    onPlanningCellMouseEnter(ev, row, column) {
        if (
            this.model.metaData.resModel === "planning.slot" &&
            row.isGroup &&
            !column.isFoldable
        ) {
            ev.currentTarget.style.cursor = "pointer";
            ev.currentTarget.style.outline = "1px solid #28a745";
        }
    },

    onPlanningCellMouseLeave(ev) {
        ev.currentTarget.style.cursor = "";
        ev.currentTarget.style.outline = "";
    },
});