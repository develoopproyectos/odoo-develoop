/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { GanttController } from '@web_gantt/gantt_controller';

patch(GanttController.prototype, {
  async setup() {   
    debugger
    // TODO =========== CAMBIO HERENCIA - NEW =============
    if(this.env.searchModel.resModel === 'planning.slot'){
      this.props.modelParams.metaData.decorationFields.push('x_stage_id');
      this.props.modelParams.metaData.decorationFields.push('x_task_date_deadline'); 
      this.props.modelParams.metaData.decorationFields.push('x_resourse_plannable_hours'); 
    }
    // TODO =========== END    =============
    super.setup(); // By using the super function, we can execute all parent functions along with ours.
  },

});
