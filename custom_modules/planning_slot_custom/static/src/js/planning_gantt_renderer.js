/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PlanningGanttRenderer } from "@planning/views/planning_gantt/planning_gantt_renderer";

patch(PlanningGanttRenderer.prototype, {
    _computeWorkHours(pill) {
        const workHours = super._computeWorkHours(...arguments);
        // TODO =========== CAMBIO HERENCIA - NEW =============
        return pill.recourse_plannable_hours;
        // TODO =========== END    =============
    },
});