odoo.define('planning_slot_custom.progress_bar', function (require) {
    "use strict";

    var utils = require('web.utils');
    var FieldRegistry = require('web.field_registry');
    var FieldProgressBar = require('web.basic_fields').FieldProgressBar;

    var progressbar = FieldProgressBar.extend({
        _render_value: function (v) {
            var value = this.value;
            var max_value = this.max_value;
            if (!isNaN(v)) {
                if (this.edit_max_value) {
                    max_value = v;
                } else {
                    value = v;
                }
            }
            value = value || 0;
            max_value = max_value || 0;
    
            var widthComplete;
            if (value <= max_value) {
                widthComplete = value/max_value * 100;
            } else {
                widthComplete = 100;
            }
    
            this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value)
                .attr('aria-valuemin', '0')
                .attr('aria-valuemax', max_value)
                .attr('aria-valuenow', value);
            this.$('.o_progressbar_complete').css('width', widthComplete + '%');
    
            if (!this.write_mode) {
                if (max_value !== 100) {
                    this.$('.o_progressbar_value').text(utils.human_number(value) + " / " + utils.human_number(max_value));
                } else {
                    this.$('.o_progressbar_value').text(utils.human_number(value) + "%");
                }
                if (this.model == "project.task" && this.viewType == "form" && this.mode == "readonly")
                {
                    if (this.record.data.planned_hours < this.record.data.effective_hours) {
                        this.$('.o_progressbar_complete').css("background-color", 'red');
                    }
                }
            } else if (isNaN(v)) {
                this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
                this.$('.o_progressbar_value').focus().select();
            }
        },
    });
      
    FieldRegistry.add('progressbar_task_custom', progressbar);
});