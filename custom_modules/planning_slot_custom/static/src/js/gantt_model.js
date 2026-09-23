/** @odoo-module **/

import { PlanningGanttModel } from "@planning/views/planning_gantt/planning_gantt_model";
import { patch } from "@web/core/utils/patch";

patch(PlanningGanttModel.prototype, {
    get hasMultiCreate() {
        return false;
    },
});