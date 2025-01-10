/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { GanttController } from '@web_gantt/gantt_controller';

patch(GanttController.prototype, {
  async setup() {   
    // TODO =========== CAMBIO HERENCIA - NEW =============
    this.props.modelParams.metaData.decorationFields.push('x_stage_id');
    this.props.modelParams.metaData.decorationFields.push('x_task_date_deadline'); 
    // TODO =========== END    =============
    super.setup(); // By using the super function, we can execute all parent functions along with ours.
  },

});
