/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { GanttRenderer } from "@web_gantt/gantt_renderer";

patch(GanttRenderer.prototype, {
  async setup() {
    super.setup(); // By using the super function, we can execute all parent functions along with ours.
  },

  onPillClicked(ev, pill) {
    debugger;
    this.model.metaData.canEdit = false;
    this.model.metaData.canDelete = false;
    this.model.mutex.exec(
      () => this.props.openDialog({ resId: pill.record.id }) // (canEdit is also considered in openDialog)
    );
  },

});
